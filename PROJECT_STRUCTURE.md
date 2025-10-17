# 全球云基础设施节点分布图 - 项目结构说明

## 项目概述

这是一个全面的云服务商基础设施可视化项目，展示了全球主要云服务商的数据中心分布情况。项目支持10家主流云服务商，包含208个全球节点数据。

## 项目特性

### ✨ 核心功能

1. **统计分析面板**
   - 全局统计：总节点数、云服务商数量、覆盖国家、可用区总数
   - 供应商对比表：展示各云服务商的节点数、国家覆盖、可用区数，并按节点数排序
   - 排名徽章：前三名显示金银铜牌标识

2. **多维度图表分析**
   - 📈 各云服务商节点数量对比（柱状图）
   - 🌍 各大洲节点分布（堆叠柱状图）
   - 📅 节点逐年增长趋势（折线图）
   - 🏆 各服务商国家覆盖对比（环形图）

3. **交互式世界地图**
   - 基于 ECharts 的散点地图
   - 实时展示208个数据中心位置
   - 10种颜色区分不同云服务商
   - 支持缩放、平移操作
   - 一键重置视图按钮

4. **节点明细数据表**
   - 完整的节点信息列表
   - 多维度筛选：按云服务商、状态筛选
   - 实时搜索：支持节点ID、名称、城市、国家搜索
   - 分页显示：每页20条，共11页
   - 详细信息：节点ID、名称、云服务商、国家、城市、可用区数、状态、启用时间

### 🎨 设计特点

- **现代化 UI**：渐变背景、毛玻璃效果、圆角卡片
- **响应式布局**：自适应不同屏幕尺寸
- **视觉分层**：统计分析 → 地图展示 → 明细数据，逻辑清晰
- **交互友好**：平滑动画、悬浮效果、直观操作

## 目录结构

```
cloud-nodes-map/
├── data/                                    # 数据目录
│   ├── alibaba-cloud/                      # 阿里云数据
│   │   └── nodes.json                      # 29个节点，14国，89个可用区
│   ├── aws/                                # AWS数据
│   │   └── nodes.json                      # 24个节点，18国，24个可用区
│   ├── azure/                              # Azure数据
│   │   └── nodes.json                      # 34个节点，19国，34个可用区
│   ├── google-cloud/                       # Google Cloud数据
│   │   └── nodes.json                      # 36个节点，24国，36个可用区
│   ├── huawei-cloud/                       # 华为云数据
│   │   └── nodes.json                      # 16个节点，10国，16个可用区
│   ├── tencent-cloud/                      # 腾讯云数据
│   │   └── nodes.json                      # 18个节点，9国，18个可用区
│   ├── oracle-cloud/                       # 甲骨文云数据
│   │   └── nodes.json                      # 21个节点，15国，21个可用区
│   ├── ibm-cloud/                          # IBM云数据
│   │   └── nodes.json                      # 11个节点，7国，11个可用区
│   ├── ovh-cloud/                          # OVH云数据
│   │   └── nodes.json                      # 9个节点，7国，9个可用区
│   ├── digitalocean/                       # DigitalOcean数据
│   │   └── nodes.json                      # 10个节点，8国，10个区
│   └── providers-metadata.json             # 供应商元数据配置
│
├── docs/                                    # 文档目录
│   ├── PROJECT_SUMMARY.md                  # 项目总结
│   ├── README.md                           # 文档说明
│   └── [其他文档...]                       # 阿里云分析文档等
│
├── scripts/                                 # 脚本目录
│   ├── alibaba_cloud_analysis.py           # 阿里云数据分析脚本
│   └── alibaba_cloud_visualization.py      # 阿里云可视化脚本
│
├── src/                                     # 源码目录
│   ├── generators/                         # 生成器
│   ├── parsers/                            # 解析器
│   ├── validators/                         # 验证器
│   └── material/                           # 素材
│       └── global_infrastructure/          # 全球基础设施图片
│
├── cloud-infrastructure-map.html           # 🌟 主应用（推荐使用）
├── cloud-infrastructure-map-simple.html    # 简化版
├── cloud-infrastructure-scatter.html       # 散点图版
│
├── serve.py                                # 本地HTTP服务器
├── requirements.txt                        # Python依赖
├── CLOUD_MAP_README.md                     # 项目说明
├── PROJECT_STRUCTURE.md                    # 本文档
└── README.md                               # 项目README
```

## 数据结构说明

### 节点数据格式 (nodes.json)

```json
{
  "provider": "provider_id",
  "version": "1.0.0",
  "last_updated": "2025-01-01T00:00:00",
  "nodes": [
    {
      "node_id": "unique-node-id",
      "name": "节点显示名称",
      "location": {
        "country": "国家",
        "region": "区域",
        "city": "城市",
        "latitude": 0.0,
        "longitude": 0.0
      },
      "data_center": "数据中心名称",
      "availability_zones": 3,           // 可用区数量
      "status": "active",                 // 状态：active/inactive
      "network_info": {
        "bandwidth": "100Gbps",
        "latency": 3.5,
        "uptime": 99.95
      },
      "description": "数据中心描述",
      "launch_date": "2016-01-01T00:00:00"
    }
  ]
}
```

### 供应商元数据格式 (providers-metadata.json)

```json
{
  "providers": {
    "provider_id": {
      "id": "provider_id",
      "name": "中文名称",
      "name_en": "English Name",
      "color": "#HEX_COLOR",
      "founded": "2009",
      "headquarters": "总部位置",
      "data_path": "data/provider/nodes.json",
      "website": "https://...",
      "description": "描述",
      "market_position": "市场定位"
    }
  },
  "display_order": ["aws", "azure", ...],
  "color_scheme": { ... }
}
```

## 云服务商配置

### 颜色方案设计

为了确保10个云服务商在地图和图表中的视觉区分度，我们精心设计了配色方案：

| 供应商 | 颜色代码 | 说明 |
|--------|----------|------|
| 阿里云 | `#FF6A00` | 阿里橙 |
| AWS | `#FF9900` | AWS橙 |
| Azure | `#0078D4` | 微软蓝 |
| Google Cloud | `#4285F4` | 谷歌蓝 |
| 华为云 | `#D0021B` | 华为红 |
| 腾讯云 | `#006EFF` | 腾讯蓝 |
| 甲骨文云 | `#F80000` | Oracle红 |
| IBM 云 | `#0F62FE` | IBM蓝 |
| OVH 云 | `#123F6D` | OVH深蓝 |
| DigitalOcean | `#0080FF` | DO天蓝 |

### 供应商排名（按节点数）

1. 🥇 **Google Cloud** - 36节点，24国，36区
2. 🥈 **Azure** - 34节点，19国，34区
3. 🥉 **阿里云** - 29节点，14国，89区
4. **AWS** - 24节点，18国，24区
5. **甲骨文云** - 21节点，15国，21区
6. **腾讯云** - 18节点，9国，18区
7. **华为云** - 16节点，10国，16区
8. **IBM 云** - 11节点，7国，11区
9. **DigitalOcean** - 10节点，8国，10区
10. **OVH 云** - 9节点，7国，9区

## 技术栈

### 前端技术
- **HTML5** - 页面结构
- **CSS3** - 样式与动画
  - Flexbox & Grid 布局
  - 渐变背景
  - 毛玻璃效果（backdrop-filter）
  - 圆角与阴影
- **JavaScript (ES6+)** - 交互逻辑
  - Async/Await 异步数据加载
  - Promise.all 并行请求
  - 数据处理与转换
  - 事件监听与DOM操作

### 数据可视化
- **ECharts 5.4.3** - 图表库
  - 世界地图（Scatter）
  - 柱状图（Bar）
  - 折线图（Line）
  - 环形图（Pie/Doughnut）
  - 堆叠柱状图（Stacked Bar）

### 开发工具
- **Python 3** - 本地服务器（serve.py）
- **Git** - 版本控制

## 使用指南

### 快速启动

1. **启动本地服务器**
   ```bash
   cd /path/to/cloud-nodes-map
   python3 serve.py
   ```

2. **访问应用**
   - 打开浏览器访问：http://localhost:8000/cloud-infrastructure-map.html

3. **探索功能**
   - 查看统计分析面板了解全局数据
   - 滚动到图表部分查看多维度分析
   - 在地图上查看节点分布，支持缩放和平移
   - 使用重置按钮恢复地图初始视图
   - 在节点明细表中搜索和筛选特定节点

### 交互操作

#### 地图操作
- **缩放**：鼠标滚轮或触摸板手势
- **平移**：鼠标拖拽
- **重置**：点击左下角🔄按钮恢复初始视图
- **图例**：左下角显示所有云服务商及其颜色

#### 节点筛选
- **搜索框**：输入关键词实时搜索（节点ID、名称、城市、国家）
- **云服务商筛选**：下拉选择特定供应商
- **状态筛选**：选择"运行中"或"已停用"

#### 分页浏览
- **上一页/下一页**：浏览所有节点数据
- **页码信息**：显示当前页、总页数、总节点数

## 数据统计

### 全局统计（截至2025年）
- **总节点数**：208个
- **云服务商**：10家
- **覆盖国家**：36个
- **可用区总数**：268个

### 地理分布
- **亚洲**：80+节点（中国、日本、韩国、新加坡、印度等）
- **北美洲**：60+节点（美国、加拿大）
- **欧洲**：50+节点（德国、英国、法国、荷兰等）
- **大洋洲**：10+节点（澳大利亚）
- **南美洲**：5+节点（巴西、智利）
- **非洲**：少量节点

### 时间线
- **2006**：AWS开始布局
- **2008-2010**：Google Cloud、Azure进入市场
- **2011-2013**：阿里云、DigitalOcean成立
- **2013-2017**：华为云、腾讯云、IBM Cloud崛起
- **2016-2020**：Oracle Cloud快速扩张
- **2020-2025**：各家持续全球化布局

## 维护指南

### 添加新的云服务商

1. **创建数据文件**
   ```bash
   mkdir -p data/new-provider
   # 创建 data/new-provider/nodes.json
   ```

2. **更新 providers-metadata.json**
   - 添加新供应商信息
   - 分配独特的颜色代码
   - 更新 display_order

3. **更新 HTML 文件**
   - 在 `providers` 对象中添加配置
   - 在 `loadData()` 函数中添加数据加载
   - 在图例中添加显示项

### 更新节点数据

1. 编辑对应供应商的 `nodes.json` 文件
2. 更新 `last_updated` 时间戳
3. 添加或修改节点信息
4. 刷新浏览器查看更新

### 自定义样式

- 修改 CSS 变量以调整主题色
- 更新 `.section-header` 渐变背景
- 调整图表高度、颜色等参数

## 性能优化

### 已实现的优化
- ✅ 并行加载所有数据文件（Promise.all）
- ✅ 图表按需渲染
- ✅ 分页显示大量节点数据
- ✅ 客户端搜索和筛选（无需服务器请求）
- ✅ 响应式图表大小调整

### 未来可优化项
- [ ] 数据懒加载（按需加载供应商数据）
- [ ] 虚拟滚动（优化大列表性能）
- [ ] Service Worker（离线访问）
- [ ] WebGL渲染（更流畅的地图交互）

## 常见问题

### Q: 为什么地图不显示？
A: 确保已启动本地服务器，并检查浏览器控制台是否有错误。ECharts需要通过HTTP协议加载地图数据。

### Q: 如何添加更多国家到大洲映射？
A: 在 HTML 文件的 `continentMapping` 对象中添加新的国家-大洲映射。

### Q: 可用区数量为什么显示为0？
A: 检查数据文件中的字段名，确保使用 `availability_zones`（复数）或正确处理 `availability_zone`（单数）。

### Q: 如何更改地图初始视图？
A: 修改 `createMap()` 函数中的 `geo.zoom` 和 `geo.center` 参数。

## 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目仅供学习和研究使用。数据来源于各云服务商公开信息。

## 联系方式

如有问题或建议，请通过 GitHub Issues 联系我们。

---

**最后更新**: 2025年1月  
**版本**: v2.0 (支持10家云服务商)  
**状态**: ✅ 生产就绪

