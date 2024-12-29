import requests
import json
import time

def test_basic_connection():
    """测试基本连接"""
    try:
        response = requests.get("http://localhost:8000/health")
        print("健康检查响应:", json.dumps(response.json(), ensure_ascii=False, indent=2))
        return True
    except Exception as e:
        print("连接测试失败:", str(e))
        return False

def test_ask_question():
    """测试问答功能"""
    url = "http://localhost:8000/ask"
    test_cases = [
        {
            "question": "1+1等于多少？",
            "context": ["这是一个简单的加法问题"]
        },
        {
            "question": "求解方程：x² + 2x + 1 = 0",
            "context": ["这是一个二次方程"]
        }
    ]
    
    for i, payload in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}:")
        print("问题:", payload["question"])
        try:
            start_time = time.time()
            response = requests.post(url, json=payload)
            end_time = time.time()
            
            print("状态码:", response.status_code)
            print("响应时间:", f"{end_time - start_time:.2f}秒")
            
            if response.status_code == 200:
                result = response.json()
                print("回答:", result["answer"])
            else:
                print("错误响应:", response.text)
        except Exception as e:
            print("请求错误:", str(e))
        print("-" * 50)

if __name__ == "__main__":
    print("=== 开始API测试 ===")
    if test_basic_connection():
        print("\n=== 测试问答功能 ===")
        test_ask_question()
    print("\n=== 测试完成 ===") 