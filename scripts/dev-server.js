const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = process.env.PORT || 3000;

// MIME 类型映射
const mimeTypes = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon'
};

// 创建服务器
const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url);
    let pathname = parsedUrl.pathname;
    
    // 默认页面
    if (pathname === '/') {
        pathname = '/index.html';
    }
    
    // 获取文件路径
    const filePath = path.join(__dirname, '..', pathname);
    const extname = path.extname(filePath);
    
    // 设置 CORS 头
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    
    // 设置缓存头
    if (extname === '.json') {
        res.setHeader('Cache-Control', 'public, max-age=3600');
    } else if (extname === '.html') {
        res.setHeader('Cache-Control', 'no-cache');
    } else {
        res.setHeader('Cache-Control', 'public, max-age=31536000');
    }
    
    // 处理 OPTIONS 请求
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    // 读取文件
    fs.readFile(filePath, (err, data) => {
        if (err) {
            if (err.code === 'ENOENT') {
                // 文件不存在，返回 404
                res.writeHead(404, { 'Content-Type': 'text/html' });
                res.end('<h1>404 - 文件未找到</h1>');
            } else {
                // 其他错误
                res.writeHead(500, { 'Content-Type': 'text/html' });
                res.end('<h1>500 - 服务器内部错误</h1>');
            }
            return;
        }
        
        // 设置正确的 MIME 类型
        const contentType = mimeTypes[extname] || 'application/octet-stream';
        res.setHeader('Content-Type', contentType);
        
        // 返回文件内容
        res.writeHead(200);
        res.end(data);
    });
});

// 启动服务器
server.listen(PORT, () => {
    console.log(`🚀 本地开发服务器启动成功！`);
    console.log(`📱 访问地址: http://localhost:${PORT}`);
    console.log(`🌐 网络地址: http://0.0.0.0:${PORT}`);
    console.log(`\n📋 服务器信息:`);
    console.log(`   - 端口: ${PORT}`);
    console.log(`   - 工作目录: ${process.cwd()}`);
    console.log(`   - 支持的文件类型: ${Object.keys(mimeTypes).join(', ')}`);
    console.log(`\n💡 提示:`);
    console.log(`   - 按 Ctrl+C 停止服务器`);
    console.log(`   - 修改文件后刷新浏览器即可看到更新`);
});

// 优雅关闭
process.on('SIGINT', () => {
    console.log('\n👋 正在关闭服务器...');
    server.close(() => {
        console.log('✅ 服务器已关闭');
        process.exit(0);
    });
}); 