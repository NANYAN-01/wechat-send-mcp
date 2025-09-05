# wechat_send MCP 服务

一个通过企业微信机器人 Webhook 接口发送文件到微信群的 MCP (Model Context Protocol) 服务。

## 功能特性

- 🚀 支持多种文件输入方式：本地文件、网络文件、Base64 编码文件
- 🔧 基于 MCP 协议，可集成到各种 AI 助手和自动化工具中
- 📱 专为企业微信群聊设计，支持文件分享
- 🛡️ 完善的错误处理和临时文件管理

## 安装依赖

```bash
pip install -r requirements.txt
```

## 启动方式

### 1. 使用 uvx 启动（推荐）
```bash
# 安装 uv（如果还没有安装）
pip install uv

# 启动服务
uvx wechat-send

# HTTP 模式启动
uvx wechat-send --http 8000
```

### 2. 使用 npx 启动
```bash
# 安装依赖
npm install

# 启动服务
npx wechat-send

# HTTP 模式启动
npx wechat-send --http 8000
```

### 3. 使用 python -m 启动
```bash
# 标准模式启动
python -m wechat_send

# HTTP 模式启动
python -m wechat_send --http 8000
```

### 4. 传统方式启动
```bash
# 直接运行 server.py
python server.py

# HTTP 模式
python server.py --http 8000
```

## 工具说明

### send_file 工具

通过企业微信机器人发送文件到群聊。

**参数说明：**
- `webhook_url` (必需): 企业微信机器人 Webhook 地址
- `file_path` (可选): 本地文件路径
- `file_url` (可选): 通过 HTTP(S) 下载的文件 URL  
- `file_base64` (可选): 文件内容的 Base64 编码

**使用方式：**
三种文件输入方式三选一：
- 直接传 `file_path` - 指定本地文件路径
- 传 `file_url` - 自动下载网络文件到临时目录
- 传 `file_base64` - 将 Base64 编码的文件内容解码为临时文件

## 配置说明

### 企业微信机器人配置

1. 在企业微信群中添加机器人
2. 获取 Webhook 地址，格式如：`https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY`
3. 将 Webhook 地址作为 `webhook_url` 参数传入

### 环境变量

- `WEBHOOK_URL`: 默认的企业微信机器人 Webhook 地址（可选）

## 使用示例

### MCP 客户端调用示例

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "send_file",
    "arguments": {
      "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY",
      "file_url": "https://example.com/file.pdf"
    }
  }
}
```

### HTTP API 调用示例

```bash
curl -X POST https://your-server.com/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "send_file",
      "arguments": {
        "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY",
        "file_path": "/path/to/your/file.pdf"
      }
    }
  }'
```

## 技术架构

- **核心模块**: `main.py` - 包含文件发送的核心逻辑
- **MCP 服务**: `server.py` - 基于 FastMCP 框架的 MCP 服务器
- **模块入口**: `__main__.py` - Python 模块主入口点，支持 `python -m` 启动
- **包初始化**: `__init__.py` - Python 包初始化文件
- **uvx 支持**: `pyproject.toml` - 支持 uvx 启动的配置文件
- **npx 支持**: `package.json` + `index.js` - Node.js 包装器，支持 npx 启动
- **配置管理**: `mcp.json` - 魔塔社区服务配置和元数据
- **依赖管理**: `requirements.txt` - Python 包依赖

## 部署说明

### 本地部署

#### 方式一：使用 uvx（推荐）
```bash
git clone <repository-url>
cd wechat_send
pip install uv
uvx wechat-send
```

#### 方式二：使用 npx
```bash
git clone <repository-url>
cd wechat_send
npm install
npx wechat-send
```

#### 方式三：使用 python -m
```bash
git clone <repository-url>
cd wechat_send
pip install -r requirements.txt
python -m wechat_send
```

#### 方式四：传统方式
```bash
git clone <repository-url>
cd wechat_send
pip install -r requirements.txt
python server.py
```

### 云平台部署
- 支持 Railway、Heroku、Docker 等平台
- 支持魔塔社区部署（使用 `python -m wechat_send` 或 `uvx wechat-send`）
- 确保安装 Python 3.8+ 和所需依赖
- 设置必要的环境变量

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

