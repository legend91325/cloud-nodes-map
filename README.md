# 云厂商全球节点数据

这个项目收集和整理了各大主流云厂商的全球节点数据，包括：

- 阿里云 (Alibaba Cloud)
- 华为云 (Huawei Cloud)
- 腾讯云 (Tencent Cloud)
- AWS (Amazon Web Services)
- 微软云 (Microsoft Azure)
- Google Cloud

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
│   ├── parsers/           # 数据解析器
│   ├── validators/        # 数据验证器
│   └── generators/        # 数据生成器
├── docs/                  # 文档
├── scripts/               # 脚本文件
└── tests/                 # 测试文件
```

## 数据格式

每个云厂商的节点数据包含以下信息：

- 节点ID
- 节点名称
- 地理位置（国家/地区/城市）
- 数据中心名称
- 可用区信息
- 服务类型
- 网络延迟
- 状态信息

## 使用方法

1. 查看特定云厂商的节点数据
2. 比较不同云厂商的节点分布
3. 分析全球节点覆盖情况
4. 生成可视化报告

## 更新频率

数据每月更新一次，确保信息的准确性和时效性。 