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

### 本地开发

#### 1. 启动前端开发服务器

```bash
cd frontend
npm install
npm run dev
```

访问：**http://localhost:3000**

#### 2. 启动静态 HTML 服务器（旧版）

```bash
cd cloud-nodes-map
python3 serve.py
```

访问：**http://localhost:8000/cloud-infrastructure-map.html**

### 部署到生产环境

项目已优化支持 **Vercel** 部署，推荐使用：

📖 **详细部署指南**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

**快速部署（5分钟）**:
```bash
# 1. 运行部署前准备脚本（自动同步数据、检查构建）
bash scripts/pre-deploy.sh

# 2. 提交代码到 GitHub
git add .
git commit -m "准备部署到 Vercel"
git push origin main

# 3. 在 Vercel 中部署
# - 访问 https://vercel.com 并登录
# - 导入项目，设置 Root Directory 为 `frontend`
# - 点击部署，完成！
```

**重要提示**:
- ⚠️ 在 Vercel 中必须设置 **Root Directory** 为 `frontend`
- ✅ 数据文件会自动从 `data/` 同步到 `frontend/public/data/`
- ✅ 每次部署前运行 `bash scripts/pre-deploy.sh` 确保数据最新
- 🌐 自定义域名 `northcloud.cloud` 配置指南: [DOMAIN_SETUP.md](DOMAIN_SETUP.md)

其他推荐平台：Netlify、Cloudflare Pages（详见部署指南）

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

## 📊 数据管理

### 数据快速参考

| 云服务商 | 节点数 | 国家数 | 最后更新 | 数据文件 | 优先级 |
|---------|-------|-------|---------|---------|-------|
| **Google Cloud** | 36 | 24 | 2024-01-15 | `data/google-cloud/nodes.json` | ⭐⭐⭐ |
| **Azure** | 34 | 19 | 2024-01-15 | `data/azure/nodes.json` | ⭐⭐⭐ |
| **阿里云** | 29 | 14 | 2024-12-19 | `data/alibaba-cloud/nodes.json` | ⭐⭐ |
| **AWS** | 24 | 18 | 2024-01-15 | `data/aws/nodes.json` | ⭐⭐⭐ |
| **Oracle Cloud** | 21 | 15 | 2025-01-01 | `data/oracle-cloud/nodes.json` | ⭐ |
| **腾讯云** | 18 | 9 | 2024-01-15 | `data/tencent-cloud/nodes.json` | ⭐⭐ |
| **华为云** | 16 | 10 | 2024-01-15 | `data/huawei-cloud/nodes.json` | ⭐⭐ |
| **火山引擎** | 14 | 8 | 2025-10-23 | `data/volcano-engine/nodes.json` | ✅ |
| **IBM Cloud** | 11 | 7 | 2025-01-01 | `data/ibm-cloud/nodes.json` | ⭐ |
| **DigitalOcean** | 10 | 8 | 2025-01-01 | `data/digitalocean/nodes.json` | ⭐ |
| **OVH Cloud** | 9 | 7 | 2025-01-01 | `data/ovh-cloud/nodes.json` | ⭐ |

**优先级说明**:
- ⭐⭐⭐ **高**: 主流云服务商，更新频繁，需要定期校准
- ⭐⭐ **中**: 区域性云服务商，按需更新
- ⭐ **低**: 覆盖较少，数据变化不大
- ✅ **最新**: 最近刚更新，暂时无需校准

### 数据源参考

#### 全球三大云（优先校准）

**AWS (Amazon Web Services)**
- 🔗 区域和可用区: https://aws.amazon.com/about-aws/global-infrastructure/regions_az/
- 🔗 全球基础设施: https://infrastructure.aws/
- 🔧 CLI查询: `aws ec2 describe-regions`
- 📝 建议更新频率: 每季度

**Microsoft Azure**
- 🔗 Azure区域: https://azure.microsoft.com/en-us/explore/global-infrastructure/geographies/
- 🔗 互动地图: https://datacenters.microsoft.com/globe/
- 🔧 CLI查询: `az account list-locations`
- 📝 建议更新频率: 每季度

**Google Cloud Platform**
- 🔗 区域和可用区: https://cloud.google.com/about/locations
- 🔗 全球位置: https://cloud.google.com/infrastructure/locations
- 🔧 CLI查询: `gcloud compute regions list`
- 📝 建议更新频率: 每季度

#### 中国云服务商

**阿里云 (Alibaba Cloud)**
- 🔗 中文文档: https://help.aliyun.com/document_detail/40654.html
- 🔗 国际站: https://www.alibabacloud.com/global-locations
- 🔧 CLI查询: `aliyun ecs DescribeRegions`
- 📝 建议更新频率: 每半年

**腾讯云 (Tencent Cloud)**
- 🔗 地域文档: https://cloud.tencent.com/document/product/213/6091
- 🔗 国际版: https://www.tencentcloud.com/document/product/213/6091
- 📝 建议更新频率: 每半年

**华为云 (Huawei Cloud)**
- 🔗 区域文档: https://support.huaweicloud.com/usermanual-iaas/zh-cn_topic_0184026189.html
- 🔗 全球站点: https://www.huaweicloud.com/intl/en-us/global/
- 📝 建议更新频率: 每半年

**火山引擎 (Volcano Engine)**
- 🔗 地域文档: https://www.volcengine.com/docs/6396/69693
- 🔗 全球基础设施: https://www.volcengine.com/product
- 📝 最后更新: 2025-10-23（最新）

#### 其他云服务商

**Oracle Cloud Infrastructure**
- 🔗 区域文档: https://docs.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm
- 🔗 全球区域: https://www.oracle.com/cloud/data-regions/
- 📝 建议更新频率: 每年

**IBM Cloud**
- 🔗 位置文档: https://cloud.ibm.com/docs/overview?topic=overview-locations
- 🔗 数据中心: https://www.ibm.com/cloud/data-centers
- 📝 建议更新频率: 每年

**OVHcloud**
- 🔗 全球基础设施: https://www.ovhcloud.com/en/about-us/global-infrastructure/
- 🔗 区域可用性: https://www.ovhcloud.com/en/public-cloud/regions-availability/
- 📝 建议更新频率: 每年

**DigitalOcean**
- 🔗 数据中心: https://docs.digitalocean.com/products/platform/availability-matrix/
- 🔗 产品文档: https://www.digitalocean.com/products/data-centers
- 📝 建议更新频率: 每年

### 数据验证工具

项目提供了数据验证脚本，用于检查数据文件的完整性和正确性：

```bash
# 验证所有云服务商数据
python3 validate_data.py
```

验证脚本会检查：
- JSON 格式正确性
- 必需字段完整性
- 经纬度范围有效性
- 节点状态有效性

## 📚 相关文档

- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - 详细部署指南（推荐阅读）
- [docs/README.md](docs/README.md) - 阿里云节点分析项目文档

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