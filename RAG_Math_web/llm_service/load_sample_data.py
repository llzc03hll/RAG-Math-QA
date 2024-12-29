import requests
import json

def load_sample_knowledge():
    """加载示例数学知识"""
    knowledge_data = [
        {
            "title": "二次方程求根公式",
            "content": "对于二次方程ax² + bx + c = 0，其解为：x = [-b ± √(b² - 4ac)] / (2a)",
            "category": "代数",
            "keywords": ["二次方程", "求根公式", "代数"],
            "examples": [
                "例如：x² + 2x + 1 = 0，可以得到x = -1（重根）"
            ]
        },
        {
            "title": "三角形面积公式",
            "content": "三角形面积可以用底边乘以高除以2来计算：S = (b × h) / 2",
            "category": "几何",
            "keywords": ["三角形", "面积", "几何"],
            "examples": [
                "例如：底边6cm，高4cm的三角形面积为：(6 × 4) / 2 = 12平方厘米"
            ]
        }
    ]
    
    for knowledge in knowledge_data:
        try:
            response = requests.post(
                "http://localhost:8000/knowledge/add",
                json=knowledge
            )
            print(f"添加知识：{knowledge['title']}")
            print(f"响应：{response.json()}")
        except Exception as e:
            print(f"添加知识失败：{str(e)}")

def load_sample_problems():
    """加载示例数学题目"""
    problem_data = [
        {
            "question": "求解方程：x² + 4x + 4 = 0",
            "solution": "这是一个二次方程，可以使用配方法或求根公式解决。\n1. 使用求根公式：a=1, b=4, c=4\n2. x = [-4 ± √(16 - 16)] / 2 = -2（重根）",
            "difficulty": "中等",
            "category": "代数",
            "tags": ["二次方程", "求根公式"]
        },
        {
            "question": "计算三角形面积，已知底边长8cm，高6cm",
            "solution": "使用三角形面积公式：S = (b × h) / 2\n代入数据：S = (8 × 6) / 2 = 24平方厘米",
            "difficulty": "简单",
            "category": "几何",
            "tags": ["三角形", "面积计算"]
        }
    ]
    
    for problem in problem_data:
        try:
            response = requests.post(
                "http://localhost:8000/problem/add",
                json=problem
            )
            print(f"添加题目：{problem['question'][:20]}...")
            print(f"响应：{response.json()}")
        except Exception as e:
            print(f"添加题目失败：{str(e)}")

if __name__ == "__main__":
    print("开始加载示例数据...")
    load_sample_knowledge()
    load_sample_problems()
    print("示例数据加载完成！") 