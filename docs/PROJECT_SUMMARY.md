# 云厂商全球节点数据项目总结

## 项目概述

本项目收集和整理了全球六大主流云厂商的全球节点数据，包括：

- **阿里云 (Alibaba Cloud)** - 12个节点
- **华为云 (Huawei Cloud)** - 16个节点  
- **腾讯云 (Tencent Cloud)** - 18个节点
- **AWS (Amazon Web Services)** - 25个节点
- **微软云 (Microsoft Azure)** - 35个节点
- **Google Cloud** - 37个节点

## 数据统计

### 总体统计
- **总节点数**: 143个
- **覆盖国家/地区**: 45个
- **云厂商数量**: 6个
- **数据更新时间**: 2024年1月15日

### 各云厂商节点分布
| 云厂商 | 节点数量 | 覆盖国家 | 主要覆盖区域 |
|--------|----------|----------|--------------|
| Google Cloud | 37 | 25 | 全球 |
| Microsoft Azure | 35 | 24 | 全球 |
| AWS | 25 | 22 | 全球 |
| 腾讯云 | 18 | 15 | 亚太为主 |
| 华为云 | 16 | 15 | 亚太为主 |
| 阿里云 | 12 | 12 | 亚太为主 |

### 全球覆盖统计 (前10名)
1. **美国** - 25个节点
2. **中国** - 18个节点
3. **德国** - 12个节点
4. **日本** - 10个节点
5. **英国** - 9个节点
6. **新加坡** - 8个节点
7. **澳大利亚** - 8个节点
8. **韩国** - 7个节点
9. **法国** - 7个节点
10. **印度** - 6个节点

## 技术架构

### 数据模型
- **CloudNode**: 云节点数据模型
- **Location**: 地理位置信息
- **NetworkInfo**: 网络性能信息
- **ServiceType**: 服务类型枚举
- **NodeStatus**: 节点状态枚举

### 核心功能
1. **数据加载与解析** (`CloudDataLoader`)
   - 支持JSON格式数据加载
   - 数据验证和完整性检查
   - 多维度数据查询

2. **数据可视化** (`CloudDataVisualizer`)
   - 云厂商对比图表
   - 全球覆盖分布图
   - 服务类型分布图
   - 网络性能对比图
   - 上线时间线图
   - HTML报告生成

3. **数据导出**
   - CSV格式导出
   - 支持按云厂商筛选导出

## 项目结构

```
cloud-nodes-map/
├── data/                    # 节点数据文件
│   ├── alibaba-cloud/      # 阿里云节点数据
│   ├── huawei-cloud/       # 华为云节点数据
│   ├── tencent-cloud/      # 腾讯云节点数据
│   ├── aws/                # AWS节点数据
│   ├── azure/              # 微软云节点数据
│   └── google-cloud/       # Google Cloud节点数据
├── src/                    # 源代码
│   ├── models.py          # 数据模型定义
│   ├── data_loader.py     # 数据加载器
│   └── visualization.py   # 可视化工具
├── scripts/               # 脚本文件
│   ├── example_usage.py   # 使用示例
│   └── visualization_example.py # 可视化示例
├── tests/                 # 测试文件
├── docs/                  # 文档
└── charts/                # 生成的图表 (运行后生成)
```

## 主要特性

### 1. 数据完整性
- 包含节点ID、名称、地理位置、数据中心、可用区等完整信息
- 支持网络性能指标（带宽、延迟、可用性）
- 包含服务类型和节点状态信息

### 2. 多维度查询
- 按国家/地区查询
- 按服务类型查询
- 按节点状态查询
- 关键词搜索功能

### 3. 数据验证
- 自动验证数据完整性
- 检查坐标范围有效性
- 验证网络延迟数据合理性

### 4. 可视化分析
- 生成多种类型的图表
- 支持图表保存和HTML报告生成
- 提供交互式数据展示

## 使用示例

### 基本使用
```python
from src.data_loader import CloudDataLoader
from src.models import CloudProvider

# 初始化数据加载器
loader = CloudDataLoader()

# 加载特定云厂商数据
alibaba_data = loader.load_provider_data(CloudProvider.ALIBABA_CLOUD)

# 按国家查询节点
china_nodes = loader.get_nodes_by_country("中国")

# 获取统计信息
stats = loader.get_provider_statistics()
```

### 可视化使用
```python
from src.visualization import CloudDataVisualizer

# 创建可视化器
visualizer = CloudDataVisualizer(loader)

# 生成完整报告
visualizer.create_dashboard("charts")
```

## 数据来源

本项目的数据来源于各云厂商的官方文档和公开信息：

- 阿里云官方文档
- 华为云官方文档
- 腾讯云官方文档
- AWS官方文档
- Microsoft Azure官方文档
- Google Cloud官方文档

## 更新计划

- **月度更新**: 每月更新一次节点数据
- **季度审查**: 每季度审查数据准确性
- **年度扩展**: 每年扩展新的云厂商数据

## 贡献指南

欢迎贡献代码和数据：

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 创建Pull Request

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交Issue
- 发送邮件
- 参与讨论

---

**注意**: 本项目的数据仅供参考，实际使用时请以各云厂商的官方文档为准。 