import sys
import base64
import tempfile
import os
from typing import Optional

# 依赖: 官方 MCP Python SDK 的快速服务端
try:
    from fastmcp import FastMCP
except Exception as import_error:  # 兜底提示，便于在未安装依赖时给出清晰错误
    raise RuntimeError(
        "未找到 fastmcp 包，请先安装依赖：pip install fastmcp"
    ) from import_error

import requests
from main import send_file_to_wechat_group


# 定义 MCP 服务端
mcp = FastMCP("wechat_send")


@mcp.tool()
def send_file(
    file_path: Optional[str] = None,
    webhook_url: str = "",
    file_url: Optional[str] = None,
    file_base64: Optional[str] = None,
) -> str:
    """
    通过企业微信机器人 Webhook 发送文件到群聊。

    参数:
    - file_path: 本地文件路径（与 file_url/file_base64 三选一）
    - file_url: 通过 HTTP(S) 下载的文件 URL
    - file_base64: 文件内容的 Base64 编码
    - webhook_url: 企业微信机器人 Webhook 地址
    """
    if not webhook_url:
        return "error: webhook_url is required"

    temp_path: Optional[str] = None
    try:
        resolved_path: Optional[str] = None

        if file_path:
            resolved_path = file_path
        elif file_url:
            # 下载到临时文件
            with requests.get(file_url, stream=True, timeout=60) as r:
                r.raise_for_status()
                suffix = os.path.splitext(file_url.split("?")[0])[-1] or ""
                fd, temp_path = tempfile.mkstemp(suffix=suffix)
                os.close(fd)
                with open(temp_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            resolved_path = temp_path
        elif file_base64:
            # 解码到临时文件（无扩展名）
            fd, temp_path = tempfile.mkstemp()
            os.close(fd)
            with open(temp_path, "wb") as f:
                f.write(base64.b64decode(file_base64))
            resolved_path = temp_path
        else:
            return "error: one of file_path, file_url, file_base64 is required"

        send_file_to_wechat_group(resolved_path, webhook_url)
        return "ok"
    except Exception as e:  # 向 MCP Host 返回清晰错误
        return f"error: {e}"
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass


if __name__ == "__main__":
    import sys
    
    # 检查命令行参数决定运行模式
    if len(sys.argv) > 1 and sys.argv[1] == "--sse":
        # SSE 模式，适用于 Web 应用
        print("Starting MCP server in SSE mode")
        mcp.run("sse")
    else:
        # 默认 stdio 模式，适配通用 MCP Host（如 IDE/代理）
        mcp.run("stdio")


