# 全球云基础设施节点分布图 🌍

这是一个全面的云服务商基础设施可视化项目，收集和展示了全球主要云服务商的数据中心分布情况。

## 🎯 支持的云服务商（共10家）

### 国际巨头
- 🇺🇸 **AWS** (Amazon Web Services) - 24节点，18国
- 🇺🇸 **Azure** (Microsoft Azure) - 34节点，19国
- 🇺🇸 **Google Cloud** - 36节点，24国
- 🇺🇸 **Oracle Cloud** - 21节点，15国
- 🇺🇸 **IBM Cloud** - 11节点，7国

### 中国云服务商
- 🇨🇳 **阿里云** (Alibaba Cloud) - 29节点，14国
- 🇨🇳 **华为云** (Huawei Cloud) - 16节点，10国
- 🇨🇳 **腾讯云** (Tencent Cloud) - 18节点，9国

### 特色云服务
- 🇫🇷 **OVHcloud** - 9节点，7国（欧洲最大）
- 🇺🇸 **DigitalOcean** - 10节点，8国（开发者友好）

## 📊 项目统计

- **总节点数**: 208个
- **覆盖国家**: 36个
- **可用区总数**: 268个
- **数据更新**: 2025年1月

## 🚀 快速开始

### 1. 启动本地服务器

```bash
cd cloud-nodes-map
python3 serve.py
```

### 2. 访问应用

打开浏览器访问：**http://localhost:8000/cloud-infrastructure-map.html**

### 3. 探索功能

- 📈 查看统计分析面板
- 🗺️ 在交互式地图上浏览全球节点
- 🔍 搜索和筛选特定云服务商的节点
- 📋 查看详细的节点列表

## ✨ 核心功能

### 统计分析
- 全局统计数据展示
- 各云服务商对比表（带排名）
- 节点数量、国家覆盖、可用区数统计

### 多维度图表
- 📊 节点数量对比（柱状图）
- 🌍 各大洲分布（堆叠柱状图）
- 📈 增长趋势分析（折线图）
- 🥧 国家覆盖对比（环形图）

### 交互式地图
- 基于 ECharts 的世界地图
- 208个节点实时展示
- 10种颜色区分云服务商
- 支持缩放、平移、重置

### 节点明细
- 完整的节点信息表
- 实时搜索（节点ID、名称、城市、国家）
- 多维筛选（云服务商、状态）
- 分页浏览（每页20条）

## 📁 项目结构

```
cloud-nodes-map/
├── data/                      # 节点数据（10家云服务商）
│   ├── alibaba-cloud/        # 阿里云 - 29节点
│   ├── aws/                  # AWS - 24节点
│   ├── azure/                # Azure - 34节点
│   ├── google-cloud/         # Google Cloud - 36节点
│   ├── huawei-cloud/         # 华为云 - 16节点
│   ├── tencent-cloud/        # 腾讯云 - 18节点
│   ├── oracle-cloud/         # 甲骨文云 - 21节点
│   ├── ibm-cloud/            # IBM云 - 11节点
│   ├── ovh-cloud/            # OVH云 - 9节点
│   ├── digitalocean/         # DigitalOcean - 10节点
│   └── providers-metadata.json  # 供应商元数据配置
├── docs/                     # 项目文档
├── scripts/                  # 数据分析脚本
├── src/                      # 源代码
│   ├── parsers/             # 数据解析器
│   ├── validators/          # 数据验证器
│   └── generators/          # 数据生成器
├── cloud-infrastructure-map.html      # 🌟 主应用
├── serve.py                 # 本地HTTP服务器
├── requirements.txt         # Python依赖
└── PROJECT_STRUCTURE.md     # 详细项目结构文档
```

## 📝 数据格式

每个云服务商的节点数据（JSON格式）包含：

- **节点ID**: 唯一标识符
- **节点名称**: 显示名称（中英文）
- **地理位置**: 国家、区域、城市、经纬度坐标
- **数据中心**: 数据中心名称
- **可用区数量**: 该节点的可用区数
- **网络信息**: 带宽、延迟、可用性
- **状态**: active（运行中）/ inactive（已停用）
- **启用时间**: 数据中心上线日期

示例：
```json
{
  "node_id": "us-east-1",
  "name": "US East (N. Virginia)",
  "location": {
    "country": "美国",
    "city": "弗吉尼亚",
    "latitude": 38.13,
    "longitude": -78.45
  },
  "availability_zones": 6,
  "status": "active",
  "launch_date": "2006-08-25T00:00:00"
}
```

## 🛠️ 技术栈

- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **可视化**: ECharts 5.4.3
- **服务器**: Python 3 (HTTP Server)
- **数据格式**: JSON

## 🎨 设计特色

- ✨ 现代化渐变UI设计
- 🔄 响应式布局
- 🎯 直观的数据可视化
- 🖱️ 流畅的交互体验
- 📱 跨设备支持

## 📚 相关文档

- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 详细的项目结构说明
- [CLOUD_MAP_README.md](CLOUD_MAP_README.md) - 地图功能说明
- [docs/PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md) - 项目总结

## 🔄 更新日志

### v2.0 (2025-01)
- ✅ 新增4家云服务商支持（Oracle Cloud, IBM Cloud, OVHcloud, DigitalOcean）
- ✅ 优化颜色方案，提升10个供应商的视觉区分度
- ✅ 改进图例布局，采用双列网格显示
- ✅ 增强节点明细表的搜索和筛选功能
- ✅ 添加地图重置按钮

### v1.0 (2024-12)
- ✅ 支持6家主流云服务商
- ✅ 交互式世界地图
- ✅ 统计分析面板
- ✅ 多维度图表展示

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目仅供学习和研究使用。数据来源于各云服务商公开信息。

---

**维护者**: Bo Wang  
**更新日期**: 2025年1月  
**项目状态**: ✅ 活跃维护中 