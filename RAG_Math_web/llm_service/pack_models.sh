#!/bin/bash

# 配置变量
MODEL_DIR="models"

# 检查模型目录是否存在
if [ ! -d "$MODEL_DIR" ]; then
    echo "错误：模型目录不存在！"
    exit 1
fi

# 打包模型文件
echo "正在打包模型文件..."
tar -czf models.tar.gz $MODEL_DIR

echo "模型打包完成：models.tar.gz" 