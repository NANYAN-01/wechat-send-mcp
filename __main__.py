#!/usr/bin/env python3
"""
wechat_send MCP 服务的主入口模块
支持 python -m wechat_send 启动方式
"""

import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入并运行服务器
from server import mcp

def main():
    """主函数，用于命令行入口点"""
    # 检查命令行参数决定运行模式
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        # HTTP 模式，适用于 Dify 等通过 HTTP 调用的平台
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
        print(f"Starting MCP server in HTTP mode on port {port}")
        mcp.run_server("localhost", port)
    else:
        # 默认 stdio 模式，适配通用 MCP Host（如 IDE/代理）
        mcp.run()

if __name__ == "__main__":
    main()
