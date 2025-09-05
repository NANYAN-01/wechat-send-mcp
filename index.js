#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

// 获取当前脚本所在目录
const scriptDir = __dirname;

// 构建 Python 命令
const pythonArgs = ['-m', 'wechat_send'];

// 如果有命令行参数，添加到 Python 参数中
if (process.argv.length > 2) {
    pythonArgs.push(...process.argv.slice(2));
}

console.log('Starting wechat_send MCP service...');
console.log('Command:', 'python', pythonArgs.join(' '));

// 启动 Python 进程
const pythonProcess = spawn('python', pythonArgs, {
    cwd: scriptDir,
    stdio: 'inherit'
});

// 处理进程退出
pythonProcess.on('close', (code) => {
    process.exit(code);
});

pythonProcess.on('error', (err) => {
    console.error('Failed to start Python process:', err);
    process.exit(1);
});
