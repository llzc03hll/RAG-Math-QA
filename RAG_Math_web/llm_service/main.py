import os
import sys
import logging
from pathlib import Path
import numpy as np
import torch
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import warnings
from services.knowledge_base import KnowledgeBase
from models.math_knowledge import MathKnowledge, MathProblem

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 忽略特定警告
warnings.filterwarnings("ignore", category=UserWarning)

# 配置HuggingFace缓存目录
os.environ['TRANSFORMERS_CACHE'] = r"E:\huggingface_cache"
os.environ['HF_HOME'] = r"E:\huggingface_cache"
os.environ['HF_DATASETS_CACHE'] = r"E:\huggingface_cache"

app = FastAPI()

# 模型名称配置
LLM_MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def load_models():
    """加载模型，使用HuggingFace缓存机制"""
    print("正在初始化模型...")

    try:
        # 加载Embedding模型
        print(f"加载Embedding模型: {EMBEDDING_MODEL_NAME}")
        embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

        # 加载LLM模型
        print(f"加载Qwen模型: {LLM_MODEL_NAME}")
        tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(LLM_MODEL_NAME, trust_remote_code=True)

        # 配置模型
        if torch.cuda.is_available():
            print("使用GPU加速")
            model = model.half().cuda()
        else:
            print("使用CPU模式")
            model = model.float()
        model = model.eval()

        # 初始化知识库
        knowledge_base = KnowledgeBase(embedding_model)

        print("模型加载完成！")
        return embedding_model, tokenizer, model, knowledge_base

    except Exception as e:
        error_msg = f"模型加载失败: {str(e)}"
        print(error_msg)
        raise RuntimeError(error_msg)

# 初始化模型和知识库
embedding_model, tokenizer, model, knowledge_base = load_models()

class QuestionRequest(BaseModel):
    question: str
    context: Optional[List[str]] = None

class EmbeddingRequest(BaseModel):
    text: str

class KnowledgeRequest(BaseModel):
    title: str
    content: str
    category: str
    keywords: List[str]
    examples: List[str]

class ProblemRequest(BaseModel):
    question: str
    solution: str
    difficulty: str
    category: str
    tags: List[str]

MATH_PROMPT_TEMPLATE = """你是一个专业的数学老师。请根据以下信息回答问题。

相关知识库内容：
{context}

问题：{question}

请基于上述知识，提供详细的解答步骤和说明。如果知识库中有相关的例题，请参考其解题思路。
"""

@app.post("/knowledge/add")
async def add_knowledge(request: KnowledgeRequest):
    """添加数学知识到知识库"""
    try:
        knowledge = MathKnowledge(
            title=request.title,
            content=request.content,
            category=request.category,
            keywords=request.keywords,
            examples=request.examples
        )
        knowledge_base.add_knowledge(knowledge)
        return {"message": "知识添加成功", "knowledge": knowledge}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/problem/add")
async def add_problem(request: ProblemRequest):
    """添加数学题目到知识库"""
    try:
        problem = MathProblem(
            question=request.question,
            solution=request.solution,
            difficulty=request.difficulty,
            category=request.category,
            tags=request.tags
        )
        knowledge_base.add_problem(problem)
        return {"message": "题目添加成功", "problem": problem}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """处理数学问题（带RAG增强）"""
    try:
        logger.info(f"收到问题: {request.question}")
        
        # 从知识库获取相关上下文
        context = knowledge_base.get_relevant_context(request.question)
        if not context:
            context = "没有找到相关的知识点和例题。"
        
        # 准备提示
        prompt = MATH_PROMPT_TEMPLATE.format(
            context=context,
            question=request.question
        )
        
        logger.info("正在生成回答...")
        # 使用Qwen生成回答
        try:
            response = generate_response(prompt)
            logger.info("成功生成回答")
        except Exception as e:
            logger.error(f"生成回答时出错: {str(e)}")
            raise HTTPException(status_code=500, detail=f"生成回答失败: {str(e)}")
        
        # 生成问题的embedding
        try:
            embedding = embedding_model.encode(request.question)
            logger.info("成功生成embedding")
        except Exception as e:
            logger.error(f"生成embedding时出错: {str(e)}")
            raise HTTPException(status_code=500, detail=f"生成embedding失败: {str(e)}")
        
        result = {
            "question": request.question,
            "context_used": context,
            "answer": response,
            "embedding": embedding.tolist()
        }
        logger.info("请求处理完成")
        return result
        
    except Exception as e:
        logger.error(f"处理请求时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/embed")
async def create_embedding(request: EmbeddingRequest):
    """生成文本的向量嵌入"""
    try:
        embedding = embedding_model.encode(request.text)
        return {"embedding": embedding.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "服务正在运行"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "cuda_available": torch.cuda.is_available(),
        "pytorch_version": torch.__version__,
        "transformers_version": transformers.__version__
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    ) 