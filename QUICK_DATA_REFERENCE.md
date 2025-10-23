# 云服务商数据快速参考表

## 📊 当前数据状态概览

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

**总计**: 11个云服务商，222个节点

**优先级说明**:
- ⭐⭐⭐ **高**: 主流云服务商，更新频繁，需要定期校准
- ⭐⭐ **中**: 区域性云服务商，按需更新
- ⭐ **低**: 覆盖较少，数据变化不大
- ✅ **最新**: 最近刚更新，暂时无需校准

---

## 🔗 核心数据源快速链接

### 全球三大云（优先校准）

#### 1. AWS - Amazon Web Services
- 📍 **区域和可用区**: https://aws.amazon.com/about-aws/global-infrastructure/regions_az/
- 📍 **全球基础设施**: https://infrastructure.aws/
- 🔧 **CLI查询**: `aws ec2 describe-regions`
- 📝 **建议更新频率**: 每季度

#### 2. Microsoft Azure
- 📍 **Azure区域**: https://azure.microsoft.com/en-us/explore/global-infrastructure/geographies/
- 📍 **互动地图**: https://datacenters.microsoft.com/globe/
- 🔧 **CLI查询**: `az account list-locations`
- 📝 **建议更新频率**: 每季度

#### 3. Google Cloud Platform
- 📍 **区域和可用区**: https://cloud.google.com/about/locations
- 📍 **全球位置**: https://cloud.google.com/infrastructure/locations
- 🔧 **CLI查询**: `gcloud compute regions list`
- 📝 **建议更新频率**: 每季度

---

### 中国云服务商

#### 4. 阿里云 (Alibaba Cloud)
- 📍 **中文文档**: https://help.aliyun.com/document_detail/40654.html
- 📍 **国际站**: https://www.alibabacloud.com/global-locations
- 🔧 **CLI查询**: `aliyun ecs DescribeRegions`
- 📝 **建议更新频率**: 每半年
- ⚠️ **注意**: 中国站和国际站数据可能有差异

#### 5. 腾讯云 (Tencent Cloud)
- 📍 **地域文档**: https://cloud.tencent.com/document/product/213/6091
- 📍 **国际版**: https://www.tencentcloud.com/document/product/213/6091
- 📝 **建议更新频率**: 每半年

#### 6. 华为云 (Huawei Cloud)
- 📍 **区域文档**: https://support.huaweicloud.com/usermanual-iaas/zh-cn_topic_0184026189.html
- 📍 **全球站点**: https://www.huaweicloud.com/intl/en-us/global/
- 📝 **建议更新频率**: 每半年

#### 7. 火山引擎 (Volcano Engine) ✅ 已更新
- 📍 **地域文档**: https://www.volcengine.com/docs/6396/69693
- 📍 **全球基础设施**: https://www.volcengine.com/product
- 📝 **最后更新**: 2025-10-23（最新）

---

### 其他云服务商

#### 8. Oracle Cloud Infrastructure
- 📍 **区域文档**: https://docs.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm
- 📍 **全球区域**: https://www.oracle.com/cloud/data-regions/
- 📝 **建议更新频率**: 每年

#### 9. IBM Cloud
- 📍 **位置文档**: https://cloud.ibm.com/docs/overview?topic=overview-locations
- 📍 **数据中心**: https://www.ibm.com/cloud/data-centers
- 📝 **建议更新频率**: 每年

#### 10. OVHcloud
- 📍 **全球基础设施**: https://www.ovhcloud.com/en/about-us/global-infrastructure/
- 📍 **区域可用性**: https://www.ovhcloud.com/en/public-cloud/regions-availability/
- 📝 **建议更新频率**: 每年

#### 11. DigitalOcean
- 📍 **数据中心**: https://docs.digitalocean.com/products/platform/availability-matrix/
- 📍 **产品文档**: https://www.digitalocean.com/products/data-centers
- 📝 **建议更新频率**: 每年

---

## 🛠️ 快速校准步骤

### 方法一：手动校准（推荐）

```bash
# 1. 访问官方网站获取最新数据
# 2. 编辑对应的数据文件
vim data/aws/nodes.json

# 3. 验证JSON格式
python3 -m json.tool data/aws/nodes.json

# 4. 运行完整验证
python3 validate_data.py

# 5. 测试可视化效果
python3 serve.py
```

### 方法二：API方式（需要配置CLI）

```bash
# AWS
aws ec2 describe-regions --output json > /tmp/aws_regions.json
aws ec2 describe-availability-zones --output json > /tmp/aws_azs.json

# Azure
az account list-locations --output json > /tmp/azure_locations.json

# Google Cloud
gcloud compute regions list --format=json > /tmp/gcp_regions.json

# 阿里云
aliyun ecs DescribeRegions > /tmp/aliyun_regions.json
```

---

## 📋 数据校准检查清单

### 每个云服务商需要验证的内容：

- [ ] **节点数量**: 是否有新增或关闭的区域？
- [ ] **区域名称**: 官方名称是否有变化？
- [ ] **可用区数量**: 是否有新增的可用区？
- [ ] **地理位置**: 经纬度是否准确？
- [ ] **启用日期**: 新区域的上线时间
- [ ] **状态**: active/planned/retired
- [ ] **特殊标注**: 政府云、主权云、本地地域等

### 常见需要更新的情况：

1. **新区域上线** - 云服务商公告新数据中心
2. **可用区扩展** - 现有区域增加可用区
3. **区域更名** - 官方修改区域命名
4. **区域关闭** - 某些区域停止服务
5. **服务变更** - 特定服务在某区域的可用性

---

## 🔍 数据质量指标

### 当前数据质量评估

| 指标 | 状态 | 说明 |
|-----|------|------|
| **格式完整性** | ✅ 100% | 所有JSON文件格式正确 |
| **必需字段** | ✅ 100% | 所有节点包含必需字段 |
| **经纬度有效性** | ✅ 100% | 所有坐标在有效范围内 |
| **数据时效性** | ⚠️ 75% | 部分数据需要更新 |

### 建议优先更新的数据

1. **AWS** (2024-01-15) - 距今约10个月
2. **Azure** (2024-01-15) - 距今约10个月  
3. **Google Cloud** (2024-01-15) - 距今约10个月
4. **腾讯云** (2024-01-15) - 距今约10个月
5. **华为云** (2024-01-15) - 距今约10个月

---

## 📝 更新记录模板

在更新数据后，建议在此记录：

```markdown
### 更新日期: 2025-XX-XX
- **云服务商**: [名称]
- **更新内容**: [具体变更]
- **节点变化**: [新增/删除/修改的节点]
- **数据来源**: [官方链接]
- **验证方式**: [手动/API]
- **更新人**: [您的名字]
```

---

## 🆘 遇到问题？

### 常见问题

**Q1: 如何获取准确的经纬度？**
A: 使用 Google Maps 搜索城市，右键点击位置即可查看坐标

**Q2: 可用区数量如何确认？**
A: 查看官方文档或使用CLI命令查询

**Q3: 如何区分Region和Availability Zone？**
A: Region是地理区域（如us-west-1），AZ是Region内的独立数据中心

**Q4: 新区域何时添加到数据文件？**
A: 建议在官方正式GA（General Availability）后添加

---

## 🎯 下一步行动

1. **立即行动**: 
   - 检查 AWS、Azure、Google Cloud 三大云的最新区域
   - 更新超过6个月的数据

2. **定期维护**:
   - 每季度检查主流云服务商
   - 每半年检查中国云服务商
   - 每年检查其他云服务商

3. **自动化考虑**:
   - 编写脚本定期爬取官方数据
   - 设置提醒定期检查更新
   - 建立数据变更通知机制

---

**工具箱**:
- 📄 详细数据源: `DATA_SOURCES.md`
- 🔧 验证脚本: `validate_data.py`
- 📊 可视化测试: `python3 serve.py`

**最后更新**: 2025-10-23

