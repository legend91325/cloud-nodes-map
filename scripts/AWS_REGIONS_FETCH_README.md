# AWS Regions 和 Availability Zones 获取与对比工具

这个脚本使用 AWS CLI 的 `lightsail get-regions` 命令获取所有 AWS regions 和可用区，并与现有的 `data/aws/nodes.json` 进行对比。

## 功能特性

- ✅ 自动检查 AWS CLI 是否安装
- ✅ 获取所有 AWS Lightsail regions 和可用区
- ✅ 与现有数据自动对比
- ✅ 生成详细的对比报告
- ✅ 保存原始数据和对比结果

## 前置要求

### 1. 安装 AWS CLI

#### macOS (推荐使用 Homebrew)

```bash
brew install awscli
```

#### macOS (使用官方安装器)

```bash
curl 'https://awscli.amazonaws.com/AWSCLIV2.pkg' -o 'AWSCLIV2.pkg'
sudo installer -pkg AWSCLIV2.pkg -target /
```

#### Linux

```bash
curl 'https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip' -o 'awscliv2.zip'
unzip awscliv2.zip
sudo ./aws/install
```

#### 验证安装

```bash
aws --version
```

### 2. 配置 AWS 凭证

```bash
aws configure
```

需要输入：
- **AWS Access Key ID**: 你的 AWS Access Key
- **AWS Secret Access Key**: 你的 Secret Key
- **Default region name**: 默认区域（如 `us-east-1`）
- **Default output format**: 输出格式（推荐 `json`）

#### 创建只读权限的 IAM 用户（推荐）

为了安全，建议创建一个只有只读权限的 IAM 用户：

1. 登录 AWS Console
2. 进入 IAM → Users → Add users
3. 创建新用户，选择 "Programmatic access"
4. 附加策略：`AmazonLightsailReadOnlyAccess` 或自定义策略：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "lightsail:GetRegions"
      ],
      "Resource": "*"
    }
  ]
}
```

5. 保存 Access Key ID 和 Secret Access Key
6. 使用这些凭证配置 AWS CLI

## 使用方法

### 运行脚本

```bash
# 从项目根目录运行
python3 scripts/fetch_aws_regions.py
```

或者：

```bash
# 直接运行（需要执行权限）
./scripts/fetch_aws_regions.py
```

### 输出文件

脚本会在 `scripts/output/` 目录下生成以下文件：

1. **`aws_lightsail_regions_YYYYMMDD_HHMMSS.json`**
   - 从 AWS CLI 获取的原始 Lightsail regions 数据

2. **`aws_comparison_YYYYMMDD_HHMMSS.json`**
   - 详细的对比分析结果（JSON 格式）

3. **`aws_comparison_report_YYYYMMDD_HHMMSS.txt`**
   - 人类可读的对比报告

## 报告内容

报告包含以下信息：

### 统计摘要
- Lightsail Regions 总数
- 现有数据 Regions 总数
- 共同 Regions 数量
- 仅在 Lightsail 中存在的 Regions
- 仅在现有数据中存在的 Regions
- 可用区差异数量

### 详细对比

1. **🆕 仅在 Lightsail 中存在的 Regions**
   - 列出所有在 Lightsail 中发现但不在现有数据中的 regions
   - 包含可用区信息

2. **📝 仅在现有数据中存在的 Regions**
   - 列出所有在现有数据中但不在 Lightsail 中的 regions
   - 可能包括：
     - GovCloud regions（`us-gov-east-1`, `us-gov-west-1`）
     - 其他特殊 regions

3. **⚠️ 可用区差异**
   - 对于共同存在的 regions，对比可用区列表
   - 显示仅在 Lightsail 中或仅在现有数据中的可用区

4. **✅ 共同 Regions 详情**
   - 列出所有共同存在的 regions
   - 显示可用区数量和一致性

## 注意事项

### Lightsail vs EC2 Regions

⚠️ **重要**: AWS Lightsail 的 regions 可能与 AWS EC2 的 regions 不完全一致。

- **Lightsail**: 是一个简化的云服务，只支持部分 regions
- **EC2**: AWS 的主要计算服务，支持更多 regions

因此，对比结果中可能会出现：
- 一些 EC2 regions 不在 Lightsail 中（如 GovCloud regions）
- Lightsail 可能不支持所有 EC2 的可用区

### 数据来源

- **Lightsail 数据**: 来自 AWS API，实时获取
- **现有数据**: 来自 `data/aws/nodes.json`，可能包含更全面的 EC2 regions

### 建议

1. 使用对比报告识别：
   - 新增的 regions（可能需要添加到数据中）
   - 可用区变化（可能需要更新）
   - 已废弃的 regions（可能需要标记）

2. 对于 Lightsail 中不存在的 regions，可以：
   - 使用 AWS EC2 API 获取更完整的数据
   - 参考 AWS 官方文档手动验证

## 故障排除

### 错误: "Unable to locate credentials"

**原因**: AWS CLI 未配置凭证

**解决**:
```bash
aws configure
```

### 错误: "Access Denied"

**原因**: IAM 用户没有足够权限

**解决**: 确保 IAM 用户有 `lightsail:GetRegions` 权限

### 错误: "aws: command not found"

**原因**: AWS CLI 未安装或不在 PATH 中

**解决**: 按照上面的安装指南安装 AWS CLI

## 参考文档

- [AWS CLI Lightsail get-regions 文档](https://docs.aws.amazon.com/cli/latest/reference/lightsail/get-regions.html)
- [AWS CLI 安装指南](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [AWS CLI 配置指南](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)

