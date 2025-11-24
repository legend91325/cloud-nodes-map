# 云服务商基础设施爬虫

这个目录包含多个爬虫脚本，用于从各个云服务商官方网站爬取全球基础设施数据，并生成符合项目数据格式的 `nodes.json` 文件。

## 可用的爬虫

- **阿里云爬虫** (`crawl_aliyun.py`) - 爬取阿里云全球基础设施数据
- **AWS爬虫** (`crawl_aws.py`) - 爬取AWS全球基础设施数据
- **Azure爬虫** (`crawl_azure.py`) - 爬取Azure全球基础设施数据

---

## 阿里云爬虫

### 功能特性

## 功能特性

- 自动爬取阿里云全球基础设施页面数据
- 解析区域信息（名称、可用区数量、推出年份等）
- 自动生成节点ID和可用区列表
- **使用公开API获取城市坐标**（OpenStreetMap Nominatim API）
- **使用公开API获取国家到大洲映射**（REST Countries API）
- 智能缓存机制，避免重复API请求
- 生成符合项目数据格式的JSON文件

## 安装依赖

```bash
cd web_crawler
pip install -r requirements.txt
```

## 使用方法

### 基本使用（使用API）

```bash
python crawl_aliyun.py
```

脚本会自动：
1. 访问阿里云全球基础设施页面
2. 解析页面数据
3. 使用OpenStreetMap API获取城市坐标
4. 使用REST Countries API获取国家大洲信息
5. 生成 `aliyun/nodes.json` 文件

**注意**：使用API模式会较慢（因为需要遵守API请求频率限制），但数据更准确。

### 快速模式（不使用API）

```bash
python crawl_aliyun.py --no-api
```

使用内置的备用数据，运行速度更快，适合快速测试。

### 自定义输出路径

```bash
python crawl_aliyun.py --output /path/to/output.json
```

### 命令行参数

- `--no-api`: 不使用API，使用备用数据（速度更快）
- `--output`: 指定输出文件路径
- `--help`: 显示帮助信息

### 输出文件

生成的 `aliyun/nodes.json` 文件结构如下：

```json
{
  "provider": "alibaba_cloud",
  "version": "1.0.6",
  "last_updated": "2025-01-XXTXX:XX:XX",
  "nodes": [
    {
      "location": {
        "country": "中国",
        "city": "北京",
        "latitude": 39.9042,
        "longitude": 116.4074,
        "continent": "亚洲"
      },
      "status": "active",
      "launch_date": "2013-01-01T00:00:00",
      "node_id": "cn-beijing",
      "name": "华北2（北京）",
      "availability_zones": [
        "cn-beijing-a",
        "cn-beijing-b",
        ...
      ]
    },
    ...
  ]
}
```

## 数据来源

- **主要来源**：https://www.alibabacloud.com/zh/global-locations
- **备用数据**：如果网页解析失败，脚本会使用已知的区域信息作为备用

## 使用的API服务

### 1. OpenStreetMap Nominatim API
- **用途**：获取城市的地理坐标（经纬度）
- **URL**：https://nominatim.openstreetmap.org
- **特点**：完全免费，无需API密钥
- **限制**：建议每秒最多1次请求（脚本已自动添加延迟）
- **文档**：https://nominatim.org/release-docs/latest/api/Overview/

### 2. REST Countries API
- **用途**：获取国家所属大洲信息
- **URL**：https://restcountries.com
- **特点**：完全免费，无需API密钥
- **文档**：https://restcountries.com/

### 缓存机制
- 脚本使用内存缓存，避免对同一城市/国家重复请求API
- 提高运行效率，减少API调用次数

## 注意事项

1. **网络连接**：确保能够访问阿里云官方网站
2. **解析准确性**：如果网页结构发生变化，可能需要更新解析逻辑
3. **可用区数量**：脚本会根据网页显示的可用区数量自动生成可用区ID列表
4. **坐标信息**：城市坐标信息来自内置映射表，如果遇到新城市可能需要手动添加

## 故障排除

### 问题：无法获取页面内容

**解决方案**：
- 检查网络连接
- 确认能够访问目标网站
- 尝试使用VPN（如果在某些地区）

### 问题：SSL证书验证失败

**错误信息**：`[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed`

**解决方案**：
- 脚本已自动处理SSL证书问题，如果验证失败会自动降级到禁用验证模式
- 如果需要永久解决，可以安装certifi包：
  ```bash
  pip install certifi
  ```
- 或者在macOS上运行：
  ```bash
  /Applications/Python\ 3.x/Install\ Certificates.command
  ```

### 问题：解析不到数据

**解决方案**：
- 脚本会自动使用备用数据
- 检查网页结构是否发生变化
- 可能需要更新解析逻辑

### 问题：坐标信息不准确

**解决方案**：
- 脚本会自动使用OpenStreetMap API获取坐标
- 如果API失败，会使用内置的备用坐标数据
- 对于特殊城市（如"硅谷"），脚本已做特殊处理

### 问题：API请求失败

**解决方案**：
- 检查网络连接
- 确认能够访问OpenStreetMap和REST Countries API
- 如果API服务不可用，脚本会自动使用备用数据
- 注意Nominatim API有请求频率限制（1秒1次）

---

## AWS爬虫

### 功能特性

- 自动爬取AWS全球基础设施页面数据
- 解析区域信息（名称、可用区数量、推出年份等）
- 自动生成节点ID和可用区列表
- **使用公开API获取城市坐标**（OpenStreetMap Nominatim API）
- **使用公开API获取国家到大洲映射**（REST Countries API）
- 智能缓存机制，避免重复API请求
- 生成符合项目数据格式的JSON文件

### 使用方法

```bash
# 使用API模式（推荐，数据更准确）
python crawl_aws.py

# 快速模式（不使用API，速度更快）
python crawl_aws.py --no-api

# 自定义输出路径
python crawl_aws.py --output /path/to/output.json
```

### 数据来源

- **主要来源**：https://aws.amazon.com/cn/about-aws/global-infrastructure/
- **备用数据**：如果网页解析失败，脚本会使用已知的区域信息作为备用

### 输出文件

生成的 `aws/nodes.json` 文件包含AWS的所有区域信息，包括：
- 37个AWS区域（包括GovCloud区域）
- 每个区域的可用区列表
- 地理坐标和大洲信息

---

## Azure爬虫

### 功能特性

- 自动爬取Azure全球基础设施页面数据
- 解析区域信息（名称、可用区数量、推出年份等）
- 自动生成节点ID和可用区列表
- **使用公开API获取城市坐标**（OpenStreetMap Nominatim API）
- **使用公开API获取国家到大洲映射**（REST Countries API）
- 智能缓存机制，避免重复API请求
- 生成符合项目数据格式的JSON文件

### 使用方法

```bash
# 使用API模式（推荐，数据更准确）
python crawl_azure.py

# 快速模式（不使用API，速度更快）
python crawl_azure.py --no-api

# 自定义输出路径
python crawl_azure.py --output /path/to/output.json
```

### 数据来源

- **主要来源**：https://datacenters.microsoft.com/globe/explore?view=table
- **备用数据**：如果网页解析失败，脚本会使用已知的区域信息作为备用

### 输出文件

生成的 `azure/nodes.json` 文件包含Azure的所有区域信息，包括：
- 47个Azure区域
- 每个区域的可用区列表
- 地理坐标和大洲信息

---

## 更新日志

### Azure爬虫 v1.0.6
- 初始版本
- 支持爬取Azure全球基础设施数据
- 自动生成节点ID和可用区列表
- 包含备用数据机制
- 支持47个Azure区域

### AWS爬虫 v1.1.6
- 初始版本
- 支持爬取AWS全球基础设施数据
- 自动生成节点ID和可用区列表
- 包含备用数据机制
- 支持37个AWS区域

### 阿里云爬虫 v1.0.6
- 初始版本
- 支持爬取阿里云全球基础设施数据
- 自动生成节点ID和可用区列表
- 包含备用数据机制

## 贡献

如果发现数据不准确或需要添加新功能，欢迎提交 Issue 或 Pull Request。

