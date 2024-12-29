import requests
import json

# 服务配置
BASE_URL = "http://localhost:8000"

def test_embedding():
    """测试文本向量嵌入功能"""
    print("\n测试文本向量嵌入功能...")
    url = f"{BASE_URL}/embed"
    
    test_text = "求解方程：x² + 2x + 1 = 0"
    payload = {"text": test_text}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            embedding = result["embedding"]
            print(f"✓ 成功生成向量嵌入")
            print(f"- 向量维度: {len(embedding)}")
            print(f"- 向量示例: [{', '.join(map(str, embedding[:3]))}...]")
        else:
            print(f"✗ 请求失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ 发生错误: {str(e)}")

def test_math_question():
    """测试数学问题回答功能"""
    print("\n测试数学问题回答功能...")
    url = f"{BASE_URL}/ask"
    
    # 测试案例
    test_cases = [
        {
            "question": "求解方程：x² + 2x + 1 = 0",
            "context": ["这是一个二次方程，可以使用配方法或求根公式解决。"]
        },
        {
            "question": "计算三角形面积，底边长6cm，高4cm",
            "context": ["三角形的面积计算公式：S = (底边×高)/2"]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试案例 {i}:")
        print(f"问题: {test_case['question']}")
        try:
            response = requests.post(url, json=test_case)
            if response.status_code == 200:
                result = response.json()
                print("✓ 成功获取回答")
                print(f"回答: {result['answer']}")
                print(f"向量维度: {len(result['embedding'])}")
            else:
                print(f"✗ 请求失败: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"✗ 发生错误: {str(e)}")

def main():
    """运行所有测试"""
    print("开始测试LLM服务...")
    
    # 测试服务是否在运行
    try:
        requests.get(f"{BASE_URL}")
        print("✓ 服务正在运行")
    except:
        print("✗ 服务未启动，请先启动服务")
        return
    
    # 运行测试
    test_embedding()
    test_math_question()

if __name__ == "__main__":
    main() 