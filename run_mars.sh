#!/bin/bash

# ==============================================================================
# Script Name: run_mars.sh
# Description: 自动化运行 Project Mars (Lightweight)
# Version: 1.0
# ==============================================================================

set -euo pipefail

# 获取脚本所在目录的绝对路径
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="${ROOT_DIR}/mars_env"

echo "========================================"
echo "    🚀 Starting Project Mars..."
echo "========================================"

# 1. 检查虚拟环境是否存在
if [ ! -d "${VENV_PATH}" ]; then
    echo "❌ 错误: 未找到虚拟环境 '${VENV_PATH}'。"
    echo "请先运行相关配置命令创建环境并安装依赖。"
    exit 1
fi

# 2. 检查 main.py 是否存在
if [ ! -f "${ROOT_DIR}/main.py" ]; then
    echo "❌ 错误: 未在目录 '${ROOT_DIR}' 中找到 main.py。"
    exit 1
fi

# 3. 激活虚拟环境并运行
echo "✅ 环境检查通过，正在启动程序..."
# 激活虚拟环境 (可选，但推荐用于环境变量一致性)
source "${VENV_PATH}/bin/activate"

# 显式使用虚拟环境内部的 Python 二进制文件运行，防止别名冲突
"${VENV_PATH}/bin/python" "${ROOT_DIR}/main.py"

echo ""
echo "========================================"
echo "    ✨ Project Mars 已退出。"
echo "========================================"
