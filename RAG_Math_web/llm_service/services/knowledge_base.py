import numpy as np
from typing import List, Optional
from sentence_transformers import SentenceTransformer
from models.math_knowledge import MathKnowledge, MathProblem

class KnowledgeBase:
    def __init__(self, embedding_model: SentenceTransformer):
        self.embedding_model = embedding_model
        self.knowledge_base: List[MathKnowledge] = []
        self.problem_base: List[MathProblem] = []
        
    def add_knowledge(self, knowledge: MathKnowledge) -> None:
        """添加知识条目"""
        # 生成embedding
        text = f"{knowledge.title} {knowledge.content}"
        knowledge.embedding = self.embedding_model.encode(text).tolist()
        self.knowledge_base.append(knowledge)
        
    def add_problem(self, problem: MathProblem) -> None:
        """添加问题"""
        # 生成embedding
        text = f"{problem.question} {problem.solution}"
        problem.embedding = self.embedding_model.encode(text).tolist()
        self.problem_base.append(problem)
        
    def search_knowledge(self, query: str, top_k: int = 3) -> List[MathKnowledge]:
        """搜索相关知识"""
        if not self.knowledge_base:
            return []
            
        # 生成查询的embedding
        query_embedding = self.embedding_model.encode(query)
        
        # 计算相似度
        similarities = []
        for knowledge in self.knowledge_base:
            if knowledge.embedding:
                similarity = np.dot(query_embedding, knowledge.embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(knowledge.embedding)
                )
                similarities.append((similarity, knowledge))
        
        # 排序并返回top_k个结果
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in similarities[:top_k]]
        
    def search_problems(self, query: str, top_k: int = 3) -> List[MathProblem]:
        """搜索相关问题"""
        if not self.problem_base:
            return []
            
        # 生成查询的embedding
        query_embedding = self.embedding_model.encode(query)
        
        # 计算相似度
        similarities = []
        for problem in self.problem_base:
            if problem.embedding:
                similarity = np.dot(query_embedding, problem.embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(problem.embedding)
                )
                similarities.append((similarity, problem))
        
        # 排序并返回top_k个结果
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in similarities[:top_k]]
        
    def get_relevant_context(self, query: str, top_k: int = 3) -> str:
        """获取相关上下文"""
        # 搜索相关知识和问题
        relevant_knowledge = self.search_knowledge(query, top_k)
        relevant_problems = self.search_problems(query, top_k)
        
        # 构建上下文
        context_parts = []
        
        # 添加相关知识
        if relevant_knowledge:
            context_parts.append("相关知识点：")
            for k in relevant_knowledge:
                context_parts.append(f"- {k.title}:")
                context_parts.append(f"  {k.content}")
                if k.examples:
                    context_parts.append("  示例：")
                    context_parts.extend(f"  * {example}" for example in k.examples)
                    
        # 添加相关问题
        if relevant_problems:
            context_parts.append("\n相关题目：")
            for p in relevant_problems:
                context_parts.append(f"- 问题：{p.question}")
                context_parts.append(f"  解答：{p.solution}")
                
        return "\n".join(context_parts) 