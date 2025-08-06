#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云全球节点数据分析脚本
生成各种统计信息和可视化数据
"""

import json
import pandas as pd
from datetime import datetime
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
import seaborn as sns
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_data():
    """加载阿里云节点数据"""
    with open('data/alibaba-cloud/nodes.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def create_overview_report(data):
    """创建总览报告"""
    nodes = data['nodes']
    
    # 基础统计
    total_nodes = len(nodes)
    total_availability_zones = sum(node['availability_zones'] for node in nodes)
    
    # 按国家统计
    countries = Counter(node['location']['country'] for node in nodes)
    
    # 按地区统计
    regions = Counter(node['location']['region'] for node in nodes)
    
    # 按年份统计
    years = Counter()
    for node in nodes:
        year = datetime.fromisoformat(node['launch_date'].replace('Z', '+00:00')).year
        years[year] += 1
    
    # 生成地图数据
    map_data = []
    for node in nodes:
        map_data.append({
            'name': node['name'],
            'city': node['location']['city'],
            'country': node['location']['country'],
            'lat': node['location']['latitude'],
            'lng': node['location']['longitude'],
            'availability_zones': node['availability_zones'],
            'launch_date': node['launch_date'],
            'year': datetime.fromisoformat(node['launch_date'].replace('Z', '+00:00')).year
        })
    
    return {
        'total_nodes': total_nodes,
        'total_availability_zones': total_availability_zones,
        'countries': dict(countries),
        'regions': dict(regions),
        'years': dict(years),
        'map_data': map_data
    }

def create_timeline_analysis(data):
    """创建时间线分析"""
    nodes = data['nodes']
    
    # 按年份统计节点数量
    yearly_stats = defaultdict(lambda: {'count': 0, 'availability_zones': 0, 'nodes': []})
    
    for node in nodes:
        launch_date = datetime.fromisoformat(node['launch_date'].replace('Z', '+00:00'))
        year = launch_date.year
        
        yearly_stats[year]['count'] += 1
        yearly_stats[year]['availability_zones'] += node['availability_zones']
        yearly_stats[year]['nodes'].append({
            'name': node['name'],
            'country': node['location']['country'],
            'city': node['location']['city'],
            'availability_zones': node['availability_zones']
        })
    
    # 转换为DataFrame用于分析
    timeline_data = []
    cumulative_nodes = 0
    cumulative_azs = 0
    
    for year in sorted(yearly_stats.keys()):
        stats = yearly_stats[year]
        cumulative_nodes += stats['count']
        cumulative_azs += stats['availability_zones']
        
        timeline_data.append({
            'year': year,
            'new_nodes': stats['count'],
            'new_availability_zones': stats['availability_zones'],
            'cumulative_nodes': cumulative_nodes,
            'cumulative_availability_zones': cumulative_azs,
            'nodes': stats['nodes']
        })
    
    return timeline_data

def create_geographic_analysis(data):
    """创建地理分布分析"""
    nodes = data['nodes']
    
    # 按大洲统计
    continent_mapping = {
        '中国': '亚洲',
        '新加坡': '亚洲',
        '马来西亚': '亚洲',
        '印度尼西亚': '亚洲',
        '菲律宾': '亚洲',
        '泰国': '亚洲',
        '日本': '亚洲',
        '韩国': '亚洲',
        '印度': '亚洲',
        '美国': '北美洲',
        '墨西哥': '北美洲',
        '德国': '欧洲',
        '英国': '欧洲',
        '阿联酋': '亚洲',
        '沙特阿拉伯': '亚洲',
        '澳大利亚': '大洋洲'
    }
    
    continents = Counter()
    for node in nodes:
        country = node['location']['country']
        continent = continent_mapping.get(country, '其他')
        continents[continent] += node['availability_zones']
    
    return dict(continents)

def generate_reports():
    """生成所有报告"""
    print("正在加载阿里云节点数据...")
    data = load_data()
    
    print("正在生成总览报告...")
    overview = create_overview_report(data)
    
    print("正在生成时间线分析...")
    timeline = create_timeline_analysis(data)
    
    print("正在生成地理分布分析...")
    geographic = create_geographic_analysis(data)
    
    # 保存总览报告
    with open('docs/alibaba_cloud_overview.json', 'w', encoding='utf-8') as f:
        json.dump(overview, f, ensure_ascii=False, indent=2)
    
    # 保存时间线数据
    with open('docs/alibaba_cloud_timeline.json', 'w', encoding='utf-8') as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)
    
    # 保存地图数据
    with open('docs/alibaba_cloud_map_data.json', 'w', encoding='utf-8') as f:
        json.dump(overview['map_data'], f, ensure_ascii=False, indent=2)
    
    # 生成Markdown报告
    generate_markdown_reports(overview, timeline, geographic)
    
    print("所有报告已生成完成！")

def generate_markdown_reports(overview, timeline, geographic):
    """生成Markdown格式的报告"""
    
    # 总览报告
    overview_md = f"""# 阿里云全球节点总览报告

## 基础统计信息

- **总节点数量**: {overview['total_nodes']} 个
- **总可用区数量**: {overview['total_availability_zones']} 个
- **覆盖国家/地区**: {len(overview['countries'])} 个
- **覆盖地理区域**: {len(overview['regions'])} 个

## 按国家分布

| 国家/地区 | 节点数量 | 可用区数量 |
|-----------|----------|------------|
"""
    
    for country, count in sorted(overview['countries'].items(), key=lambda x: x[1], reverse=True):
        az_count = sum(node['availability_zones'] for node in overview['map_data'] if node['country'] == country)
        overview_md += f"| {country} | {count} | {az_count} |\n"
    
    overview_md += f"""
## 按地区分布

| 地区 | 节点数量 |
|------|----------|
"""
    
    for region, count in sorted(overview['regions'].items(), key=lambda x: x[1], reverse=True):
        overview_md += f"| {region} | {count} |\n"
    
    overview_md += f"""
## 按年份分布

| 年份 | 新增节点数 |
|------|------------|
"""
    
    for year, count in sorted(overview['years'].items()):
        overview_md += f"| {year} | {count} |\n"
    
    with open('docs/alibaba_cloud_overview.md', 'w', encoding='utf-8') as f:
        f.write(overview_md)
    
    # 时间线报告
    timeline_md = """# 阿里云全球节点发展时间线

## 年度发展统计

| 年份 | 新增节点 | 新增可用区 | 累计节点 | 累计可用区 |
|------|----------|------------|----------|------------|
"""
    
    for entry in timeline:
        timeline_md += f"| {entry['year']} | {entry['new_nodes']} | {entry['new_availability_zones']} | {entry['cumulative_nodes']} | {entry['cumulative_availability_zones']} |\n"
    
    timeline_md += "\n## 年度新增节点详情\n\n"
    
    for entry in timeline:
        if entry['new_nodes'] > 0:
            timeline_md += f"### {entry['year']}年\n\n"
            for node in entry['nodes']:
                timeline_md += f"- **{node['name']}** ({node['country']} {node['city']}) - {node['availability_zones']}个可用区\n"
            timeline_md += "\n"
    
    with open('docs/alibaba_cloud_timeline.md', 'w', encoding='utf-8') as f:
        f.write(timeline_md)
    
    # 地理分布报告
    geographic_md = """# 阿里云全球节点地理分布分析

## 按大洲分布

| 大洲 | 可用区数量 |
|------|------------|
"""
    
    for continent, az_count in sorted(geographic.items(), key=lambda x: x[1], reverse=True):
        geographic_md += f"| {continent} | {az_count} |\n"
    
    with open('docs/alibaba_cloud_geographic.md', 'w', encoding='utf-8') as f:
        f.write(geographic_md)

if __name__ == "__main__":
    generate_reports() 