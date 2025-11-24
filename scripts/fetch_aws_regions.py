#!/usr/bin/env python3
"""
AWS Regions 和 Availability Zones 获取与对比脚本

使用 AWS CLI 的 lightsail get-regions 命令获取所有 region 和可用区，
并与现有的 data/aws/nodes.json 进行对比。

参考文档:
https://docs.aws.amazon.com/cli/latest/reference/lightsail/get-regions.html
"""

import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
AWS_NODES_FILE = PROJECT_ROOT / "data" / "aws" / "nodes.json"
OUTPUT_DIR = PROJECT_ROOT / "scripts" / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def check_aws_cli() -> bool:
    """检查 AWS CLI 是否已安装"""
    try:
        result = subprocess.run(
            ["aws", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ AWS CLI 已安装: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    except subprocess.TimeoutExpired:
        pass
    
    print("❌ AWS CLI 未安装")
    return False


def install_aws_cli_instructions():
    """显示 AWS CLI 安装说明"""
    print("\n" + "="*70)
    print("📦 AWS CLI 安装指南")
    print("="*70)
    print("\nmacOS (使用 Homebrew):")
    print("  brew install awscli")
    print("\n或者使用官方安装器:")
    print("  curl 'https://awscli.amazonaws.com/AWSCLIV2.pkg' -o 'AWSCLIV2.pkg'")
    print("  sudo installer -pkg AWSCLIV2.pkg -target /")
    print("\nLinux:")
    print("  curl 'https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip' -o 'awscliv2.zip'")
    print("  unzip awscliv2.zip")
    print("  sudo ./aws/install")
    print("\n配置 AWS CLI:")
    print("  aws configure")
    print("  输入 AWS Access Key ID 和 Secret Access Key")
    print("  注意: 对于只读操作，可以使用最小权限的 IAM 用户")
    print("\n" + "="*70 + "\n")


def fetch_lightsail_regions() -> Optional[Dict]:
    """使用 AWS CLI 获取 Lightsail regions 和可用区"""
    print("\n🔍 正在获取 AWS Lightsail regions 和可用区...")
    
    try:
        # 获取包含可用区的 regions
        result = subprocess.run(
            [
                "aws", "lightsail", "get-regions",
                "--include-availability-zones",
                "--output", "json"
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"❌ AWS CLI 命令执行失败:")
            print(f"   错误代码: {result.returncode}")
            print(f"   错误信息: {result.stderr}")
            if "Unable to locate credentials" in result.stderr:
                print("\n💡 提示: 请先配置 AWS 凭证:")
                print("   aws configure")
            return None
        
        data = json.loads(result.stdout)
        print(f"✅ 成功获取 {len(data.get('regions', []))} 个 regions")
        return data
        
    except subprocess.TimeoutExpired:
        print("❌ 请求超时")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")
        print(f"   输出: {result.stdout[:200]}")
        return None
    except Exception as e:
        print(f"❌ 获取数据失败: {e}")
        return None


def load_existing_nodes() -> Dict:
    """加载现有的 AWS nodes.json 文件"""
    try:
        with open(AWS_NODES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ 已加载现有数据: {len(data.get('nodes', []))} 个节点")
        return data
    except FileNotFoundError:
        print(f"⚠️  文件不存在: {AWS_NODES_FILE}")
        return {"nodes": []}
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")
        return {"nodes": []}


def normalize_region_name(region_name: str) -> str:
    """标准化 region 名称（用于对比）"""
    return region_name.lower().strip()


def compare_regions(lightsail_data: Dict, existing_data: Dict) -> Dict:
    """对比 Lightsail regions 和现有数据"""
    print("\n📊 开始对比分析...")
    
    # 从 Lightsail 数据中提取 regions
    lightsail_regions = {}
    for region in lightsail_data.get('regions', []):
        region_name = region.get('name', '')
        if not region_name:
            continue
        
        azs = []
        for az in region.get('availabilityZones', []):
            az_name = az.get('zoneName', '')
            if az_name:
                azs.append(az_name)
        
        lightsail_regions[normalize_region_name(region_name)] = {
            'name': region_name,
            'displayName': region.get('displayName', ''),
            'description': region.get('description', ''),
            'continentCode': region.get('continentCode', ''),
            'availabilityZones': sorted(azs),
            'az_count': len(azs)
        }
    
    # 从现有数据中提取 regions
    existing_regions = {}
    for node in existing_data.get('nodes', []):
        node_id = node.get('node_id', '')
        if not node_id:
            continue
        
        azs = node.get('availability_zones', [])
        existing_regions[normalize_region_name(node_id)] = {
            'node_id': node_id,
            'name': node.get('name', ''),
            'availabilityZones': sorted(azs),
            'az_count': len(azs),
            'location': node.get('location', {}),
            'status': node.get('status', ''),
            'launch_date': node.get('launch_date', '')
        }
    
    # 对比分析
    lightsail_set = set(lightsail_regions.keys())
    existing_set = set(existing_regions.keys())
    
    # 只在 Lightsail 中存在的 regions
    only_in_lightsail = lightsail_set - existing_set
    
    # 只在现有数据中存在的 regions
    only_in_existing = existing_set - lightsail_set
    
    # 两者都存在的 regions
    common_regions = lightsail_set & existing_set
    
    # 对比可用区
    az_differences = {}
    for region_name in common_regions:
        lightsail_azs = set(lightsail_regions[region_name]['availabilityZones'])
        existing_azs = set(existing_regions[region_name]['availabilityZones'])
        
        if lightsail_azs != existing_azs:
            az_differences[region_name] = {
                'lightsail_azs': sorted(lightsail_azs),
                'existing_azs': sorted(existing_azs),
                'only_in_lightsail': sorted(lightsail_azs - existing_azs),
                'only_in_existing': sorted(existing_azs - lightsail_azs)
            }
    
    return {
        'lightsail_regions': lightsail_regions,
        'existing_regions': existing_regions,
        'only_in_lightsail': sorted(only_in_lightsail),
        'only_in_existing': sorted(only_in_existing),
        'common_regions': sorted(common_regions),
        'az_differences': az_differences,
        'summary': {
            'lightsail_count': len(lightsail_regions),
            'existing_count': len(existing_regions),
            'common_count': len(common_regions),
            'only_in_lightsail_count': len(only_in_lightsail),
            'only_in_existing_count': len(only_in_existing),
            'az_diff_count': len(az_differences)
        }
    }


def generate_report(comparison: Dict, lightsail_data: Dict) -> str:
    """生成对比报告"""
    report_lines = []
    report_lines.append("="*70)
    report_lines.append("AWS Regions 和 Availability Zones 对比报告")
    report_lines.append("="*70)
    report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    
    summary = comparison['summary']
    report_lines.append("📊 统计摘要")
    report_lines.append("-"*70)
    report_lines.append(f"Lightsail Regions 总数: {summary['lightsail_count']}")
    report_lines.append(f"现有数据 Regions 总数: {summary['existing_count']}")
    report_lines.append(f"共同 Regions: {summary['common_count']}")
    report_lines.append(f"仅在 Lightsail 中: {summary['only_in_lightsail_count']}")
    report_lines.append(f"仅在现有数据中: {summary['only_in_existing_count']}")
    report_lines.append(f"可用区差异: {summary['az_diff_count']}")
    report_lines.append("")
    
    # 仅在 Lightsail 中的 regions
    if comparison['only_in_lightsail']:
        report_lines.append("🆕 仅在 Lightsail 中存在的 Regions")
        report_lines.append("-"*70)
        for region_name in comparison['only_in_lightsail']:
            region = comparison['lightsail_regions'][region_name]
            report_lines.append(f"  • {region['name']} ({region['displayName']})")
            report_lines.append(f"    可用区数量: {region['az_count']}")
            if region['availabilityZones']:
                report_lines.append(f"    可用区: {', '.join(region['availabilityZones'])}")
            report_lines.append("")
    
    # 仅在现有数据中的 regions
    if comparison['only_in_existing']:
        report_lines.append("📝 仅在现有数据中存在的 Regions")
        report_lines.append("-"*70)
        for region_name in comparison['only_in_existing']:
            region = comparison['existing_regions'][region_name]
            report_lines.append(f"  • {region['node_id']} ({region['name']})")
            report_lines.append(f"    可用区数量: {region['az_count']}")
            if region['availabilityZones']:
                report_lines.append(f"    可用区: {', '.join(region['availabilityZones'])}")
            report_lines.append("")
    
    # 可用区差异
    if comparison['az_differences']:
        report_lines.append("⚠️  可用区差异")
        report_lines.append("-"*70)
        for region_name, diff in comparison['az_differences'].items():
            report_lines.append(f"  Region: {region_name}")
            if diff['only_in_lightsail']:
                report_lines.append(f"    仅在 Lightsail 中: {', '.join(diff['only_in_lightsail'])}")
            if diff['only_in_existing']:
                report_lines.append(f"    仅在现有数据中: {', '.join(diff['only_in_existing'])}")
            report_lines.append("")
    
    # 共同 regions 的详细信息
    report_lines.append("✅ 共同 Regions 详情")
    report_lines.append("-"*70)
    for region_name in sorted(comparison['common_regions']):
        lightsail_region = comparison['lightsail_regions'][region_name]
        existing_region = comparison['existing_regions'][region_name]
        report_lines.append(f"  {lightsail_region['name']} ({lightsail_region['displayName']})")
        report_lines.append(f"    Lightsail 可用区: {lightsail_region['az_count']} 个")
        report_lines.append(f"    现有数据可用区: {existing_region['az_count']} 个")
        if lightsail_region['availabilityZones'] == existing_region['availabilityZones']:
            report_lines.append(f"    ✅ 可用区一致")
        report_lines.append("")
    
    report_lines.append("="*70)
    
    return "\n".join(report_lines)


def save_results(lightsail_data: Dict, comparison: Dict, report: str):
    """保存结果到文件"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 保存原始 Lightsail 数据
    lightsail_file = OUTPUT_DIR / f"aws_lightsail_regions_{timestamp}.json"
    with open(lightsail_file, 'w', encoding='utf-8') as f:
        json.dump(lightsail_data, f, indent=2, ensure_ascii=False)
    print(f"💾 Lightsail 数据已保存: {lightsail_file}")
    
    # 保存对比结果
    comparison_file = OUTPUT_DIR / f"aws_comparison_{timestamp}.json"
    with open(comparison_file, 'w', encoding='utf-8') as f:
        json.dump(comparison, f, indent=2, ensure_ascii=False)
    print(f"💾 对比结果已保存: {comparison_file}")
    
    # 保存报告
    report_file = OUTPUT_DIR / f"aws_comparison_report_{timestamp}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"💾 对比报告已保存: {report_file}")
    
    # 打印报告摘要
    print("\n" + report)


def main():
    """主函数"""
    print("="*70)
    print("AWS Regions 和 Availability Zones 获取与对比工具")
    print("="*70)
    
    # 检查 AWS CLI
    if not check_aws_cli():
        install_aws_cli_instructions()
        sys.exit(1)
    
    # 获取 Lightsail regions
    lightsail_data = fetch_lightsail_regions()
    if not lightsail_data:
        print("\n❌ 无法获取 Lightsail 数据，请检查 AWS CLI 配置")
        sys.exit(1)
    
    # 加载现有数据
    existing_data = load_existing_nodes()
    
    # 对比分析
    comparison = compare_regions(lightsail_data, existing_data)
    
    # 生成报告
    report = generate_report(comparison, lightsail_data)
    
    # 保存结果
    save_results(lightsail_data, comparison, report)
    
    print("\n✅ 完成！")


if __name__ == "__main__":
    main()

