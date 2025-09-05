## wechat_send MCP 服务

### 依赖安装
```bash
pip install -r requirements.txt
```

### 启动方式
- 作为独立 MCP Server 通过 stdio 启动：
```bash
python server.py
```

### 暴露的工具
- send_file(
  - file_path: Optional[str]
  - file_url: Optional[str]
  - file_base64: Optional[str]
  - webhook_url: str
) -> str

### 说明
- 三种文件输入方式三选一：
  - 直接传 `file_path`
  - 传 `file_url`（会下载到临时文件再发送）
  - 传 `file_base64`（Base64 解码为临时文件再发送）
- 工具内部复用 `main.py` 中的 `send_file_to_wechat_group` 实现。
- 若在 IDE/代理中注册为 MCP Server，请将可执行命令指向 `python server.py`，工作目录为本项目根目录。

