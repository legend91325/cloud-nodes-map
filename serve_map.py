#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云服务提供商全球节点地图服务器
启动一个简单的HTTP服务器来展示地图页面
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

def start_server(port=8000):
    """启动HTTP服务器"""
    
    # 获取当前目录
    current_dir = Path(__file__).parent.absolute()
    
    # 切换到当前目录
    os.chdir(current_dir)
    
    # 检查地图文件是否存在
    map_file = current_dir / "cloud_nodes_map_v3.html"
    if not map_file.exists():
        print("❌ 错误: cloud_nodes_map_v3.html 文件不存在")
        return False
    
    # 创建HTTP服务器
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"🌐 服务器已启动在端口 {port}")
            print(f"📁 服务目录: {current_dir}")
            print(f"🔗 访问地址: http://localhost:{port}/cloud_nodes_map_v3.html")
            print("💡 按 Ctrl+C 停止服务器")
            print("-" * 50)
            
            # 自动打开浏览器
            try:
                webbrowser.open(f"http://localhost:{port}/cloud_nodes_map_v3.html")
                print("✅ 已自动打开浏览器")
            except Exception as e:
                print(f"⚠️  无法自动打开浏览器: {e}")
                print("请手动访问: http://localhost:8000/cloud_nodes_map_v3.html")
            
            # 启动服务器
            httpd.serve_forever()
            
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ 端口 {port} 已被占用，请尝试其他端口")
            return False
        else:
            print(f"❌ 启动服务器失败: {e}")
            return False
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")
        return True

def main():
    """主函数"""
    print("🌍 云服务提供商全球节点地图服务器")
    print("=" * 50)
    
    # 检查端口参数
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ 端口号必须是数字")
            return
    
    # 启动服务器
    start_server(port)

if __name__ == "__main__":
    main() 