# 阿里云全球节点信息获取工具

## 功能说明

通过阿里云官方API获取全球节点信息，包括：
- 所有可用区域（Regions）
- 每个区域的可用区（Zones）
- 自动保存到JSON或CSV文件

## 安装依赖

```bash
pip install aliyun-python-sdk-core aliyun-python-sdk-ecs
```

## 使用方法

### 1. 凭据管理（可选）
首次使用前，可以运行凭据管理工具：
```bash
python manage_credentials.py
```

### 2. 运行主脚本
```bash
python aliyun_api_nodes.py
```

### 3. 认证信息处理
- 如果已保存凭据：脚本会询问是否使用已保存的凭据
- 如果未保存凭据：需要输入AccessKey ID和Secret，并询问是否保存

### 4. 选择保存格式
- JSON格式：完整的结构化数据
- CSV格式：扁平化的表格数据
- 两种格式都保存

## 输出文件

文件保存在 `output/` 目录下：
- `aliyun_nodes_complete.json` - JSON格式的完整数据
- `aliyun_nodes_complete.csv` - CSV格式的扁平化数据

## 数据格式

### JSON格式包含：
```json
{
  "regions": [...],
  "zones_by_region": {...},
  "fetch_time": "...",
  "total_regions": 25,
  "total_zones": 75
}
```

### CSV格式包含：
- region_id: 区域ID
- region_name: 区域名称
- zone_id: 可用区ID
- zone_name: 可用区名称
- zone_status: 可用区状态
- fetch_time: 获取时间

## 凭据管理

### 配置文件位置
凭据保存在用户主目录下的隐藏文件夹中：
- macOS/Linux: `~/.aliyun_config/credentials.json`
- Windows: `%USERPROFILE%\.aliyun_config\credentials.json`

### 安全性
- 配置文件权限设置为只有用户可读写（600）
- 凭据使用Base64编码存储（基本混淆，不是加密）
- 建议定期更换AccessKey

## 注意事项

1. **权限要求**：AccessKey需要有ECS服务的访问权限
2. **网络要求**：需要能够访问阿里云API
3. **数据更新**：每次运行都会获取最新的节点信息
4. **文件覆盖**：同名文件会被覆盖
5. **凭据安全**：请妥善保管AccessKey，不要分享给他人

## 故障排除

### API调用失败
- 检查AccessKey是否正确
- 确认AccessKey有ECS服务权限
- 检查网络连接

### 依赖安装失败
```bash
pip install --upgrade pip
pip install aliyun-python-sdk-core aliyun-python-sdk-ecs
``` 