#!/bin/bash
# GitHub Pages 自动化部署脚本

echo "🚀 开始部署到GitHub Pages..."
echo "=================================================="

# 检查Git是否安装
if ! command -v git &> /dev/null; then
    echo "❌ Git未安装，请先安装Git"
    exit 1
fi

# 检查当前目录
if [ ! -f "cloud_nodes_map_v3.html" ]; then
    echo "❌ 未找到 cloud_nodes_map_v3.html 文件"
    echo "请确保在正确的目录中运行此脚本"
    exit 1
fi

# 创建部署目录
DEPLOY_DIR="cloud-nodes-map-deploy"
if [ -d "$DEPLOY_DIR" ]; then
    echo "🗑️  清理旧的部署目录..."
    rm -rf "$DEPLOY_DIR"
fi

echo "📁 创建部署目录..."
mkdir "$DEPLOY_DIR"
cd "$DEPLOY_DIR"

# 复制文件
echo "📋 复制文件..."
cp ../cloud_nodes_map_v3.html index.html
if [ -d "../output" ]; then
    cp -r ../output/ .
fi

# 创建README
echo "📝 创建README文件..."
cat > README.md << 'EOF'
# 云服务提供商全球节点地图

这是一个展示阿里云、华为云、腾讯云全球节点布局的交互式地图。

## 🌍 访问地址
https://YOUR_USERNAME.github.io/cloud-nodes-map/

## ✨ 功能特性
- 🌍 全球节点分布地图
- 📊 实时统计信息
- 🎯 按云服务提供商筛选
- 📱 响应式设计
- 🗺️ 交互式地图操作

## 🛠️ 技术栈
- HTML5 + CSS3 + JavaScript
- Leaflet.js 地图库
- OpenStreetMap 地图数据
- 响应式设计

## 📊 数据来源
- 阿里云官方API
- 华为云官方API
- 腾讯云官方API

## 🔄 更新频率
数据基于官方API实时获取，定期更新。

## 📄 许可证
MIT License
EOF

# 创建.gitignore
echo "📄 创建.gitignore文件..."
cat > .gitignore << 'EOF'
# 系统文件
.DS_Store
Thumbs.db

# 编辑器文件
.vscode/
.idea/
*.swp
*.swo

# 日志文件
*.log

# 临时文件
*.tmp
*.temp
EOF

# 初始化Git
echo "🔧 初始化Git仓库..."
git init
git add .
git commit -m "Initial commit: Deploy cloud nodes map"

echo ""
echo "✅ 部署文件准备完成！"
echo "=================================================="
echo "📝 接下来请按照以下步骤完成部署："
echo ""
echo "1️⃣  在GitHub创建新仓库："
echo "   - 访问 https://github.com"
echo "   - 点击 'New repository'"
echo "   - 仓库名：cloud-nodes-map"
echo "   - 选择 'Public'"
echo "   - 不要初始化README"
echo ""
echo "2️⃣  添加远程仓库并推送："
echo "   git remote add origin https://github.com/YOUR_USERNAME/cloud-nodes-map.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3️⃣  启用GitHub Pages："
echo "   - 进入GitHub仓库页面"
echo "   - 点击 'Settings' 标签"
echo "   - 左侧菜单找到 'Pages'"
echo "   - Source选择 'Deploy from a branch'"
echo "   - Branch选择 'main'，文件夹选择 '/ (root)'"
echo "   - 点击 'Save'"
echo ""
echo "4️⃣  访问网站："
echo "   几分钟后，您的网站将在以下地址可用："
echo "   https://YOUR_USERNAME.github.io/cloud-nodes-map/"
echo ""
echo "🔗 快速链接："
echo "   - GitHub: https://github.com"
echo "   - 创建仓库: https://github.com/new"
echo ""
echo "💡 提示："
echo "   - 记得将 YOUR_USERNAME 替换为您的GitHub用户名"
echo "   - 部署完成后，每次更新只需运行 git push 即可"
echo "   - 可以在GitHub仓库的Actions中查看部署状态" 