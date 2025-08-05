# 腾讯云节点信息获取工具

这个工具用于获取腾讯云全球各个区域和可用区的信息，参考了阿里云节点获取工具的实现方式。

## 功能特性

- 🔍 获取腾讯云全球所有区域信息
- 🏢 获取每个区域的可用区信息
- 💾 支持保存为JSON和CSV格式
- 🔐 支持凭据管理和安全存储
- 📊 按大洲分组显示节点信息
- 🛡️ 完整的错误处理和日志记录

## 安装依赖

```bash
pip install tencentcloud-sdk-python
```

或者安装所有依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 配置腾讯云凭据

#### 方法一：环境变量（推荐）
```bash
export TENCENTCLOUD_SECRET_ID="你的SecretId"
export TENCENTCLOUD_SECRET_KEY="你的SecretKey"
```

#### 方法二：配置文件
在 `~/.tencentcloud/credentials` 文件中配置：
```ini
[default]
secret_id = 你的SecretId
secret_key = 你的SecretKey
```

#### 方法三：运行时输入
运行程序时会提示输入凭据，并可以选择保存供下次使用。

### 2. 运行程序

```bash
python tencentcloud_api_nodes.py
```

### 3. 简单测试

```bash
python tencentcloud_simple_test.py
```

## 输出格式

### JSON格式
```json
{
  "regions": [
    {
      "region_id": "ap-guangzhou",
      "region_name": "广州",
      "region_state": "AVAILABLE",
      "fetch_time": "2024-01-01T12:00:00"
    }
  ],
  "zones_by_region": {
    "ap-guangzhou": [
      {
        "zone_id": "ap-guangzhou-1",
        "zone_name": "广州一区",
        "zone_state": "AVAILABLE",
        "region_id": "ap-guangzhou",
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
| ap-guangzhou | 广州 | AVAILABLE | | | | 2024-01-01T12:00:00 |
| ap-guangzhou | 广州 | AVAILABLE | ap-guangzhou-1 | 广州一区 | AVAILABLE | 2024-01-01T12:00:00 |

## 腾讯云区域说明

腾讯云的区域命名规则：
- `ap-*`: 亚太地区
  - `ap-guangzhou`: 广州
  - `ap-shenzhen`: 深圳
  - `ap-shanghai`: 上海
  - `ap-beijing`: 北京
  - `ap-hongkong`: 香港
  - `ap-seoul`: 首尔
  - `ap-tokyo`: 东京
  - `ap-singapore`: 新加坡
  - `ap-bangkok`: 曼谷
  - `ap-mumbai`: 孟买
- `na-*`: 北美地区
  - `na-siliconvalley`: 硅谷
  - `na-ashburn`: 弗吉尼亚
- `eu-*`: 欧洲地区
  - `eu-frankfurt`: 法兰克福
- `sa-*`: 南美地区
  - `sa-saopaulo`: 圣保罗

## 注意事项

1. **权限要求**: 需要腾讯云API访问权限，建议使用只读权限的API密钥
2. **网络要求**: 需要能够访问腾讯云API的网络环境
3. **频率限制**: 腾讯云API有调用频率限制，程序已内置适当的延迟
4. **数据准确性**: 获取的数据为实时数据，区域和可用区状态可能会变化

## 错误处理

程序包含完整的错误处理机制：
- SDK安装检查
- 凭据验证
- API调用异常处理
- 网络连接问题处理
- 数据格式验证

## 与阿里云工具对比

| 特性 | 阿里云工具 | 腾讯云工具 |
|------|------------|------------|
| SDK | aliyun-python-sdk-core | tencentcloud-sdk-python |
| 认证方式 | AccessKey/SecretKey | SecretId/SecretKey |
| 配置文件 | ~/.aliyun/config.json | ~/.tencentcloud/credentials |
| 环境变量 | ALIBABA_CLOUD_ACCESS_KEY_ID | TENCENTCLOUD_SECRET_ID |
| API版本 | 2014-05-26 | 2017-03-12 |
| 默认区域 | cn-hangzhou | ap-guangzhou |

## 开发说明

### 主要类说明

- `TencentCloudConfig`: 腾讯云配置管理类
- `TencentCloudAPINodes`: 腾讯云API节点获取类

### 扩展功能

可以基于此工具扩展更多功能：
- 获取实例信息
- 获取网络配置
- 获取存储信息
- 监控数据获取
- 成本分析等

## 许可证

本项目遵循MIT许可证。 