#!/bin/bash
# 部署前准备脚本 - 执行所有必要的检查和准备

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║           部署前准备脚本                                          ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# 检查是否在项目根目录
if [ ! -d "frontend" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 1. 同步数据文件
echo "📁 步骤 1/4: 同步数据文件..."
bash scripts/sync-data.sh
if [ $? -ne 0 ]; then
    echo "❌ 数据文件同步失败"
    exit 1
fi
echo ""

# 2. 检查依赖
echo "📦 步骤 2/4: 检查依赖..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "   安装依赖..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
else
    echo "   ✅ 依赖已安装"
fi
cd ..
echo ""

# 3. 测试构建
echo "🔨 步骤 3/4: 测试构建..."
cd frontend
if npm run build > /tmp/build.log 2>&1; then
    echo "   ✅ 构建成功！"
else
    echo "   ❌ 构建失败！"
    echo ""
    echo "   错误日志:"
    tail -30 /tmp/build.log
    cd ..
    exit 1
fi
cd ..
echo ""

# 4. 检查 Git 状态
echo "📝 步骤 4/4: 检查 Git 状态..."
if [ -d ".git" ]; then
    if [ -n "$(git status --porcelain)" ]; then
        echo "   ⚠️  有未提交的更改:"
        git status --short
        echo ""
        echo "   💡 建议提交更改后再部署:"
        echo "      git add ."
        echo "      git commit -m '准备部署'"
        echo "      git push origin main"
    else
        echo "   ✅ 所有更改已提交"
    fi
else
    echo "   ⚠️  未检测到 Git 仓库"
    echo "   💡 建议初始化 Git 仓库并推送到 GitHub"
fi
echo ""

echo "═══════════════════════════════════════════════════════════════════"
echo "✅ 部署前准备完成！"
echo ""
echo "📋 下一步:"
echo "   1. 确保代码已推送到 GitHub"
echo "   2. 访问 https://vercel.com"
echo "   3. 导入项目，设置 Root Directory 为 'frontend'"
echo "   4. 点击部署"
echo ""
echo "📖 详细步骤请查看: DEPLOYMENT_GUIDE.md"
echo "═══════════════════════════════════════════════════════════════════"

