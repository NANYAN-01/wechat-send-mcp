#!/usr/bin/env python3
"""
标准MCP over HTTP服务器，符合MCP协议规范
"""
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import traceback
from typing import Dict, Any

# 导入MCP工具
from server import send_file


class MCPHTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """处理MCP协议的POST请求"""
        try:
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            # 处理MCP请求
            response = self.handle_mcp_request(request_data)
            
            # 返回响应
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_error_response(str(e), traceback.format_exc())
    
    def handle_mcp_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理MCP协议请求"""
        method = request.get('method')
        params = request.get('params', {})
        request_id = request.get('id')
        
        if method == 'initialize':
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "wechat_send",
                        "version": "1.0.0"
                    }
                }
            }
        
        elif method == 'tools/list':
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "send_file",
                            "description": "通过企业微信机器人发送文件到群聊",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "webhook_url": {
                                        "type": "string",
                                        "description": "企业微信机器人Webhook地址"
                                    },
                                    "file_path": {
                                        "type": "string",
                                        "description": "本地文件路径"
                                    },
                                    "file_url": {
                                        "type": "string", 
                                        "description": "网络文件URL"
                                    },
                                    "file_base64": {
                                        "type": "string",
                                        "description": "Base64编码的文件内容"
                                    }
                                },
                                "required": ["webhook_url"]
                            }
                        }
                    ]
                }
            }
        
        elif method == 'tools/call':
            tool_name = params.get('name')
            arguments = params.get('arguments', {})
            
            if tool_name == 'send_file':
                result = send_file(
                    file_path=arguments.get('file_path'),
                    webhook_url=arguments.get('webhook_url', ''),
                    file_url=arguments.get('file_url'),
                    file_base64=arguments.get('file_base64')
                )
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": result
                            }
                        ]
                    }
                }
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def send_error_response(self, message: str, details: str = ""):
        """发送错误响应"""
        self.send_response(500)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        error_response = {
            "jsonrpc": "2.0",
            "error": {
                "code": -32603,
                "message": message,
                "data": details
            }
        }
        self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def do_OPTIONS(self):
        """处理CORS预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """处理GET请求，返回服务信息"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        info = {
            "service": "wechat_send MCP Server",
            "protocol": "MCP over HTTP",
            "version": "1.0.0",
            "endpoints": {
                "POST /": "MCP JSON-RPC 2.0 endpoint"
            }
        }
        self.wfile.write(json.dumps(info, ensure_ascii=False, indent=2).encode('utf-8'))


def run_mcp_server(port=8001):
    """启动MCP HTTP服务器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MCPHTTPHandler)
    print(f"MCP HTTP Server running on http://localhost:{port}")
    print("MCP Protocol: JSON-RPC 2.0 over HTTP")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()


if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', sys.argv[1] if len(sys.argv) > 1 else 8001))
    run_mcp_server(port)