#!/bin/bash
# 部署前准备脚本

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║           部署前准备检查脚本                                      ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# 检查是否在项目根目录
if [ ! -d "frontend" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

cd frontend

echo "📦 检查依赖..."
if [ ! -d "node_modules" ]; then
    echo "   安装依赖..."
    npm install
else
    echo "   ✅ 依赖已安装"
fi

echo ""
echo "📁 检查数据文件..."
if [ ! -d "public/data" ]; then
    echo "   ⚠️  public/data 目录不存在，创建中..."
    mkdir -p public/data
fi

# 检查数据文件是否完整
data_count=$(find public/data -name "*.json" 2>/dev/null | wc -l | tr -d ' ')
if [ "$data_count" -lt 10 ]; then
    echo "   ⚠️  数据文件可能不完整（当前: $data_count 个文件）"
    echo "   建议从根目录复制: cp -r ../data/* public/data/"
else
    echo "   ✅ 数据文件完整（$data_count 个文件）"
fi

echo ""
echo "🔨 测试构建..."
if npm run build > /tmp/build.log 2>&1; then
    echo "   ✅ 构建成功！"
    echo ""
    echo "═══════════════════════════════════════════════════════════════════"
    echo "✅ 项目已准备好部署！"
    echo ""
    echo "📝 下一步："
    echo "   1. 提交代码到 GitHub:"
    echo "      git add ."
    echo "      git commit -m '准备部署'"
    echo "      git push origin main"
    echo ""
    echo "   2. 访问 https://vercel.com 并部署"
    echo "   3. 或查看 DEPLOYMENT_GUIDE.md 了解详细步骤"
    echo "═══════════════════════════════════════════════════════════════════"
else
    echo "   ❌ 构建失败！"
    echo ""
    echo "   查看错误日志:"
    tail -20 /tmp/build.log
    echo ""
    echo "   请修复错误后重试"
    exit 1
fi

