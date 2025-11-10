#!/bin/bash
# 数据文件同步脚本 - 确保 frontend/public/data 与 data 目录同步

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║           数据文件同步脚本                                        ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# 检查是否在项目根目录
if [ ! -d "data" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 确保 frontend/public/data 目录存在
mkdir -p frontend/public/data

echo "📁 同步数据文件..."
echo "   从: data/"
echo "   到: frontend/public/data/"
echo ""

# 同步所有数据文件
rsync -av --delete \
  --exclude='*.bak' \
  --exclude='.DS_Store' \
  data/ frontend/public/data/

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 数据文件同步完成！"
    echo ""
    
    # 统计文件数量
    file_count=$(find frontend/public/data -name "*.json" | wc -l | tr -d ' ')
    echo "📊 统计: 共 $file_count 个 JSON 文件"
    echo ""
    
    # 列出所有云服务商
    echo "📋 已同步的云服务商:"
    for dir in frontend/public/data/*/; do
        if [ -d "$dir" ]; then
            provider=$(basename "$dir")
            node_count=$(find "$dir" -name "nodes.json" -exec cat {} \; | grep -o '"node_id"' | wc -l | tr -d ' ')
            echo "   - $provider ($node_count 个节点)"
        fi
    done
    
    echo ""
    echo "💡 提示: 在提交代码前运行此脚本，确保数据文件是最新的"
else
    echo ""
    echo "❌ 同步失败，请检查错误信息"
    exit 1
fi

