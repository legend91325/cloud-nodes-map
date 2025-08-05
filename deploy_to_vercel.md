# 🚀 Vercel 部署指南 - 云服务提供商全球节点地图

## 方案优势

### ✨ Vercel 特点
- **完全免费**：个人项目免费托管
- **自动部署**：连接Git仓库，自动部署
- **全球CDN**：访问速度快
- **HTTPS**：自动配置SSL证书
- **自定义域名**：支持绑定自己的域名
- **实时预览**：每次提交都有预览链接

## 部署步骤

### 步骤1：准备项目文件

```bash
# 创建vercel项目目录
mkdir cloud-nodes-map-vercel
cd cloud-nodes-map-vercel

# 复制主文件
cp ../cloud_nodes_map_v3.html index.html

# 复制数据文件（可选）
cp -r ../output/ .

# 创建vercel.json配置文件
cat > vercel.json << 'EOF'
{
  "version": 2,
  "name": "cloud-nodes-map",
  "builds": [
    {
      "src": "*.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=3600"
        }
      ]
    }
  ]
}
EOF

# 创建README
cat > README.md << 'EOF'
# 云服务提供商全球节点地图

这是一个展示阿里云、华为云、腾讯云全球节点布局的交互式地图。

## 🌍 功能特性
- 全球节点分布地图
- 实时统计信息
- 按云服务提供商筛选
- 响应式设计
- 交互式地图操作

## 🛠️ 技术栈
- HTML5 + CSS3 + JavaScript
- Leaflet.js 地图库
- OpenStreetMap 地图数据

## 📊 数据来源
- 阿里云官方API
- 华为云官方API
- 腾讯云官方API
EOF
```

### 步骤2：创建GitHub仓库

1. 访问 [GitHub](https://github.com)
2. 点击 "New repository"
3. 仓库名：`cloud-nodes-map`
4. 选择 "Public"
5. 不要初始化README

### 步骤3：上传到GitHub

```bash
# 初始化Git
git init
git add .
git commit -m "Initial commit: Cloud nodes map for Vercel"

# 添加远程仓库（替换YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/cloud-nodes-map.git
git branch -M main
git push -u origin main
```

### 步骤4：部署到Vercel

1. 访问 [Vercel](https://vercel.com)
2. 使用GitHub账号登录
3. 点击 "New Project"
4. 选择您刚创建的GitHub仓库 `cloud-nodes-map`
5. 保持默认设置，点击 "Deploy"

### 步骤5：访问网站

部署完成后，Vercel会自动生成一个域名，类似：
```
https://cloud-nodes-map-xxxxx.vercel.app
```

## 自动化部署脚本

### 创建Vercel部署脚本

```bash
#!/bin/bash
# deploy_to_vercel.sh

echo "🚀 开始部署到Vercel..."
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

# 创建Vercel项目目录
VERCEL_DIR="cloud-nodes-map-vercel"
if [ -d "$VERCEL_DIR" ]; then
    echo "🗑️  清理旧的Vercel目录..."
    rm -rf "$VERCEL_DIR"
fi

echo "📁 创建Vercel项目目录..."
mkdir "$VERCEL_DIR"
cd "$VERCEL_DIR"

# 复制文件
echo "📋 复制文件..."
cp ../cloud_nodes_map_v3.html index.html
if [ -d "../output" ]; then
    cp -r ../output/ .
fi

# 创建vercel.json
echo "⚙️  创建Vercel配置文件..."
cat > vercel.json << 'EOF'
{
  "version": 2,
  "name": "cloud-nodes-map",
  "builds": [
    {
      "src": "*.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=3600"
        }
      ]
    }
  ]
}
EOF

# 创建README
echo "📝 创建README文件..."
cat > README.md << 'EOF'
# 云服务提供商全球节点地图

这是一个展示阿里云、华为云、腾讯云全球节点布局的交互式地图。

## 🌍 功能特性
- 全球节点分布地图
- 实时统计信息
- 按云服务提供商筛选
- 响应式设计
- 交互式地图操作

## 🛠️ 技术栈
- HTML5 + CSS3 + JavaScript
- Leaflet.js 地图库
- OpenStreetMap 地图数据

## 📊 数据来源
- 阿里云官方API
- 华为云官方API
- 腾讯云官方API

## 🔄 更新频率
数据基于官方API实时获取，定期更新。
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

# Vercel
.vercel
EOF

# 初始化Git
echo "🔧 初始化Git仓库..."
git init
git add .
git commit -m "Initial commit: Deploy to Vercel"

echo ""
echo "✅ Vercel项目准备完成！"
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
echo "3️⃣  部署到Vercel："
echo "   - 访问 https://vercel.com"
echo "   - 使用GitHub账号登录"
echo "   - 点击 'New Project'"
echo "   - 选择您的GitHub仓库"
echo "   - 点击 'Deploy'"
echo ""
echo "4️⃣  访问网站："
echo "   部署完成后，Vercel会自动生成访问链接"
echo ""
echo "🔗 快速链接："
echo "   - GitHub: https://github.com"
echo "   - Vercel: https://vercel.com"
echo ""
echo "💡 提示："
echo "   - 记得将 YOUR_USERNAME 替换为您的GitHub用户名"
echo "   - 部署完成后，每次更新只需运行 git push 即可"
echo "   - Vercel会自动重新部署"
```

## 自定义域名配置

### 在Vercel中添加自定义域名

1. 登录Vercel控制台
2. 选择您的项目
3. 点击 "Settings" 标签
4. 找到 "Domains" 部分
5. 点击 "Add Domain"
6. 输入您的域名
7. 按照提示配置DNS记录

### DNS配置示例

```
类型: CNAME
名称: www
值: cname.vercel-dns.com
```

## 环境变量配置（可选）

如果需要配置环境变量，可以在Vercel项目设置中添加：

```bash
# 在vercel.json中添加环境变量
{
  "env": {
    "API_KEY": "your-api-key"
  }
}
```

## 性能优化

### 1. 启用压缩

Vercel会自动启用Gzip压缩，无需额外配置。

### 2. 缓存策略

在vercel.json中配置缓存头：

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=3600, s-maxage=86400"
        }
      ]
    }
  ]
}
```

### 3. 图片优化

Vercel支持自动图片优化，可以添加图片优化配置：

```json
{
  "images": {
    "sizes": [640, 750, 828, 1080, 1200],
    "domains": ["example.com"]
  }
}
```

## 监控和分析

### 1. Vercel Analytics

在项目设置中启用Vercel Analytics：

```json
{
  "analytics": {
    "enabled": true
  }
}
```

### 2. 自定义分析

添加Google Analytics：

```html
<!-- 在HTML头部添加 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## 更新部署

### 自动更新

每次推送到GitHub，Vercel会自动重新部署：

```bash
# 修改文件后
git add .
git commit -m "Update map data"
git push origin main
```

### 手动部署

也可以使用Vercel CLI进行手动部署：

```bash
# 安装Vercel CLI
npm i -g vercel

# 登录Vercel
vercel login

# 部署
vercel

# 生产环境部署
vercel --prod
```

## 故障排除

### 常见问题

1. **部署失败**
   - 检查vercel.json配置
   - 查看部署日志

2. **页面无法访问**
   - 检查域名配置
   - 确认DNS记录正确

3. **地图不显示**
   - 检查网络连接
   - 确认Leaflet.js加载正常

### 调试工具

- Vercel部署日志
- 浏览器开发者工具
- Vercel CLI调试命令

---

Vercel是一个非常优秀的部署平台，特别适合静态网站。部署完成后，您就可以通过互联网访问您的云服务提供商全球节点地图了！ 