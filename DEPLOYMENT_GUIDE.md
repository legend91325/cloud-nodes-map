# 网站部署指南 🚀

本指南为初创者提供简单、免费或低成本的网站部署方案。

## 📋 推荐方案对比

| 平台 | 免费套餐 | 难度 | 推荐指数 | 特点 |
|------|---------|------|---------|------|
| **Vercel** | ✅ 无限 | ⭐ 极简单 | ⭐⭐⭐⭐⭐ | Next.js 官方推荐，自动部署 |
| **Netlify** | ✅ 100GB/月 | ⭐ 简单 | ⭐⭐⭐⭐ | 拖拽部署，功能丰富 |
| **Cloudflare Pages** | ✅ 无限 | ⭐⭐ 中等 | ⭐⭐⭐⭐ | 全球 CDN，速度极快 |
| **Railway** | ✅ $5/月额度 | ⭐⭐ 中等 | ⭐⭐⭐ | 简单易用，支持数据库 |
| **Render** | ✅ 有限制 | ⭐⭐ 中等 | ⭐⭐⭐ | 免费但有限制 |

---

## 🏆 方案一：Vercel（最推荐）⭐

**为什么选择 Vercel？**
- ✅ Next.js 的创建者，完美支持
- ✅ 免费套餐无限制（个人项目）
- ✅ 自动 HTTPS 和全球 CDN
- ✅ 零配置部署
- ✅ 自动预览每个 PR

### 部署步骤

#### 方法 1：通过 GitHub 自动部署（推荐）

1. **运行部署前准备脚本**
   ```bash
   # 在项目根目录运行
   bash scripts/pre-deploy.sh
   ```
   这个脚本会：
   - ✅ 同步数据文件到 `frontend/public/data/`
   - ✅ 检查并安装依赖
   - ✅ 测试构建是否成功
   - ✅ 检查 Git 状态

2. **提交代码到 GitHub**
   ```bash
   git add .
   git commit -m "准备部署到 Vercel"
   git push origin main
   ```

3. **登录 Vercel**
   - 访问 https://vercel.com
   - 使用 GitHub 账号登录（推荐）

4. **导入项目**
   - 点击 "Add New Project"
   - 选择你的 GitHub 仓库
   - Vercel 会自动检测 Next.js 项目

5. **配置项目（重要！）**
   - **Root Directory**: 设置为 `frontend` ⚠️ 必须设置！
   - **Framework Preset**: Next.js（自动检测）
   - **Build Command**: `npm run build`（默认，已配置在 vercel.json）
   - **Output Directory**: `.next`（默认，已配置在 vercel.json）
   - **Install Command**: `npm install`（默认，已配置在 vercel.json）

6. **部署**
   - 点击 "Deploy"
   - 等待 2-3 分钟
   - 获得一个 `your-project.vercel.app` 的域名

7. **配置自定义域名 `cloudnorth.cloud`**
   
   **步骤 A: 在 Vercel 中添加域名**
   - 部署完成后，进入项目 Dashboard
   - 点击 "Settings" → "Domains"
   - 在 "Add Domain" 输入框中输入：`cloudnorth.cloud`
   - 点击 "Add"
   - Vercel 会显示需要配置的 DNS 记录

   **步骤 B: 配置 DNS 记录**
   
   根据 Vercel 显示的 DNS 记录，在你的域名注册商（如 Namecheap、Cloudflare 等）配置：
   
   **方式 1: 使用 A 记录（推荐）**
   ```
   类型: A
   名称: @ (或留空，表示根域名)
   值: 76.76.21.21 (Vercel 提供的 IP，请查看 Vercel 显示的准确值)
   TTL: 3600 (或自动)
   ```
   
   **方式 2: 使用 CNAME 记录（更灵活）**
   ```
   类型: CNAME
   名称: @ (或留空)
   值: cname.vercel-dns.com (Vercel 提供的 CNAME，请查看 Vercel 显示的准确值)
   TTL: 3600 (或自动)
   ```
   
   **注意**: 某些域名注册商（如 Namecheap）不支持根域名的 CNAME，需要使用 A 记录或 ALIAS 记录。
   
   **步骤 C: 等待 DNS 生效**
   - DNS 记录通常需要 5-60 分钟生效
   - 在 Vercel 的 Domains 页面可以看到验证状态
   - 当状态变为 "Valid Configuration" 时，域名配置成功

   **步骤 D: 验证 HTTPS**
   - Vercel 会自动为你的域名配置 SSL 证书
   - 通常需要几分钟时间
   - 完成后，你的网站就可以通过 `https://cloudnorth.cloud` 访问了

   **常见问题**:
   - 如果 DNS 验证失败，检查 DNS 记录是否正确配置
   - 确保域名已解锁（不是隐私保护状态）
   - 某些注册商需要等待更长时间才能生效

#### 方法 2：通过 Vercel CLI

```bash
# 安装 Vercel CLI
npm i -g vercel

# 进入前端目录
cd frontend

# 部署
vercel

# 按照提示操作：
# - 登录 Vercel 账号
# - 选择项目设置
# - 确认部署
```

### 环境变量配置（如果需要）

如果将来需要添加环境变量：
1. 在 Vercel 项目设置中找到 "Environment Variables"
2. 添加变量
3. 重新部署

### 自动部署

- ✅ 每次推送到 `main` 分支自动部署到生产环境
- ✅ 每次 PR 自动创建预览环境
- ✅ 支持回滚到之前的版本

---

## 🥈 方案二：Netlify

**为什么选择 Netlify？**
- ✅ 免费套餐 100GB 带宽/月
- ✅ 拖拽部署，超级简单
- ✅ 自动 HTTPS
- ✅ 表单处理、函数支持

### 部署步骤

#### 方法 1：通过 GitHub 自动部署

1. **准备代码**
   ```bash
   git add .
   git commit -m "准备部署到 Netlify"
   git push origin main
   ```

2. **登录 Netlify**
   - 访问 https://www.netlify.com
   - 使用 GitHub 账号登录

3. **导入项目**
   - 点击 "Add new site" → "Import an existing project"
   - 选择 GitHub 仓库

4. **配置构建设置**
   ```
   Base directory: frontend
   Build command: npm run build
   Publish directory: frontend/.next
   ```

5. **部署**
   - 点击 "Deploy site"
   - 获得 `your-project.netlify.app` 域名

#### 方法 2：拖拽部署（最简单）

1. **构建项目**
   ```bash
   cd frontend
   npm run build
   npm run export  # 如果需要静态导出
   ```

2. **打包**
   ```bash
   # 在 frontend 目录下
   tar -czf deploy.tar.gz .next public package.json
   ```

3. **拖拽部署**
   - 访问 https://app.netlify.com/drop
   - 直接拖拽 `deploy.tar.gz` 文件
   - 自动部署完成

---

## 🥉 方案三：Cloudflare Pages

**为什么选择 Cloudflare Pages？**
- ✅ 完全免费，无限制
- ✅ 全球 CDN，速度极快
- ✅ 自动 HTTPS
- ✅ 支持预览部署

### 部署步骤

1. **准备代码**
   ```bash
   git add .
   git commit -m "准备部署到 Cloudflare Pages"
   git push origin main
   ```

2. **登录 Cloudflare**
   - 访问 https://pages.cloudflare.com
   - 使用账号登录（如果没有，先注册）

3. **创建项目**
   - 点击 "Create a project"
   - 连接 GitHub 仓库

4. **配置构建设置**
   ```
   Framework preset: Next.js
   Build command: npm run build
   Build output directory: .next
   Root directory: frontend
   ```

5. **部署**
   - 点击 "Save and Deploy"
   - 获得 `your-project.pages.dev` 域名

---

## 🔧 部署前检查清单

### 1. 确保数据文件已同步

**推荐方式：使用同步脚本**
```bash
# 在项目根目录运行
bash scripts/sync-data.sh
```

**手动方式：**
```bash
# 检查 public/data 目录是否有所有数据文件
cd frontend
ls -la public/data/

# 如果没有，从根目录复制
cp -r ../data/* public/data/
```

**注意**: 数据文件必须在 `frontend/public/data/` 目录下，因为 Next.js 会自动服务 `public` 目录下的文件。

### 2. 测试本地构建

```bash
cd frontend
npm install
npm run build

# 如果构建成功，说明可以部署
# 如果失败，先修复错误
```

### 3. 检查环境变量

```bash
# 检查是否有 .env 文件需要配置
# 如果有，需要在部署平台配置环境变量
```

### 4. 优化构建

确保 `next.config.ts` 配置正确：

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // 如果需要静态导出（某些平台需要）
  // output: 'export',
  
  // 图片优化
  images: {
    unoptimized: true, // 如果使用静态导出
  },
};

export default nextConfig;
```

---

## 📝 部署后优化

### 1. 自定义域名配置

**域名**: `cloudnorth.cloud`

📖 **详细配置指南**: [DOMAIN_SETUP.md](DOMAIN_SETUP.md)

**快速步骤**:
1. 在 Vercel Dashboard → Settings → Domains 中添加 `cloudnorth.cloud`
2. 根据 Vercel 显示的 DNS 记录，在域名注册商配置 DNS
3. 等待 DNS 生效（5-60 分钟）
4. Vercel 自动配置 SSL 证书

### 2. 性能优化

- ✅ 启用 Vercel Analytics（免费）
- ✅ 使用图片优化
- ✅ 启用压缩

### 2. 监控和日志

- **Vercel**: 内置 Analytics 和 Logs
- **Netlify**: 内置 Analytics
- **Cloudflare**: 使用 Cloudflare Analytics

### 3. 自定义域名

所有平台都支持免费自定义域名：

1. 购买域名（推荐：Namecheap, Cloudflare Registrar）
2. 在平台设置中添加域名
3. 配置 DNS 记录
4. 自动获得 SSL 证书

---

## 🆘 常见问题

### Q1: 构建失败怎么办？

**检查：**
1. 本地是否能成功构建：`npm run build`
2. 查看构建日志中的错误信息
3. 检查 Node.js 版本（推荐 18+）

### Q2: 数据文件加载失败？

**解决：**
1. 确保 `public/data/` 目录下的文件已提交到 Git
2. 检查文件路径是否正确
3. 使用相对路径：`/data/xxx/nodes.json`

### Q3: 如何更新网站？

**方法：**
- 推送到 GitHub，自动触发部署
- 或在平台手动触发重新部署

### Q4: 如何回滚到之前的版本？

**Vercel/Netlify:**
- 在部署历史中选择之前的版本
- 点击 "Promote to Production"

### Q5: 免费套餐有限制吗？

**Vercel:**
- 个人项目：无限制
- 团队项目：有使用限制

**Netlify:**
- 100GB 带宽/月
- 300 分钟构建时间/月

**Cloudflare Pages:**
- 完全免费，无限制

---

## 🎯 推荐方案总结

### 对于初创者，我强烈推荐：

1. **首选：Vercel** ⭐⭐⭐⭐⭐
   - 最简单，最适合 Next.js
   - 零配置，自动部署
   - 免费且无限制

2. **备选：Netlify** ⭐⭐⭐⭐
   - 功能丰富
   - 拖拽部署超简单
   - 免费套餐足够用

3. **备选：Cloudflare Pages** ⭐⭐⭐⭐
   - 完全免费
   - 全球 CDN 速度快
   - 适合追求性能

---

## 📚 相关资源

- [Vercel 文档](https://vercel.com/docs)
- [Netlify 文档](https://docs.netlify.com)
- [Cloudflare Pages 文档](https://developers.cloudflare.com/pages)
- [Next.js 部署文档](https://nextjs.org/docs/deployment)

---

## 🚀 快速开始（5分钟部署）

### 使用 Vercel（最简单）

```bash
# 1. 确保代码在 GitHub
git add .
git commit -m "准备部署"
git push origin main

# 2. 访问 https://vercel.com
# 3. 用 GitHub 登录
# 4. 点击 "Add New Project"
# 5. 选择仓库，设置 Root Directory 为 "frontend"
# 6. 点击 "Deploy"
# 7. 等待 2-3 分钟，完成！
```

---

**最后更新**: 2025-01  
**维护者**: Cloud Nodes Map Project

