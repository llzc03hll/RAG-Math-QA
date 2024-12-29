# 在Python解释器中运行以下代码
import torch
import transformers
import sentence_transformers
import fastapi
import uvicorn

print(f"PyTorch version: {torch.__version__}")

print(f"Transformers version: {transformers.__version__}")
if torch.cuda.is_available():
    print(f"CUDA版本: {torch.version.cuda}")
    print(f"GPU设备: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA不可用")

print("\n=== 检查完成 ===")
