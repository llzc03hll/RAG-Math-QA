#!/bin/bash

# 配置变量
MODEL_DIR="models"
VENV_DIR="venv"
REQUIREMENTS="requirements.txt"

# 创建虚拟环境
echo "创建Python虚拟环境..."
python -m venv $VENV_DIR

# 激活虚拟环境
source $VENV_DIR/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r $REQUIREMENTS

# 创建模型目录
mkdir -p $MODEL_DIR

# 如果模型文件存在，解压模型
if [ -f "models.tar.gz" ]; then
    echo "发现模型文件，正在解压..."
    tar -xzf models.tar.gz -C $MODEL_DIR
fi

# 启动服务
echo "启动服务..."
export MODEL_PATH=$MODEL_DIR
python main.py 