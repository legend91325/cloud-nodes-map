# 本地调试 Analytics 指南 🔍

本指南介绍如何在本地开发环境中验证和调试 Analytics 功能。

---

## 🚀 快速开始

### 1. 配置环境变量

在 `frontend/` 目录下创建 `.env.local` 文件：

```bash
cd frontend
cp .env.example .env.local
```

编辑 `.env.local`：

```env
# 使用本地开发环境的 Google Analytics 测量 ID
NEXT_PUBLIC_GA_ID=G-73C89GPVERCEL

# 启用调试模式（可选）
NEXT_PUBLIC_ANALYTICS_DEBUG=true
```

**注意**: 
- 本地开发环境使用 `G-73C89GPVERCEL`
- 生产环境使用 `G-73C89GPMYBVERCEL`
- 这样可以区分不同环境的访问数据

### 2. 安装依赖并启动

```bash
cd frontend
npm install
npm run dev
```

### 3. 打开浏览器控制台

访问 `http://localhost:3000`，然后打开浏览器开发者工具（F12），在控制台中你会看到：

```
╔═══════════════════════════════════════════════════════════════════╗
║              Analytics 调试面板                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## 🔧 调试工具

### 方法 1: 使用浏览器控制台命令

在浏览器控制台中，可以使用以下命令：

```javascript
// 检查 Analytics 状态
window.__checkAnalyticsStatus()

// 启用调试模式（会在控制台输出所有事件）
window.__enableAnalyticsDebug()

// 发送测试事件
window.__testAnalyticsEvent()
```

### 方法 2: 使用 Google Analytics DebugView

1. **安装 Google Analytics Debugger 扩展**（Chrome）:
   - 访问 [Chrome Web Store](https://chrome.google.com/webstore/detail/google-analytics-debugger/jnkmfdileelhofjcijamephohjechhna)
   - 点击 "添加到 Chrome"

2. **启用 DebugView**:
   - 打开你的网站（http://localhost:3000）
   - 点击浏览器工具栏中的 GA Debugger 图标
   - 图标变红表示已启用

3. **查看实时事件**:
   - 访问 [Google Analytics](https://analytics.google.com)
   - 进入你的属性
   - 点击 "管理" → "DebugView"
   - 在 DebugView 中可以看到实时事件流

### 方法 3: 使用 Network 标签

1. 打开浏览器开发者工具（F12）
2. 切换到 "Network" 标签
3. 在过滤器中输入 `google-analytics` 或 `gtag`
4. 触发页面操作（点击、滚动等）
5. 查看发送到 Google Analytics 的请求

---

## 📊 验证步骤

### 步骤 1: 检查 Analytics 是否加载

在浏览器控制台运行：

```javascript
window.__checkAnalyticsStatus()
```

应该看到：
- ✅ gtag loaded: ✅
- ✅ dataLayer loaded: ✅
- ✅ GA ID: G-73C89GPVERCEL（本地开发环境）

### 步骤 2: 测试事件发送

```javascript
// 发送测试事件
window.__testAnalyticsEvent()
```

在控制台应该看到：
```
🧪 Testing Analytics event...
✅ Test event sent: {event_category: "Test", ...}
```

### 步骤 3: 启用调试模式

```javascript
window.__enableAnalyticsDebug()
```

之后所有的 Analytics 事件都会在控制台输出，例如：
```
🔍 [Analytics Debug]
Event: event
Parameters: ["test_event", {event_category: "Test", ...}]
```

### 步骤 4: 验证页面浏览

1. 刷新页面
2. 在控制台查看是否有 `page_view` 事件
3. 或在 Network 标签中查看是否有对 `google-analytics.com` 的请求

### 步骤 5: 验证自定义事件

在代码中调用事件追踪函数，例如：

```typescript
import { trackEvent } from '@/components/Analytics';

// 在某个按钮点击时
trackEvent('click', 'Button', 'Download');
```

在控制台应该看到相应的事件输出。

---

## 🐛 常见问题

### Q1: 控制台显示 "Analytics 未配置"

**原因**: 没有设置 `NEXT_PUBLIC_GA_ID` 环境变量

**解决**:
1. 创建 `frontend/.env.local` 文件
2. 添加 `NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX`
3. 重启开发服务器

### Q2: 控制台没有调试面板

**原因**: 调试工具可能没有自动加载

**解决**:
1. 手动在控制台运行：
   ```javascript
   import('@/lib/analytics-debug').then(m => m.showAnalyticsDebugPanel())
   ```
2. 或刷新页面

### Q3: 事件没有发送到 Google Analytics

**检查**:
1. 确认 GA ID 正确
2. 检查 Network 标签，查看是否有对 `google-analytics.com` 的请求
3. 检查是否有 CORS 错误
4. 确认没有广告拦截器阻止了请求

### Q4: DebugView 没有显示事件

**原因**: DebugView 需要启用 GA Debugger 扩展

**解决**:
1. 安装 Google Analytics Debugger 扩展
2. 点击扩展图标启用
3. 刷新页面
4. 在 GA DebugView 中查看

### Q5: Vercel Analytics 在本地不工作

**原因**: Vercel Analytics 只在 Vercel 部署环境中工作

**说明**: 这是正常的，Vercel Analytics 需要 Vercel 的基础设施支持。本地开发时：
- ✅ Google Analytics 可以正常工作
- ❌ Vercel Analytics 不会工作（但不会报错）

---

## 🎯 测试清单

- [ ] Analytics 组件已加载
- [ ] gtag 函数可用
- [ ] dataLayer 已初始化
- [ ] 页面浏览事件正常发送
- [ ] 自定义事件可以发送
- [ ] 调试模式可以启用
- [ ] Network 标签可以看到请求
- [ ] Google Analytics DebugView 可以查看事件（如果使用扩展）

---

## 💡 调试技巧

### 1. 使用条件断点

在浏览器开发者工具的 Sources 标签中，可以在 Analytics 代码中设置断点，查看事件数据。

### 2. 监听 dataLayer

在控制台运行：

```javascript
// 监听所有 dataLayer 推送
const originalPush = window.dataLayer.push;
window.dataLayer.push = function(...args) {
  console.log('DataLayer push:', args);
  return originalPush.apply(window.dataLayer, args);
};
```

### 3. 检查事件参数

在发送事件后，检查 dataLayer：

```javascript
// 查看所有事件
console.log(window.dataLayer);
```

### 4. 使用 React DevTools

如果使用 React DevTools，可以查看 Analytics 组件的 props 和状态。

---

## 📚 相关资源

- [Google Analytics DebugView 文档](https://support.google.com/analytics/answer/7201382)
- [GA4 事件调试指南](https://developers.google.com/analytics/devguides/collection/ga4/debug/events)
- [Next.js 环境变量文档](https://nextjs.org/docs/app/building-your-application/configuring/environment-variables)

---

## ✅ 完成检查

完成以上步骤后，你应该能够：
- ✅ 在本地验证 Analytics 功能
- ✅ 查看事件发送情况
- ✅ 调试事件参数
- ✅ 确认 Analytics 正常工作

**现在可以放心部署到生产环境了！** 🎉

