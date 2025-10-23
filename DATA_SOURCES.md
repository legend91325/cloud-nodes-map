# 云服务商基础数据来源参考

## 📋 数据校准指南

本文档提供所有云服务商的官方数据源链接，用于校准和验证节点数据的准确性。

---

## 🌐 各云服务商官方数据源

### 1. AWS (Amazon Web Services)
**官方数据源：**
- 🔗 **区域和可用区**: https://aws.amazon.com/about-aws/global-infrastructure/regions_az/
- 🔗 **全球基础设施地图**: https://infrastructure.aws/
- 🔗 **区域列表 API**: https://docs.aws.amazon.com/general/latest/gr/rande.html
- 📍 **数据文件**: `data/aws/nodes.json`

**关键数据点：**
- Regions (区域)
- Availability Zones (可用区)
- Edge Locations (边缘节点)
- Local Zones (本地区域)

**校准要点：**
- AWS 官网提供最权威的区域和可用区信息
- 注意区分 Region、AZ、Local Zone、Edge Location
- 每个 Region 包含多个 AZ

---

### 2. Microsoft Azure
**官方数据源：**
- 🔗 **Azure 区域**: https://azure.microsoft.com/en-us/explore/global-infrastructure/geographies/
- 🔗 **全球基础设施**: https://datacenters.microsoft.com/globe/
- 🔗 **区域产品可用性**: https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/
- 🔗 **区域对**: https://docs.microsoft.com/en-us/azure/best-practices-availability-paired-regions
- 📍 **数据文件**: `data/azure/nodes.json`

**关键数据点：**
- Regions (区域)
- Availability Zones (可用区)
- Region Pairs (区域对)
- Geography (地理位置)

**校准要点：**
- Azure 有详细的区域文档
- 注意区分有 AZ 和无 AZ 的区域
- 某些区域配对用于灾备

---

### 3. Google Cloud Platform (GCP)
**官方数据源：**
- 🔗 **区域和可用区**: https://cloud.google.com/about/locations
- 🔗 **全球位置**: https://cloud.google.com/infrastructure/locations
- 🔗 **区域文档**: https://cloud.google.com/compute/docs/regions-zones
- 🔗 **网络地图**: https://cloud.google.com/about/locations#network
- 📍 **数据文件**: `data/google-cloud/nodes.json`

**关键数据点：**
- Regions (区域)
- Zones (可用区)
- Edge Points of Presence (边缘节点)
- Network Connectivity

**校准要点：**
- Google Cloud 使用 Region-Zone 命名规范
- 每个 Region 通常有 3 个 Zone
- 注意区分 Region 和 Multi-region

---

### 4. 阿里云 (Alibaba Cloud)
**官方数据源：**
- 🔗 **地域和可用区**: https://www.alibabacloud.com/help/zh/doc-detail/40654.htm
- 🔗 **全球基础设施**: https://www.alibabacloud.com/global-locations
- 🔗 **中国站**: https://help.aliyun.com/document_detail/40654.html
- 🔗 **产品地域可用性**: https://www.alibabacloud.com/help/zh/doc-detail/123712.htm
- 📍 **数据文件**: `data/alibaba-cloud/nodes.json`

**关键数据点：**
- 地域 (Region)
- 可用区 (Availability Zone)
- 本地地域 (Local Region)

**校准要点：**
- 阿里云中国站和国际站数据可能有差异
- 注意区分公共地域和本地地域
- 国内节点数据更详细

---

### 5. 腾讯云 (Tencent Cloud)
**官方数据源：**
- 🔗 **地域和可用区**: https://cloud.tencent.com/document/product/213/6091
- 🔗 **全球基础设施**: https://intl.cloud.tencent.com/document/product/213/6091
- 🔗 **国际版**: https://www.tencentcloud.com/document/product/213/6091
- 🔗 **产品可用地域**: https://cloud.tencent.com/document/product/213/15708
- 📍 **数据文件**: `data/tencent-cloud/nodes.json`

**关键数据点：**
- 地域 (Region)
- 可用区 (Available Zone)

**校准要点：**
- 腾讯云官网提供详细的地域文档
- 注意国内版和国际版的差异
- 某些地域可能有多个可用区

---

### 6. 华为云 (Huawei Cloud)
**官方数据源：**
- 🔗 **区域和可用区**: https://support.huaweicloud.com/usermanual-iaas/zh-cn_topic_0184026189.html
- 🔗 **全球基础设施**: https://www.huaweicloud.com/intl/en-us/global/
- 🔗 **国际站**: https://www.huaweicloud.com/intl/zh-cn/global/
- 🔗 **服务地域**: https://developer.huaweicloud.com/endpoint
- 📍 **数据文件**: `data/huawei-cloud/nodes.json`

**关键数据点：**
- 区域 (Region)
- 可用区 (Availability Zone)

**校准要点：**
- 华为云有详细的区域文档
- 注意国内和海外节点
- 某些服务在特定区域可用

---

### 7. 火山引擎 (Volcano Engine / ByteDance Cloud)
**官方数据源：**
- 🔗 **地域和可用区**: https://www.volcengine.com/docs/6396/69693
- 🔗 **全球基础设施**: https://www.volcengine.com/product
- 🔗 **控制台**: https://console.volcengine.com/
- 🔗 **服务地域**: https://www.volcengine.com/docs/6396/75753
- 📍 **数据文件**: `data/volcano-engine/nodes.json`

**关键数据点：**
- 地域 (Region)
- 可用区 (Availability Zone)

**校准要点：**
- 火山引擎是字节跳动的云服务
- 重点覆盖中国和亚太地区
- 数据可能更新较快，需定期校准

**⚠️ 注意**: 火山引擎数据可能需要登录账号才能查看完整信息

---

### 8. Oracle Cloud Infrastructure (OCI)
**官方数据源：**
- 🔗 **区域和可用域**: https://docs.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm
- 🔗 **全球区域**: https://www.oracle.com/cloud/data-regions/
- 🔗 **区域可用性**: https://docs.oracle.com/en-us/iaas/Content/General/Concepts/serviceavailability.htm
- 🔗 **基础设施**: https://www.oracle.com/cloud/architecture-and-regions/
- 📍 **数据文件**: `data/oracle-cloud/nodes.json`

**关键数据点：**
- Regions (区域)
- Availability Domains (可用域)
- Realms (领域)

**校准要点：**
- Oracle 使用 Availability Domain 而非 Zone
- 每个 Region 有 1-3 个 AD
- 注意 Government Cloud 和 Commercial Cloud

---

### 9. IBM Cloud
**官方数据源：**
- 🔗 **位置和数据中心**: https://www.ibm.com/cloud/data-centers
- 🔗 **区域和可用区**: https://cloud.ibm.com/docs/overview?topic=overview-locations
- 🔗 **全球位置**: https://www.ibm.com/cloud/locations
- 🔗 **服务位置**: https://cloud.ibm.com/docs/overview?topic=overview-services_region
- 📍 **数据文件**: `data/ibm-cloud/nodes.json`

**关键数据点：**
- Regions (区域)
- Zones (可用区)
- Data Centers (数据中心)
- Multi-Zone Regions (MZR)

**校准要点：**
- IBM Cloud 有详细的位置文档
- 区分 Classic Infrastructure 和 VPC Infrastructure
- 某些服务只在特定 MZR 可用

---

### 10. OVHcloud
**官方数据源：**
- 🔗 **数据中心位置**: https://www.ovhcloud.com/en/about-us/global-infrastructure/
- 🔗 **区域和可用区**: https://www.ovhcloud.com/en/public-cloud/regions-availability/
- 🔗 **全球网络**: https://www.ovhcloud.com/en/network/
- 🔗 **数据中心列表**: https://www.ovhcloud.com/en/about-us/data-centers/
- 📍 **数据文件**: `data/ovh-cloud/nodes.json`

**关键数据点：**
- Regions (区域)
- Data Centers (数据中心)
- Local Zones (本地区域)

**校准要点：**
- OVH 主要覆盖欧洲
- 有自己的数据中心网络
- 注意区分不同产品线的可用性

---

### 11. DigitalOcean
**官方数据源：**
- 🔗 **数据中心区域**: https://docs.digitalocean.com/products/platform/availability-matrix/
- 🔗 **全球基础设施**: https://www.digitalocean.com/products/data-centers
- 🔗 **产品可用性**: https://docs.digitalocean.com/products/
- 🔗 **区域 Slug**: https://docs.digitalocean.com/glossary/region-slug/
- 📍 **数据文件**: `data/digitalocean/nodes.json`

**关键数据点：**
- Regions (区域)
- Data Centers (数据中心)

**校准要点：**
- DigitalOcean 使用简单的命名规范
- 注意 Region Slug（如 nyc3, sfo2）
- 专注开发者市场

---

## 🛠️ 数据校准方法

### 手动校准步骤

1. **访问官方网站**
   - 打开上述对应云服务商的官方链接
   - 确保访问的是最新版本的文档

2. **记录关键信息**
   ```
   - Region ID（区域标识）
   - Region Name（区域名称）
   - Location（地理位置）
   - Country（国家）
   - City（城市）
   - Latitude & Longitude（经纬度）
   - Availability Zones（可用区数量）
   - Launch Date（启用日期）
   - Status（状态：active/planned/retired）
   ```

3. **更新数据文件**
   - 编辑对应的 `data/<provider>/nodes.json` 文件
   - 保持 JSON 格式正确
   - 验证数据完整性

4. **验证更新**
   ```bash
   python3 -m json.tool data/<provider>/nodes.json
   ```

### API 方式获取（推荐）

某些云服务商提供 API 查询区域信息：

**AWS CLI:**
```bash
aws ec2 describe-regions --output json
aws ec2 describe-availability-zones --output json
```

**Azure CLI:**
```bash
az account list-locations --output json
```

**Google Cloud:**
```bash
gcloud compute regions list
gcloud compute zones list
```

**阿里云 CLI:**
```bash
aliyun ecs DescribeRegions
aliyun ecs DescribeZones
```

---

## 📊 数据格式标准

### 统一的 JSON 格式

```json
{
  "provider": "provider_id",
  "version": "1.0.0",
  "last_updated": "2025-10-23T00:00:00",
  "nodes": [
    {
      "node_id": "region-id",
      "name": "区域名称",
      "location": {
        "country": "国家",
        "region": "大区",
        "city": "城市",
        "latitude": 纬度,
        "longitude": 经度
      },
      "data_center": "数据中心名称",
      "availability_zones": 可用区数量,
      "status": "active",
      "network_info": {
        "bandwidth": "100Gbps",
        "latency": 延迟毫秒,
        "uptime": 99.95
      },
      "description": "描述",
      "launch_date": "2020-01-01T00:00:00"
    }
  ]
}
```

---

## 🔍 数据验证工具

创建一个简单的验证脚本：

```python
import json
import os

def validate_provider_data(provider_id):
    file_path = f'data/{provider_id}/nodes.json'
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 验证必需字段
        required_fields = ['provider', 'version', 'nodes']
        for field in required_fields:
            if field not in data:
                print(f"❌ 缺少字段: {field}")
                return False
        
        # 验证节点数据
        for i, node in enumerate(data['nodes']):
            if 'node_id' not in node:
                print(f"❌ 节点 {i} 缺少 node_id")
                return False
            if 'location' not in node:
                print(f"❌ 节点 {i} 缺少 location")
                return False
        
        print(f"✅ {provider_id} 数据格式正确")
        print(f"   节点数: {len(data['nodes'])}")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON 格式错误: {e}")
        return False

# 验证所有提供商
providers = [
    'alibaba-cloud', 'aws', 'azure', 'google-cloud',
    'huawei-cloud', 'tencent-cloud', 'volcano-engine',
    'oracle-cloud', 'ibm-cloud', 'ovh-cloud', 'digitalocean'
]

for provider in providers:
    validate_provider_data(provider)
```

---

## 📝 数据更新日志模板

建议为每次数据更新创建日志：

```markdown
## 更新记录

### 2025-10-23
- 更新提供商: AWS
- 更新内容: 新增 ap-southeast-5 区域（马来西亚）
- 数据来源: https://aws.amazon.com/about-aws/whats-new/2025/10/aws-malaysia/
- 更新人: [您的名字]

### 2025-10-22
- 更新提供商: 阿里云
- 更新内容: 更新杭州可用区数量从 8 → 9
- 数据来源: https://help.aliyun.com/document_detail/40654.html
- 更新人: [您的名字]
```

---

## ⚠️ 注意事项

### 1. 数据时效性
- 云服务商会不断开设新区域
- 建议每季度更新一次数据
- 关注云服务商的官方公告

### 2. 数据准确性
- 优先使用官方文档数据
- 经纬度可使用 Google Maps 确认
- 可用区数量可能随时间变化

### 3. 命名规范
- 保持与官方命名一致
- 中文名称使用官方译名
- Region ID 使用官方标识符

### 4. 特殊情况
- 某些区域可能处于 Preview 状态
- 政府云和主权云区域可能有特殊要求
- Edge Location 和 Region 要区分清楚

---

## 🔗 其他参考资源

### 通用资源
- 📊 **Cloud Infrastructure Map**: https://www.cloudinfrastructuremap.com/
- 📊 **Cloud Comparison**: https://comparecloud.in/
- 📊 **Geekflare Cloud**: https://geekflare.com/cloud/

### 经纬度查询
- 🗺️ **LatLong.net**: https://www.latlong.net/
- 🗺️ **Google Maps**: https://www.google.com/maps
- 🗺️ **OpenStreetMap**: https://www.openstreetmap.org/

### 网络延迟测试
- ⚡ **CloudPing**: https://www.cloudping.info/
- ⚡ **GCPing**: https://gcping.com/
- ⚡ **AzureSpeed**: https://www.azurespeed.com/

---

## 📧 联系方式

如果在数据校准过程中遇到问题，可以：
1. 查阅官方文档的最新版本
2. 联系云服务商技术支持
3. 在社区论坛寻求帮助

---

**最后更新**: 2025-10-23  
**版本**: 1.0.0  
**维护者**: Cloud Nodes Map Project

