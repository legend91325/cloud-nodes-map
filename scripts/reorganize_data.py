#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云服务商数据重组脚本 - 按大洲排序并添加洲字段
"""

import json
import os
from collections import OrderedDict

# 国家到大洲的映射
COUNTRY_TO_CONTINENT = {
    # 亚洲 (Asia)
    '中国': '亚洲',
    '中国台湾': '亚洲',
    '日本': '亚洲',
    '韩国': '亚洲',
    '新加坡': '亚洲',
    '印度': '亚洲',
    '印度尼西亚': '亚洲',
    '马来西亚': '亚洲',
    '泰国': '亚洲',
    '菲律宾': '亚洲',
    '越南': '亚洲',
    '以色列': '亚洲',
    '阿联酋': '亚洲',
    '巴林': '亚洲',
    '沙特阿拉伯': '亚洲',
    '卡塔尔': '亚洲',
    
    # 欧洲 (Europe)
    '英国': '欧洲',
    '德国': '欧洲',
    '法国': '欧洲',
    '爱尔兰': '欧洲',
    '荷兰': '欧洲',
    '比利时': '欧洲',
    '瑞典': '欧洲',
    '瑞士': '欧洲',
    '西班牙': '欧洲',
    '意大利': '欧洲',
    '波兰': '欧洲',
    '芬兰': '欧洲',
    '挪威': '欧洲',
    '丹麦': '欧洲',
    '俄罗斯': '欧洲',
    
    # 北美洲 (North America)
    '美国': '北美洲',
    '加拿大': '北美洲',
    '墨西哥': '北美洲',
    
    # 南美洲 (South America)
    '巴西': '南美洲',
    '智利': '南美洲',
    '阿根廷': '南美洲',
    '哥伦比亚': '南美洲',
    
    # 非洲 (Africa)
    '南非': '非洲',
    '埃及': '非洲',
    '尼日利亚': '非洲',
    '肯尼亚': '非洲',
    
    # 大洋洲 (Oceania)
    '澳大利亚': '大洋洲',
    '新西兰': '大洋洲',
}

# 大洲排序优先级
CONTINENT_ORDER = {
    '亚洲': 1,
    '欧洲': 2,
    '北美洲': 3,
    '南美洲': 4,
    '非洲': 5,
    '大洋洲': 6,
}

def get_continent(country):
    """根据国家获取所属洲"""
    return COUNTRY_TO_CONTINENT.get(country, '未知')

def sort_nodes_by_continent(nodes):
    """按大洲和国家对节点排序"""
    # 为每个节点添加洲信息
    for node in nodes:
        country = node['location']['country']
        continent = get_continent(country)
        node['location']['continent'] = continent
    
    # 排序：先按洲，再按国家，最后按节点ID
    sorted_nodes = sorted(nodes, key=lambda x: (
        CONTINENT_ORDER.get(x['location']['continent'], 999),
        x['location']['country'],
        x.get('node_id', '')
    ))
    
    return sorted_nodes

def reorganize_provider_data(provider_id):
    """重组单个云服务商的数据"""
    file_path = f'data/{provider_id}/nodes.json'
    
    if not os.path.exists(file_path):
        print(f"⚠️  文件不存在: {file_path}")
        return False
    
    try:
        # 读取原始数据
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        original_count = len(data.get('nodes', []))
        
        # 排序节点
        sorted_nodes = sort_nodes_by_continent(data['nodes'])
        data['nodes'] = sorted_nodes
        
        # 统计各洲节点数
        continent_stats = {}
        for node in sorted_nodes:
            continent = node['location']['continent']
            continent_stats[continent] = continent_stats.get(continent, 0) + 1
        
        # 更新版本信息
        version_parts = data.get('version', '1.0.0').split('.')
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        data['version'] = '.'.join(version_parts)
        
        # 写回文件（保持格式化）
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {provider_id:20s} - {original_count:3d}个节点")
        for continent in sorted(continent_stats.keys(), key=lambda x: CONTINENT_ORDER.get(x, 999)):
            print(f"   └─ {continent}: {continent_stats[continent]}个")
        
        return True
        
    except Exception as e:
        print(f"❌ {provider_id} 处理失败: {e}")
        return False

def main():
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║         云服务商数据重组 - 按大洲排序并添加洲字段               ║")
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
    total_nodes = 0
    
    for provider in providers:
        if reorganize_provider_data(provider):
            success_count += 1
            # 统计总节点数
            try:
                with open(f'data/{provider}/nodes.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    total_nodes += len(data.get('nodes', []))
            except:
                pass
        print()
    
    print("="*66)
    print(f"📊 重组完成: {success_count}/{len(providers)} 个云服务商")
    print(f"📍 总节点数: {total_nodes}")
    print("="*66)
    
    print("\n✨ 所有数据已按大洲重新排序并添加洲字段！")
    print("💡 每个节点现在都包含 location.continent 字段")
    
    # 显示大洲列表
    print("\n📋 支持的大洲:")
    for continent, order in sorted(CONTINENT_ORDER.items(), key=lambda x: x[1]):
        print(f"   {order}. {continent}")

if __name__ == '__main__':
    main()

