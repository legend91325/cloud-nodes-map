# 监控和维护统计指南 📊

本指南介绍如何为网站配置监控和统计功能，帮助了解网站访问情况、性能指标和用户行为。

---

## 📋 监控方案概览

### 1. Google Analytics 4 (GA4) ✅ 已集成

**功能**:
- 📊 访问统计（PV、UV、会话数）
- 👥 用户分析（地理位置、设备类型、浏览器）
- 📈 流量来源分析
- 🎯 自定义事件追踪
- 📱 移动端分析

**优势**:
- ✅ 完全免费
- ✅ 功能强大
- ✅ 数据保留 14 个月（免费版）
- ✅ 实时数据

### 2. Vercel Analytics ✅ 已集成

**功能**:
- 📊 Web Analytics（访问统计）
- ⚡ Speed Insights（性能监控）
- 🚀 自动集成，无需配置

**优势**:
- ✅ 完全免费（Vercel 项目）
- ✅ 零配置
- ✅ 实时性能数据
- ✅ 与 Vercel 部署深度集成

---

## 🚀 快速开始

### 📍 本地调试（开发环境）

**重要**: 你可以在本地开发环境中验证和调试 Analytics 功能！

📖 **详细本地调试指南**: [LOCAL_DEBUG_GUIDE.md](LOCAL_DEBUG_GUIDE.md)

**快速步骤**:
1. 创建 `frontend/.env.local` 文件，添加你的 GA ID
2. 启动开发服务器：`npm run dev`
3. 打开浏览器控制台（F12），会自动显示调试面板
4. 使用调试命令验证功能

### 步骤 1: 配置 Google Analytics 4

#### 1.1 创建 GA4 属性

1. 访问 [Google Analytics](https://analytics.google.com/)
2. 登录你的 Google 账号
3. 点击 "管理" → "创建属性"
4. 填写属性名称（如：`cloudnorth.cloud`）
5. 选择时区和货币
6. 点击 "下一步" → "创建"

#### 1.2 获取测量 ID

1. 在 GA4 中，进入 "管理" → "数据流"
2. 点击 "网站" 数据流
3. 复制 **测量 ID**（格式：`G-XXXXXXXXXX`）

#### 1.3 配置环境变量

**在 Vercel 中配置**:

1. 进入 Vercel Dashboard → 你的项目
2. 点击 "Settings" → "Environment Variables"
3. 添加生产环境变量：
   - **Name**: `NEXT_PUBLIC_GA_ID`
   - **Value**: `G-73C89GPMYBVERCEL`（生产环境 GA ID）
   - **Environment**: **只选择 Production**（重要！）
4. 点击 "Save"

**可选**: 如果需要为不同环境配置不同的 GA ID：
- **Preview 环境**: 可以单独配置（通常使用生产环境的 GA ID）
- **Development 环境**: 可以单独配置（通常使用本地开发环境的 GA ID `G-73C89GPVERCEL`）

**本地开发配置**:

1. 在 `frontend/` 目录下创建 `.env.local` 文件：
   ```bash
   cd frontend
   cp .env.example .env.local
   ```

2. 编辑 `.env.local`，添加本地开发环境的 GA ID：
   ```env
   NEXT_PUBLIC_GA_ID=G-73C89GPVERCEL
   NEXT_PUBLIC_ANALYTICS_DEBUG=true
   ```

3. 重启开发服务器：
   ```bash
   npm run dev
   ```

**注意**: 本地开发环境使用 `G-73C89GPVERCEL`，生产环境使用 `G-73C89GPMYBVERCEL`，这样可以区分不同环境的访问数据。

### 步骤 2: 启用 Vercel Analytics

1. 进入 Vercel Dashboard → 你的项目
2. 点击 "Settings" → "Analytics"
3. 启用 **Web Analytics**
4. 启用 **Speed Insights**（可选，推荐）

**注意**: Vercel Analytics 会自动工作，无需额外配置！

---

## 📊 查看统计数据

### Google Analytics 4

1. 访问 [Google Analytics](https://analytics.google.com/)
2. 选择你的属性
3. 查看报告：
   - **实时**: 当前在线用户
   - **概览**: 访问量、用户数、会话数
   - **流量获取**: 流量来源分析
   - **参与度**: 页面浏览量、平均会话时长
   - **受众特征**: 用户地理位置、设备类型

### Vercel Analytics

1. 进入 Vercel Dashboard → 你的项目
2. 点击 "Analytics" 标签
3. 查看：
   - **Web Analytics**: 访问统计、热门页面
   - **Speed Insights**: 性能指标、Core Web Vitals

---

## 🎯 自定义事件追踪

项目已集成自定义事件追踪功能，可以在代码中使用：

### 使用示例

```typescript
import { trackEvent, trackNodeView, trackChartInteraction, trackFilter } from '@/components/Analytics';

// 追踪节点查看
trackNodeView('aws', 'us-east-1');

// 追踪图表交互
trackChartInteraction('MapChart', 'zoom');

// 追踪筛选操作
trackFilter('aws', 'North America');

// 自定义事件
trackEvent('download', 'Data', 'nodes.json', 1);
```

### 已集成的事件

- ✅ 页面浏览（自动）
- 📍 节点查看（可在 NodesTable 中添加）
- 📊 图表交互（可在图表组件中添加）
- 🔍 筛选操作（可在筛选组件中添加）

---

## 🔧 高级配置

### 禁用 Analytics（开发环境）

在 `frontend/.env.local` 中不设置 `NEXT_PUBLIC_GA_ID`，或设置为空字符串。

### 仅在生产环境启用

在 Vercel 环境变量中，只设置 Production 环境的值。

### 隐私保护

Google Analytics 4 默认符合 GDPR 要求。如需更严格的隐私保护：

1. 在 GA4 中启用 IP 匿名化
2. 配置 Cookie 同意横幅（可选）
3. 使用 Google Tag Manager 管理（高级）

---

## 📈 性能监控

### Vercel Speed Insights

自动监控以下指标：

- **LCP** (Largest Contentful Paint): 最大内容绘制时间
- **FID** (First Input Delay): 首次输入延迟
- **CLS** (Cumulative Layout Shift): 累积布局偏移
- **TTFB** (Time to First Byte): 首字节时间

### 查看性能报告

1. Vercel Dashboard → 项目 → Analytics → Speed Insights
2. 查看实时性能数据
3. 识别性能瓶颈

---

## 🐛 错误监控（可选）

### 推荐方案：Sentry

如果需要错误监控，可以集成 Sentry：

1. 安装 Sentry：
   ```bash
   npm install @sentry/nextjs
   ```

2. 初始化 Sentry（参考 [Sentry Next.js 文档](https://docs.sentry.io/platforms/javascript/guides/nextjs/)）

3. 配置错误追踪

**注意**: Sentry 免费版有使用限制，对于初创项目，Vercel 的日志功能通常足够。

---

## 📝 维护检查清单

### 每日检查（可选）

- [ ] 查看 Vercel Analytics 实时访问数据
- [ ] 检查部署状态（Vercel Dashboard）

### 每周检查

- [ ] 查看 Google Analytics 周报
- [ ] 检查性能指标（Speed Insights）
- [ ] 查看错误日志（如有）

### 每月检查

- [ ] 分析流量趋势
- [ ] 检查热门页面
- [ ] 优化性能瓶颈
- [ ] 更新依赖包

---

## 🆘 常见问题

### Q1: Google Analytics 没有数据？

**检查**:
1. 确认 `NEXT_PUBLIC_GA_ID` 环境变量已正确设置
2. 确认已部署到生产环境（本地开发可能看不到实时数据）
3. 等待 24-48 小时（GA4 数据有延迟）
4. 使用 GA4 DebugView 检查事件是否发送

### Q2: Vercel Analytics 没有数据？

**检查**:
1. 确认已在 Vercel Dashboard 中启用 Analytics
2. 等待几分钟（数据有延迟）
3. 确认网站有实际访问（测试访问不算）

### Q3: 如何测试事件追踪？

**方法**:
1. 使用 Google Analytics DebugView（实时查看事件）
2. 使用浏览器开发者工具 Network 标签，查看对 `google-analytics.com` 的请求
3. 使用 GA4 实时报告

### Q4: 数据隐私合规？

**建议**:
1. 在网站添加隐私政策页面
2. 说明使用的分析工具
3. 提供 Cookie 同意选项（如需要）
4. 配置 GA4 IP 匿名化

---

## 📚 相关资源

- [Google Analytics 4 文档](https://developers.google.com/analytics/devguides/collection/ga4)
- [Vercel Analytics 文档](https://vercel.com/docs/analytics)
- [Vercel Speed Insights 文档](https://vercel.com/docs/speed-insights)
- [Next.js Analytics 最佳实践](https://nextjs.org/docs/app/building-your-application/optimizing/analytics)

---

## ✅ 配置完成检查

- [ ] Google Analytics 4 测量 ID 已配置
- [ ] Vercel Analytics 已启用
- [ ] 环境变量已设置（Vercel + 本地）
- [ ] 已测试事件追踪（可选）
- [ ] 已查看初始统计数据

**完成以上步骤后，你的网站监控系统就配置好了！** 🎉

