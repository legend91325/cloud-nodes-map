# 云服务商测评网站设计规范

## 设计理念

**"简洁、现代、专业"** - 参考 Google Cloud 的 Material Design 设计语言，采用蓝色系作为主色，传达科技感与专业性；通过清晰的层次结构、适当的阴影和简洁的布局，构建易于理解、高效使用的界面，让技术决策者能够快速获取关键信息。

---

## 色系系统

### 主色 (Primary Color) - Google Cloud 风格

- **Primary-50**: `#E8F0FE` - 极浅蓝，用于背景、卡片背景、高亮区域
- **Primary-100**: `#D2E3FC` - 浅蓝，用于悬停状态、次要背景
- **Primary-500**: `#4285F4` - Google 蓝，用于主要按钮、链接、品牌标识
- **Primary-600**: `#1A73E8` - 深蓝，用于按钮悬停状态、强调元素
- **Primary-700**: `#1967D2` - 更深蓝，用于激活状态

**应用场景**:
- 头部导航栏：使用 `bg-primary-500` 或 `bg-primary-600`
- 主要按钮：`bg-primary-500 text-white hover:bg-primary-600`
- 次要按钮：`bg-white text-primary-500 border border-primary-500 hover:bg-primary-50`
- 链接：`text-primary-500 hover:text-primary-600`
- 表格表头：`bg-primary-50 text-primary-700`

### 辅助色 (Secondary Colors) - Google Material Colors

#### 成功色 (Success)
- **Success-50**: `#E6F4EA` - 浅绿背景
- **Success-500**: `#34A853` - Google 绿，用于成功提示、完成状态、正向指标

**应用场景**:
- 成功消息：`bg-success-50 text-success-500`
- 状态标签（运行中）：`bg-success-50 text-success-500`
- 正向指标：`text-success-500`

#### 警告色 (Warning)
- **Warning-50**: `#FEF7E0` - 浅黄背景
- **Warning-500**: `#FBBC05` - Google 黄，用于警告提示、注意事项、待处理状态

**应用场景**:
- 警告消息：`bg-warning-50 text-warning-500`
- 警告标签：`bg-warning-50 text-warning-500`

#### 错误色 (Error)
- **Error-50**: `#FCE8E6` - 浅红背景
- **Error-500**: `#EA4335` - Google 红，用于错误提示、失败状态、删除操作

**应用场景**:
- 错误消息：`bg-error-50 text-error-500`
- 错误标签：`bg-error-50 text-error-500`

#### 信息色 (Info)
- **Info-50**: `#E8F0FE` - 浅蓝背景（与 Primary-50 相同）
- **Info-500**: `#4285F4` - Google 蓝（与 Primary-500 相同），用于信息提示、帮助说明

**应用场景**:
- 信息消息：`bg-info-50 text-info-500`
- 信息标签：`bg-info-50 text-info-500`

### 中性色 (Neutral Colors) - Google Material Gray

- **Neutral-50**: `#F8F9FA` - 近白灰，用于页面背景、容器背景
- **Neutral-100**: `#F1F3F4` - 极浅灰，用于卡片背景、输入框背景、次要区域背景
- **Neutral-200**: `#E8EAED` - 浅灰，用于边框、分割线
- **Neutral-300**: `#DADCE0` - 中浅灰，用于边框、分割线、禁用状态
- **Neutral-500**: `#5F6368` - 中灰，用于辅助文字、说明文字、占位符
- **Neutral-700**: `#3C4043` - 中深灰，用于副标题、次要文字
- **Neutral-900**: `#202124` - 深灰黑，用于主标题、重要文字

**应用场景**:
- 主标题：`text-neutral-900`
- 副标题：`text-neutral-700`
- 辅助文字：`text-neutral-500`
- 边框：`border-neutral-200` 或 `border-neutral-300`
- 背景：`bg-white` 或 `bg-neutral-50`
- 禁用状态：`bg-neutral-200 text-neutral-500`

---

## 组件设计规范

### 头部 (Header) - Google Cloud 风格
```tsx
<header className="bg-white border-b border-neutral-200 shadow-sm">
  <div className="container mx-auto px-4 py-4">
    <h1 className="text-2xl font-medium text-neutral-900">标题</h1>
    <p className="text-sm text-neutral-500 mt-1">副标题</p>
  </div>
</header>
```

### 按钮系统 - Material Design 风格

#### 主要按钮 (Primary Button)
```tsx
<button className="bg-primary-500 text-white px-4 py-2 rounded-md hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors shadow-sm">
  主要操作
</button>
```

#### 次要按钮 (Secondary Button)
```tsx
<button className="bg-white text-primary-500 border border-primary-500 px-4 py-2 rounded-md hover:bg-primary-50 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors">
  次要操作
</button>
```

#### 文本按钮 (Text Button)
```tsx
<button className="text-primary-500 hover:bg-primary-50 px-4 py-2 rounded-md transition-colors">
  文本按钮
</button>
```

#### 成功按钮
```tsx
<button className="bg-success-500 text-white px-4 py-2 rounded-md hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-success-500 focus:ring-offset-2 transition-opacity shadow-sm">
  成功操作
</button>
```

#### 危险按钮
```tsx
<button className="bg-error-500 text-white px-4 py-2 rounded-md hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-error-500 focus:ring-offset-2 transition-opacity shadow-sm">
  危险操作
</button>
```

### 卡片 (Card) - Material Design Elevation
```tsx
<div className="bg-white rounded-lg shadow-sm border border-neutral-200 p-6 hover:shadow-md transition-shadow">
  {/* 内容 */}
</div>
```

**阴影层级**:
- 默认卡片：`shadow-sm` (轻微阴影)
- 悬停卡片：`shadow-md` (中等阴影)
- 模态框/对话框：`shadow-lg` (大阴影)

### 表格 (Table) - Google Cloud Console 风格

#### 表头
```tsx
<thead className="bg-neutral-50 border-b border-neutral-200">
  <th className="px-4 py-3 text-left text-xs font-medium text-neutral-700 uppercase tracking-wider">
    列名
  </th>
</thead>
```

#### 表格行
```tsx
<tbody className="bg-white divide-y divide-neutral-200">
  <tr className="hover:bg-neutral-50 transition-colors">
    <td className="px-4 py-3 text-sm text-neutral-900">内容</td>
  </tr>
</tbody>
```

### 标签 (Badge/Tag) - Material Design Chips

#### 状态标签
```tsx
{/* 成功状态 */}
<span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-success-50 text-success-500">
  运行中
</span>

{/* 警告状态 */}
<span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-warning-50 text-warning-500">
  警告
</span>

{/* 错误状态 */}
<span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-error-50 text-error-500">
  错误
</span>

{/* 信息状态 */}
<span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-info-50 text-info-500">
  信息
</span>
```

#### 大洲标签
```tsx
<span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-50 text-primary-700">
  亚洲
</span>
```

### 输入框 (Input) - Material Design Outlined
```tsx
<input 
  className="w-full px-3 py-2 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white text-neutral-900 placeholder:text-neutral-500"
  placeholder="请输入..."
/>
```

### 统计卡片 (Stats Card) - Google Cloud Dashboard 风格
```tsx
<div className="bg-white rounded-lg shadow-sm border border-neutral-200 p-6 hover:shadow-md transition-shadow">
  <p className="text-sm font-medium text-neutral-500 mb-1">标签</p>
  <p className="text-3xl font-normal text-neutral-900">
    数值
  </p>
  <p className="text-xs text-neutral-500 mt-1">说明文字</p>
</div>
```

---

## 页面布局规范

### 页面背景 - Google Cloud Console 风格
```tsx
<div className="min-h-screen bg-neutral-50">
  {/* 内容 */}
</div>
```

### 容器布局
```tsx
<div className="container mx-auto px-4 py-6 max-w-7xl">
  {/* 内容区域，最大宽度 1280px */}
</div>
```

### 加载状态 - Material Design Circular Progress
```tsx
<div className="flex items-center justify-center p-8">
  <div className="inline-block animate-spin rounded-full h-8 w-8 border-2 border-primary-500 border-t-transparent"></div>
  <p className="ml-3 text-sm text-neutral-500">加载中...</p>
</div>
```

### 页脚 - Google Cloud 风格
```tsx
<footer className="bg-white border-t border-neutral-200 py-6 mt-12">
  <div className="container mx-auto px-4 text-center">
    <p className="text-sm text-neutral-500">版权信息</p>
    <p className="text-xs text-neutral-400 mt-1">说明文字</p>
  </div>
</footer>
```

---

## 数据可视化色板

用于图表中区分不同云服务商的颜色（保持与设计规范一致）：

- **AWS**: `#FF9900` (橙色)
- **Azure**: `#0078D4` (蓝色)
- **Google Cloud**: `#34A853` (绿色，图表专用)
- **阿里云**: `#FF6A00` (橙红)
- **腾讯云**: `#9C27B0` (紫色)
- **华为云**: `#D0021B` (红色)
- **火山引擎**: `#00BCD4` (青色)
- **Oracle Cloud**: `#C74634` (红棕)
- **IBM Cloud**: `#FFC107` (金色)
- **OVH Cloud**: `#607D8B` (蓝灰)
- **DigitalOcean**: `#E91E63` (粉红)

**注意**: 在图表中使用时，建议在浅色背景上使用深色边框或阴影，确保可读性。

---

## 可访问性要求

### 对比度标准
- 所有颜色组合必须满足 **WCAG 2.1 AA级对比度标准**
- 正文文字 (Neutral-900) 与背景 (White): 16.8:1 ✅ AAA级
- 主色按钮 (Primary-500) 与文字 (White): 4.5:1 ✅ AA级
- 次要文字 (Neutral-500) 与背景 (White): 4.5:1 ✅ AA级

### 色盲友好
- 不仅依赖颜色传达信息，同时使用图标、文字、形状区分
- 图表中使用不同图案/纹理辅助区分
- 确保所有交互元素有明确的视觉反馈

### 交互状态
- 所有可点击元素提供明确的悬停、聚焦、激活状态
- 使用 Material Design 的 focus ring (ring-2 ring-primary-500 ring-offset-2)
- 适当的阴影变化增强层次感

---

## 代码规范

### 使用 Tailwind CSS 类名
- 优先使用 Tailwind CSS 工具类，而不是内联样式
- 使用已定义的颜色变量（如 `primary-500`、`neutral-500` 等）
- 避免使用硬编码的颜色值

### 响应式设计
- 使用 Tailwind 的响应式前缀（`sm:`、`md:`、`lg:`、`xl:`）
- 确保在所有设备上保持良好的可读性和可用性
- 容器最大宽度：`max-w-7xl` (1280px)

### 一致性
- 相同功能的组件使用相同的样式
- 保持间距、圆角、阴影等视觉元素的一致性
- 圆角：统一使用 `rounded-md` (4px) 或 `rounded-lg` (8px)
- 阴影：`shadow-sm` (默认), `shadow-md` (悬停), `shadow-lg` (模态框)

---

## 禁止事项

❌ **不要使用**:
- 硬编码的颜色值（如 `#FF0000`），应使用定义的颜色变量
- 未定义的颜色类名（如 `bg-red-500`），应使用 `bg-error-500`
- 不一致的圆角大小（统一使用 `rounded-md` 或 `rounded-lg`）
- 过度的阴影（遵循 Material Design 的 elevation 原则）
- 渐变背景（Google Cloud 风格偏向纯色背景）

✅ **应该使用**:
- 定义好的颜色系统（`primary-*`、`neutral-*`、`success-*` 等）
- 统一的间距系统（Tailwind 的间距工具类）
- Material Design 的阴影层级（shadow-sm, shadow-md, shadow-lg）
- 白色背景配合适当的边框和阴影

---

## 示例代码

### 完整的组件示例
```tsx
// 统计卡片组件 - Google Cloud Dashboard 风格
<div className="bg-white rounded-lg shadow-sm border border-neutral-200 p-6 hover:shadow-md transition-shadow">
  <div className="flex items-center justify-between">
    <div>
      <p className="text-sm font-medium text-neutral-500 mb-1">云服务商</p>
      <p className="text-3xl font-normal text-neutral-900">
        11
      </p>
    </div>
    <div className="w-12 h-12 rounded-lg bg-primary-50 flex items-center justify-center">
      <span className="text-2xl">☁️</span>
    </div>
  </div>
</div>
```

---

## 总结

遵循以上设计规范，确保：
1. **视觉一致性** - 所有组件使用统一的色系和样式，参考 Google Cloud 的设计语言
2. **专业感** - 蓝色主色传达科技、专业、可靠的形象
3. **可访问性** - 满足 WCAG 2.1 AA 级标准
4. **可维护性** - 使用统一的 Tailwind 类名，便于维护和更新
5. **Material Design** - 遵循 Material Design 的设计原则，包括适当的阴影、圆角和交互反馈

**记住**: 当创建新组件或修改现有组件时，始终参考此规范，保持整体设计风格与 Google Cloud 的一致性。
