# 🌐 云服务提供商全球节点地图 - 部署指南

## 方案1：GitHub Pages 部署（推荐）

### 步骤1：准备文件
```bash
# 创建部署目录
mkdir cloud-nodes-map-deploy
cd cloud-nodes-map-deploy

# 复制必要文件
cp cloud_nodes_map_v3.html index.html
cp -r output/ .
```

### 步骤2：创建GitHub仓库
1. 访问 [GitHub](https://github.com)
2. 点击 "New repository"
3. 仓库名：`cloud-nodes-map`
4. 选择 "Public"
5. 不要初始化README

### 步骤3：上传文件
```bash
# 初始化Git仓库
git init
git add .
git commit -m "Initial commit: Cloud nodes map"

# 添加远程仓库（替换YOUR_USERNAME为您的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/cloud-nodes-map.git
git branch -M main
git push -u origin main
```

### 步骤4：启用GitHub Pages
1. 进入GitHub仓库页面
2. 点击 "Settings" 标签
3. 左侧菜单找到 "Pages"
4. Source选择 "Deploy from a branch"
5. Branch选择 "main"，文件夹选择 "/ (root)"
6. 点击 "Save"

### 步骤5：访问网站
几分钟后，您的网站将在以下地址可用：
```
https://YOUR_USERNAME.github.io/cloud-nodes-map/
```

## 方案2：Vercel 部署

### 步骤1：准备项目
```bash
# 创建vercel.json配置文件
cat > vercel.json << EOF
{
  "version": 2,
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
  ]
}
EOF
```

### 步骤2：部署到Vercel
1. 访问 [Vercel](https://vercel.com)
2. 使用GitHub账号登录
3. 点击 "New Project"
4. 导入您的GitHub仓库
5. 点击 "Deploy"

## 方案3：Netlify 部署

### 步骤1：准备文件
```bash
# 创建netlify.toml配置文件
cat > netlify.toml << EOF
[build]
  publish = "."
  command = ""

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
EOF
```

### 步骤2：部署到Netlify
1. 访问 [Netlify](https://netlify.com)
2. 使用GitHub账号登录
3. 点击 "New site from Git"
4. 选择您的GitHub仓库
5. 点击 "Deploy site"

## 方案4：阿里云OSS部署

### 步骤1：创建OSS Bucket
1. 登录阿里云控制台
2. 创建OSS Bucket
3. 设置Bucket为公共读

### 步骤2：上传文件
```bash
# 安装阿里云CLI工具
pip install oss2

# 上传文件
python -c "
import oss2
auth = oss2.Auth('AccessKeyId', 'AccessKeySecret')
bucket = oss2.Bucket(auth, 'endpoint', 'bucket-name')
bucket.put_object_from_file('index.html', 'cloud_nodes_map_v3.html')
"
```

### 步骤3：配置CDN（可选）
1. 在阿里云控制台配置CDN
2. 添加自定义域名
3. 配置HTTPS证书

## 自动化部署脚本

### GitHub Pages 自动化脚本
```bash
#!/bin/bash
# deploy_github_pages.sh

echo "🚀 开始部署到GitHub Pages..."

# 检查Git是否安装
if ! command -v git &> /dev/null; then
    echo "❌ Git未安装，请先安装Git"
    exit 1
fi

# 创建部署目录
DEPLOY_DIR="cloud-nodes-map-deploy"
if [ -d "$DEPLOY_DIR" ]; then
    rm -rf "$DEPLOY_DIR"
fi
mkdir "$DEPLOY_DIR"
cd "$DEPLOY_DIR"

# 复制文件
echo "📁 复制文件..."
cp ../cloud_nodes_map_v3.html index.html
cp -r ../output/ .

# 创建README
cat > README.md << EOF
# 云服务提供商全球节点地图

这是一个展示阿里云、华为云、腾讯云全球节点布局的交互式地图。

## 访问地址
https://YOUR_USERNAME.github.io/cloud-nodes-map/

## 功能特性
- 🌍 全球节点分布地图
- 📊 实时统计信息
- 🎯 按云服务提供商筛选
- 📱 响应式设计

## 技术栈
- HTML5 + CSS3 + JavaScript
- Leaflet.js 地图库
- OpenStreetMap 地图数据
EOF

# 初始化Git
echo "🔧 初始化Git仓库..."
git init
git add .
git commit -m "Deploy cloud nodes map"

echo "✅ 部署文件准备完成！"
echo "📝 请按照以下步骤完成部署："
echo "1. 在GitHub创建新仓库"
echo "2. 运行: git remote add origin https://github.com/YOUR_USERNAME/cloud-nodes-map.git"
echo "3. 运行: git push -u origin main"
echo "4. 在GitHub仓库设置中启用Pages"
```

### 使用方法
```bash
# 给脚本执行权限
chmod +x deploy_github_pages.sh

# 运行部署脚本
./deploy_github_pages.sh
```

## 自定义域名配置

### GitHub Pages 自定义域名
1. 在GitHub仓库设置中添加自定义域名
2. 在域名提供商处添加CNAME记录
3. 等待DNS生效

### Vercel 自定义域名
1. 在Vercel项目设置中添加域名
2. 按照提示配置DNS记录
3. 自动配置SSL证书

## 性能优化建议

### 1. 图片优化
```html
<!-- 使用WebP格式 -->
<picture>
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="描述">
</picture>
```

### 2. 缓存策略
```html
<!-- 添加缓存头 -->
<meta http-equiv="Cache-Control" content="max-age=3600">
```

### 3. CDN加速
- 使用jsDelivr CDN加载Leaflet.js
- 配置图片CDN

## 监控和分析

### 1. Google Analytics
```html
<!-- 添加到HTML头部 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### 2. 访问统计
- GitHub Pages：在仓库Insights中查看
- Vercel：在Analytics中查看
- Netlify：在Analytics中查看

## 故障排除

### 常见问题
1. **页面无法访问**：检查GitHub Pages设置
2. **地图不显示**：检查网络连接和CDN
3. **样式异常**：检查CSS文件路径

### 调试工具
- 浏览器开发者工具
- GitHub Actions日志
- Vercel/Netlify部署日志

## 更新部署

### 自动更新
```bash
# 修改文件后重新部署
git add .
git commit -m "Update map data"
git push origin main
```

### 手动更新
1. 修改本地文件
2. 重新运行部署脚本
3. 推送到GitHub

---

选择最适合您需求的方案，我推荐从GitHub Pages开始，因为它免费且简单易用！ 