# 前端应用

基于 Next.js 构建的云服务商节点分布可视化应用。

## 🚀 快速开始

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

访问 [http://localhost:3000](http://localhost:3000) 查看应用。

### 构建生产版本

```bash
npm run build
npm start
```

## 📁 项目结构

```
frontend/
├── app/                    # Next.js App Router
│   ├── layout.tsx          # 根布局
│   ├── page.tsx            # 首页
│   └── globals.css         # 全局样式
├── components/            # React 组件
│   ├── Header.tsx         # 页面头部
│   ├── StatsCard.tsx      # 统计卡片
│   ├── ProviderStatsTable.tsx      # 云服务商统计表
│   ├── ProviderCountryStatsTable.tsx # 国家覆盖统计表
│   ├── NodesTable.tsx     # 节点列表
│   ├── MapChart.tsx       # 地图图表
│   ├── ProviderComparisonChart.tsx  # 对比图表
│   ├── ContinentDistributionChart.tsx # 大洲分布图表
│   └── GrowthTrendChart.tsx # 增长趋势图表
├── lib/                   # 工具库
│   ├── data.ts            # 数据获取和处理
│   ├── chartColors.ts     # 图表颜色配置
│   └── chartData.ts       # 图表数据生成
└── types/                 # TypeScript 类型定义
    └── index.ts           # 类型定义
```

## 🎨 设计系统

项目采用 Google Cloud 风格的 Material Design 设计语言，详细设计规范请参考 [.cursor/rules.md](../.cursor/rules.md)。

### 主要颜色

- **Primary**: `#4285F4` (Google 蓝)
- **Success**: `#34A853` (Google 绿)
- **Warning**: `#FBBC05` (Google 黄)
- **Error**: `#EA4335` (Google 红)

## 🛠️ 技术栈

- **框架**: Next.js 15 (App Router)
- **语言**: TypeScript
- **样式**: Tailwind CSS v4
- **图表**: ECharts
- **数据可视化**: 自定义 React 组件

## 📊 数据源

数据文件位于 `public/data/` 目录，与根目录的 `data/` 目录同步。

## 🔧 开发说明

### 添加新的图表组件

1. 在 `components/` 目录创建新组件
2. 使用 `chartColors.ts` 中的颜色配置
3. 使用 `chartData.ts` 中的数据处理函数
4. 在 `app/page.tsx` 中引入使用

### 更新数据

数据文件位于项目根目录的 `data/` 目录，更新后需要同步到 `public/data/` 目录。

## 📝 注意事项

- 使用 Tailwind CSS v4 的 `@theme` 指令定义颜色
- 所有图表组件应遵循统一的设计规范
- 确保数据格式与 `types/index.ts` 中的类型定义一致
