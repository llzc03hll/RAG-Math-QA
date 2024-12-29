# RAG数学问答系统

这是一个基于RAG（检索增强生成）的数学问答系统，使用Spring Boot和Python FastAPI构建。系统集成了Qwen2.5-0.5B-Instruct模型，并通过向量检索增强数学问题的回答质量。

## 项目结构

```
RAG_Math_web/
├── src/                    # Java后端代码
│   └── main/
│       ├── java/          # Java源代码
│       └── resources/     # 配置文件
├── llm_service/           # Python LLM服务
│   ├── main.py           # 主服务文件
│   ├── models/           # 数据模型
│   ├── services/         # 服务层
│   └── requirements.txt  # Python依赖
└── pom.xml               # Maven配置文件
```

## 技术栈

- **后端框架**: Spring Boot 3.2.2
- **数据库**: PostgreSQL（带pgvector扩展）
- **LLM模型**: Qwen2.5-0.5B-Instruct
- **向量嵌入**: Sentence Transformers
- **API框架**: FastAPI

## 功能特点

1. 数学问题智能回答
2. 基于向量相似度的知识检索
3. 支持数学知识库的动态扩展
4. RESTful API接口

## 安装说明

### 1. Java后端

```bash
# 克隆项目
git clone [repository-url]

# 进入项目目录
cd RAG_Math_web

# 使用Maven构建项目
mvn clean install
```

### 2. Python LLM服务

```bash
# 进入LLM服务目录
cd llm_service

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows使用: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 数据库配置

1. 安装PostgreSQL
2. 创建数据库：rag_math_db
3. 配置application.properties中的数据库连接信息

## 使用说明

1. 启动Java后端：
```bash
mvn spring-boot:run
```

2. 启动LLM服务：
```bash
cd llm_service
python main.py
```

3. 加载示例数据：
```bash
python load_sample_data.py
```

## API文档

- Java后端API: http://localhost:8080/swagger-ui.html
- LLM服务API: http://localhost:8000/docs

## 开发团队



## 许可证

MIT License 