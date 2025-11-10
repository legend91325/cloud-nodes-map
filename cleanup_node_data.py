#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理节点数据文件，移除不必要的属性
保留核心字段：node_id, name, location, availability_zones, status, launch_date
"""

import json
import os
from pathlib import Path
from datetime import datetime

# 需要保留的字段
KEEP_FIELDS = {
    'node_id',
    'name',
    'location',
    'availability_zones',
    'availability_zone',  # 兼容旧格式
    'status',
    'launch_date',
}

# 需要删除的字段
REMOVE_FIELDS = {
    'network_info',
    'service_types',
    'data_center',
    'description',
    'region',  # location 中可能存在的 region 字段
}

def clean_node(node):
    """清理单个节点数据"""
    cleaned = {}
    
    # 保留核心字段
    for field in KEEP_FIELDS:
        if field in node:
            cleaned[field] = node[field]
    
    # 清理 location 对象，移除 region 字段（如果存在）
    if 'location' in cleaned:
        location = cleaned['location'].copy()
        if 'region' in location:
            del location['region']
        cleaned['location'] = location
    
    return cleaned

def process_provider(provider_dir):
    """处理单个云服务商的数据文件"""
    nodes_file = provider_dir / 'nodes.json'
    
    if not nodes_file.exists():
        print(f"  ⚠️  文件不存在: {nodes_file}")
        return False
    
    try:
        # 读取数据
        with open(nodes_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 备份原文件
        backup_file = nodes_file.with_suffix('.json.bak')
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 清理节点数据
        original_count = len(data.get('nodes', []))
        cleaned_nodes = [clean_node(node) for node in data.get('nodes', [])]
        
        # 更新数据
        data['nodes'] = cleaned_nodes
        data['version'] = data.get('version', '1.0.0')
        if '.' in data['version']:
            parts = data['version'].split('.')
            parts[-1] = str(int(parts[-1]) + 1)
            data['version'] = '.'.join(parts)
        else:
            data['version'] = '1.1.0'
        data['last_updated'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        
        # 保存清理后的数据
        with open(nodes_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 统计删除的字段
        removed_stats = {}
        for node in data.get('nodes', []):
            for field in REMOVE_FIELDS:
                if field in node:
                    removed_stats[field] = removed_stats.get(field, 0) + 1
        
        print(f"  ✅ 处理完成: {original_count} 个节点")
        if removed_stats:
            print(f"     删除字段统计: {removed_stats}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 处理失败: {e}")
        return False

def main():
    """主函数"""
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║              节点数据清理 - 移除不必要属性                       ║")
    print("╚═══════════════════════════════════════════════════════════════════╝\n")
    
    data_dir = Path(__file__).parent / 'data'
    
    if not data_dir.exists():
        print(f"❌ 数据目录不存在: {data_dir}")
        return
    
    # 获取所有云服务商目录
    provider_dirs = [d for d in data_dir.iterdir() if d.is_dir() and (d / 'nodes.json').exists()]
    
    print(f"📁 找到 {len(provider_dirs)} 个云服务商数据文件\n")
    
    success_count = 0
    failed_count = 0
    
    for provider_dir in sorted(provider_dirs):
        provider_name = provider_dir.name
        print(f"处理: {provider_name}")
        
        if process_provider(provider_dir):
            success_count += 1
        else:
            failed_count += 1
        print()
    
    print("=" * 66)
    print(f"📊 清理完成: 成功 {success_count} 个，失败 {failed_count} 个")
    print("=" * 66)
    print("\n📝 说明:")
    print("  • 已删除字段: network_info, service_types, data_center, description, region")
    print("  • 保留字段: node_id, name, location, availability_zones, status, launch_date")
    print("  • 原文件已备份为 .json.bak")
    print("  • 版本号已自动递增")

if __name__ == '__main__':
    main()

