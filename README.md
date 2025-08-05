# 云服务提供商全球节点地图

这是一个展示阿里云、华为云、腾讯云全球节点布局的交互式地图。

## 🌍 功能特性
- 全球节点分布地图
- 实时统计信息
- 按云服务提供商筛选
- 响应式设计
- 交互式地图操作
- 动态数据加载

## 🛠️ 技术栈
- HTML5 + CSS3 + JavaScript
- Leaflet.js 地图库
- OpenStreetMap 地图数据
- Vercel 部署平台

## 📊 数据来源
- 阿里云官方API (`aliyun_nodes_complete.json`)
- 华为云官方API (`huaweicloud_nodes_complete.json`)
- 腾讯云官方API (`tencentcloud_nodes_complete.json`)

## 🔄 更新频率
数据基于官方API实时获取，定期更新。

## 🚀 部署到 Vercel

### 方法一：通过 Vercel CLI
```bash
# 安装 Vercel CLI
npm i -g vercel

# 登录 Vercel
vercel login

# 部署项目
vercel

# 生产环境部署
vercel --prod
```

### 方法二：通过 GitHub 集成
1. 将代码推送到 GitHub 仓库
2. 在 [Vercel Dashboard](https://vercel.com/dashboard) 中导入项目
3. 选择 GitHub 仓库
4. 配置部署设置（可选）
5. 点击 "Deploy"

### 方法三：直接拖拽部署
1. 访问 [Vercel](https://vercel.com)
2. 登录或注册账户
3. 点击 "New Project"
4. 选择 "Upload" 选项
5. 拖拽项目文件夹到上传区域
6. 等待部署完成

## 📁 项目结构
```
cloud-nodes-map/
├── index.html                 # 主页面
├── aliyun_nodes_complete.json # 阿里云节点数据
├── huaweicloud_nodes_complete.json # 华为云节点数据
├── tencentcloud_nodes_complete.json # 腾讯云节点数据
├── vercel.json               # Vercel 配置文件
├── package.json              # 项目配置文件
└── README.md                 # 项目说明
```

## ⚙️ 配置说明

### vercel.json 配置
- **版本**: 使用 Vercel 2.0 配置
- **构建**: 静态文件构建
- **路由**: 所有请求重定向到 index.html
- **缓存**: JSON 文件缓存 1 小时，HTML 文件不缓存
- **安全**: 添加了基本的安全头
- **区域**: 部署到香港、东京、悉尼区域

### 数据更新
当 JSON 文件更新时，网站会自动反映最新数据。如果 JSON 文件加载失败，会使用默认数据作为备选。

## 🌐 访问地址
部署完成后，Vercel 会提供一个类似 `https://your-project.vercel.app` 的访问地址。

## 🔧 本地开发
```bash
# 安装依赖
npm install

# 压缩 JSON 文件（优化加载速度）
npm run compress

# 启动本地服务器
npm run dev

# 或使用 serve
npx serve .
```

## ⚡ 性能优化

### 已实施的优化措施：
1. **资源预加载**: 预加载 Leaflet CSS 和 JS 文件
2. **DNS 预解析**: 预解析外部域名，减少 DNS 查询时间
3. **异步加载**: 使用 defer 属性异步加载 JavaScript
4. **JSON 压缩**: 压缩 JSON 文件减少 28-32% 的文件大小
5. **缓存优化**: 配置了多层缓存策略
6. **地图瓦片优化**: 优化地图瓦片加载参数
7. **加载指示器**: 提供用户友好的加载反馈
8. **错误处理**: 完善的错误处理和降级方案

### 性能监控：
- 在浏览器控制台可以看到详细的加载时间信息
- 使用 `npm run compress` 可以重新压缩 JSON 文件

## 📝 更新日志
- **2025-08-04**: 初始版本发布
- **2025-08-04**: 优化 Vercel 部署配置
- **2025-08-04**: 添加动态数据加载功能

## 🤝 贡献
欢迎提交 Issue 和 Pull Request！

## 📄 许可证
MIT License
