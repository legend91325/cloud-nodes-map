# 华为云节点信息获取工具

这个工具用于获取华为云全球各个区域和可用区的信息，参考了阿里云和腾讯云节点获取工具的实现方式。

## 功能特性

- 🔍 获取华为云全球所有区域信息
- 🏢 获取每个区域的可用区信息
- 💾 支持保存为JSON和CSV格式
- 🔐 支持凭据管理和安全存储
- 📊 按大洲分组显示节点信息
- 🛡️ 完整的错误处理和日志记录

## 安装依赖

```bash
pip install huaweicloudsdkcore huaweicloudsdkecs
```

或者安装所有依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 配置华为云凭据

#### 方法一：环境变量（推荐）
```bash
export HUAWEICLOUD_ACCESS_KEY_ID="你的AccessKey ID"
export HUAWEICLOUD_SECRET_ACCESS_KEY="你的SecretAccessKey"
export HUAWEICLOUD_PROJECT_ID="你的Project ID"  # 可选
```

#### 方法二：配置文件
在 `~/.huaweicloud/credentials` 文件中配置：
```ini
[default]
access_key_id = 你的AccessKey ID
secret_access_key = 你的SecretAccessKey
project_id = 你的Project ID  # 可选
```

#### 方法三：运行时输入
运行程序时会提示输入凭据，并可以选择保存供下次使用。

### 2. 运行程序

```bash
python huaweicloud_api_nodes.py
```

### 3. 简单测试

```bash
python huaweicloud_simple_test.py
```

## 输出格式

### JSON格式
```json
{
  "regions": [
    {
      "region_id": "cn-north-4",
      "region_name": "华北-北京四",
      "region_state": "available",
      "fetch_time": "2024-01-01T12:00:00"
    }
  ],
  "zones_by_region": {
    "cn-north-4": [
      {
        "zone_id": "cn-north-4a",
        "zone_name": "cn-north-4a",
        "zone_state": "available",
        "region_id": "cn-north-4",
        "fetch_time": "2024-01-01T12:00:00"
      }
    ]
  },
  "fetch_time": "2024-01-01T12:00:00",
  "total_regions": 1,
  "total_zones": 1
}
```

### CSV格式
| region_id | region_name | region_state | zone_id | zone_name | zone_state | fetch_time |
|-----------|-------------|--------------|---------|-----------|------------|------------|
| cn-north-4 | 华北-北京四 | available | | | | 2024-01-01T12:00:00 |
| cn-north-4 | 华北-北京四 | available | cn-north-4a | cn-north-4a | available | 2024-01-01T12:00:00 |

## 华为云区域说明

华为云的区域命名规则：
- `cn-*`: 中国地区
  - `cn-north-1`: 华北-北京一
  - `cn-north-2`: 华北-北京二
  - `cn-north-4`: 华北-北京四
  - `cn-east-2`: 华东-上海二
  - `cn-east-3`: 华东-上海一
  - `cn-south-1`: 华南-广州
  - `cn-southwest-2`: 西南-贵阳一
- `ap-*`: 亚太地区
  - `ap-southeast-1`: 中国-香港
  - `ap-southeast-2`: 亚太-曼谷
  - `ap-southeast-3`: 亚太-新加坡
  - `ap-southeast-4`: 亚太-雅加达
  - `ap-southeast-5`: 亚太-孟买
  - `ap-southeast-6`: 亚太-吉隆坡
  - `ap-southeast-7`: 亚太-马尼拉
  - `ap-southeast-8`: 亚太-东京
  - `ap-southeast-9`: 亚太-大阪
  - `ap-southeast-10`: 亚太-首尔
- `eu-*`: 欧洲地区
  - `eu-west-0`: 欧洲-巴黎
  - `eu-west-101`: 欧洲-巴黎二
  - `eu-west-200`: 欧洲-巴黎三
  - `eu-north-0`: 欧洲-斯德哥尔摩
  - `eu-north-200`: 欧洲-斯德哥尔摩二
- `na-*`: 北美地区
  - `na-mexico-1`: 拉美-墨西哥城一
  - `na-mexico-2`: 拉美-墨西哥城二
- `sa-*`: 南美地区
  - `sa-brazil-1`: 拉美-圣保罗一
- `af-*`: 非洲地区
  - `af-south-1`: 非洲-约翰内斯堡

## 注意事项

1. **权限要求**: 需要华为云API访问权限，建议使用只读权限的API密钥
2. **网络要求**: 需要能够访问华为云API的网络环境
3. **频率限制**: 华为云API有调用频率限制，程序已内置适当的延迟
4. **数据准确性**: 获取的数据为实时数据，区域和可用区状态可能会变化
5. **Project ID**: 华为云需要Project ID，可以在华为云控制台获取

## 错误处理

程序包含完整的错误处理机制：
- SDK安装检查
- 凭据验证
- API调用异常处理
- 网络连接问题处理
- 数据格式验证

## 与阿里云、腾讯云工具对比

| 特性 | 阿里云工具 | 腾讯云工具 | 华为云工具 |
|------|------------|------------|------------|
| SDK | aliyun-python-sdk-core | tencentcloud-sdk-python | huaweicloudsdkcore |
| 认证方式 | AccessKey/SecretKey | SecretId/SecretKey | AccessKey/SecretKey |
| 配置文件 | ~/.aliyun/config.json | ~/.tencentcloud/credentials | ~/.huaweicloud/credentials |
| 环境变量 | ALIBABA_CLOUD_ACCESS_KEY_ID | TENCENTCLOUD_SECRET_ID | HUAWEICLOUD_ACCESS_KEY_ID |
| API版本 | 2014-05-26 | 2017-03-12 | v2 |
| 默认区域 | cn-hangzhou | ap-guangzhou | cn-north-4 |
| 特殊要求 | 无 | 无 | 需要Project ID |

## 开发说明

### 主要类说明

- `HuaweiCloudConfig`: 华为云配置管理类
- `HuaweiCloudAPINodes`: 华为云API节点获取类

### 扩展功能

可以基于此工具扩展更多功能：
- 获取实例信息
- 获取网络配置
- 获取存储信息
- 监控数据获取
- 成本分析等

## 许可证

本项目遵循MIT许可证。 