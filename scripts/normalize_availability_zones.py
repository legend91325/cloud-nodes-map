#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一可用区数据格式为数组
将 availability_zone 和 availability_zones 统一为数组格式
"""

import json
import os
import re

def generate_availability_zones(region_id, zone_count=None, example_zone=None):
    """
    根据region ID和可用区数量生成可用区数组
    支持多种云服务商的命名规则
    """
    zones = []
    
    # 确定可用区数量
    if zone_count and zone_count > 0:
        count = int(zone_count)
    elif example_zone:
        # 有示例但没有数量，默认3个（大多数云服务商的标准）
        count = 3
    else:
        return []
    
    # 如果有示例可用区，优先使用示例来解析命名规则
    if example_zone and isinstance(example_zone, str):
        # 提取前缀：ap-east-1a -> ap-east-1
        match = re.match(r'^(.+?)([a-z]+\d*)$', example_zone)
        if match:
            region_prefix = match.group(1)
            # 根据示例生成可用区
            for i in range(count):
                if region_id.startswith('cn-'):
                    zones.append(f"{region_prefix}-{chr(ord('a') + i)}")
                else:
                    zones.append(f"{region_prefix}{chr(ord('a') + i)}")
            return zones
    
    # 根据region ID格式生成
    region_prefix = None
    
    # AWS/标准格式: us-east-1 -> us-east-1a, us-east-1b, us-east-1c
    if re.match(r'^[a-z]+-[a-z]+-\d+$', region_id):
        region_prefix = region_id
    # 阿里云格式: cn-beijing -> cn-beijing-a, cn-beijing-b
    elif re.match(r'^cn-[a-z]+$', region_id):
        region_prefix = region_id
    # 腾讯云/Azure格式: ap-shanghai-1 -> ap-shanghai-1a
    elif re.match(r'^[a-z]+-[a-z]+-\d+$', region_id):
        region_prefix = region_id
    # DigitalOcean格式: blr1, sgp1 -> blr1-a, sgp1-a
    elif re.match(r'^[a-z]+\d+$', region_id):
        region_prefix = region_id
    # IBM/OVH格式: ap-north, sgp -> ap-north-a, sgp-a
    elif re.match(r'^[a-z]+(-[a-z]+)?$', region_id):
        region_prefix = region_id
    else:
        # 无法识别的格式，尝试通用处理
        region_prefix = region_id
    
    if not region_prefix:
        return []
    
    # 根据云服务商类型生成可用区
    if region_id.startswith('cn-'):
        # 中国云服务商（阿里云等）：cn-beijing -> cn-beijing-a, cn-beijing-b
        for i in range(count):
            zone_suffix = chr(ord('a') + i)
            zones.append(f"{region_prefix}-{zone_suffix}")
    elif re.match(r'^[a-z]+\d+$', region_id):
        # DigitalOcean格式：blr1 -> blr1-a, blr1-b
        for i in range(count):
            zone_suffix = chr(ord('a') + i)
            zones.append(f"{region_prefix}-{zone_suffix}")
    elif '-' in region_id and re.search(r'\d', region_id):
        # 标准格式（AWS/Azure等）：us-east-1 -> us-east-1a, us-east-1b
        for i in range(count):
            zone_suffix = chr(ord('a') + i)
            zones.append(f"{region_prefix}{zone_suffix}")
    else:
        # 其他格式：简单追加后缀
        for i in range(count):
            zone_suffix = chr(ord('a') + i)
            zones.append(f"{region_prefix}-{zone_suffix}")
    
    return zones

def normalize_availability_zones(node):
    """标准化节点的可用区数据为数组格式"""
    region_id = node.get('node_id', '')
    
    # 检查现有字段
    zone_val = None
    zones_val = None
    
    if 'availability_zone' in node:
        zone_val = node.pop('availability_zone')
    if 'availability_zones' in node:
        zones_val = node.pop('availability_zones')
    
    zones = []
    
    if zone_val is not None:
        # 处理单数字段 (availability_zone)
        if isinstance(zone_val, str):
            # 字符串格式：示例可用区
            # 尝试根据region ID和常见数量生成完整列表
            zones = generate_availability_zones(region_id, zone_count=None, example_zone=zone_val)
            if not zones:
                # 如果无法生成，至少保留示例
                zones = [zone_val]
        elif isinstance(zone_val, list):
            zones = zone_val
    
    elif zones_val is not None:
        # 处理复数字段 (availability_zones)
        if isinstance(zones_val, list):
            zones = zones_val
        elif isinstance(zones_val, (int, float)):
            # 数字格式：可用区数量
            zone_count = int(zones_val)
            if zone_count > 0:
                zones = generate_availability_zones(region_id, zone_count=zone_count)
    
    # 统一设置为 availability_zones 数组
    node['availability_zones'] = zones if zones else []
    
    return node

def process_provider(provider_id):
    """处理单个云服务商的数据"""
    file_path = f'data/{provider_id}/nodes.json'
    
    if not os.path.exists(file_path):
        print(f"⚠️  文件不存在: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        nodes = data.get('nodes', [])
        original_format_count = {
            'availability_zone': 0,
            'availability_zones_number': 0,
            'availability_zones_array': 0,
            'none': 0
        }
        
        # 统计原始格式
        for node in nodes:
            if 'availability_zone' in node:
                original_format_count['availability_zone'] += 1
            elif 'availability_zones' in node:
                if isinstance(node['availability_zones'], list):
                    original_format_count['availability_zones_array'] += 1
                else:
                    original_format_count['availability_zones_number'] += 1
            else:
                original_format_count['none'] += 1
        
        # 标准化所有节点
        normalized_count = 0
        for node in nodes:
            normalize_availability_zones(node)
            normalized_count += 1
        
        # 更新版本号
        version_parts = data.get('version', '1.0.0').split('.')
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        data['version'] = '.'.join(version_parts)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 统计结果
        array_zones = sum(1 for node in nodes if isinstance(node.get('availability_zones'), list) and len(node.get('availability_zones', [])) > 0)
        empty_zones = sum(1 for node in nodes if not node.get('availability_zones') or len(node.get('availability_zones', [])) == 0)
        
        print(f"✅ {provider_id:20s} - {len(nodes):3d}个节点")
        print(f"   原始格式:")
        if original_format_count['availability_zone'] > 0:
            print(f"     - availability_zone (string): {original_format_count['availability_zone']}个")
        if original_format_count['availability_zones_number'] > 0:
            print(f"     - availability_zones (number): {original_format_count['availability_zones_number']}个")
        if original_format_count['availability_zones_array'] > 0:
            print(f"     - availability_zones (array): {original_format_count['availability_zones_array']}个")
        if original_format_count['none'] > 0:
            print(f"     - 无可用区字段: {original_format_count['none']}个")
        print(f"   标准化后:")
        print(f"     - 有可用区数组: {array_zones}个")
        print(f"     - 空数组: {empty_zones}个")
        
        return True
        
    except Exception as e:
        print(f"❌ {provider_id} 处理失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║           可用区数据格式标准化 - 统一为数组格式                 ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    providers = [
        'alibaba-cloud',
        'aws',
        'azure',
        'google-cloud',
        'huawei-cloud',
        'tencent-cloud',
        'volcano-engine',
        'oracle-cloud',
        'ibm-cloud',
        'ovh-cloud',
        'digitalocean'
    ]
    
    success_count = 0
    
    for provider in providers:
        if process_provider(provider):
            success_count += 1
        print()
    
    print("="*66)
    print(f"📊 标准化完成: {success_count}/{len(providers)} 个云服务商")
    print("="*66)
    
    print("\n✨ 所有可用区数据已统一为数组格式！")
    print("💡 字段统一为: availability_zones (数组)")

if __name__ == '__main__':
    main()

