#!/usr/bin/env python3
"""
简单的HTTP服务器，用于本地测试云基础设施地图
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

def main():
    # 设置端口
    PORT = 8000
    
    # 切换到项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 创建HTTP服务器
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"🚀 服务器启动成功!")
            print(f"📊 访问地址: http://localhost:{PORT}/cloud-infrastructure-map.html")
            print(f"📁 服务目录: {project_root}")
            print(f"⏹️  按 Ctrl+C 停止服务器")
            print("-" * 50)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ 端口 {PORT} 已被占用，请尝试其他端口")
            print("💡 可以修改 serve.py 中的 PORT 变量")
        else:
            print(f"❌ 启动服务器失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
