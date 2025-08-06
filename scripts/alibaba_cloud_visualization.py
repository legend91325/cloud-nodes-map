#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云全球节点数据可视化脚本
生成各种图表和可视化内容
"""

import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
import seaborn as sns
import numpy as np
from datetime import datetime
import pandas as pd

# 设置中文字体和样式
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")
plt.style.use('seaborn-v0_8')

def load_data():
    """加载分析数据"""
    with open('docs/alibaba_cloud_overview.json', 'r', encoding='utf-8') as f:
        overview = json.load(f)
    
    with open('docs/alibaba_cloud_timeline.json', 'r', encoding='utf-8') as f:
        timeline = json.load(f)
    
    return overview, timeline

def create_timeline_chart(timeline_data):
    """创建时间线图表"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    years = [entry['year'] for entry in timeline_data]
    new_nodes = [entry['new_nodes'] for entry in timeline_data]
    cumulative_nodes = [entry['cumulative_nodes'] for entry in timeline_data]
    new_azs = [entry['new_availability_zones'] for entry in timeline_data]
    cumulative_azs = [entry['cumulative_availability_zones'] for entry in timeline_data]
    
    # 新增节点数量
    bars1 = ax1.bar(years, new_nodes, color='skyblue', alpha=0.7, label='新增节点')
    ax1.set_title('阿里云全球节点年度新增数量', fontsize=16, fontweight='bold')
    ax1.set_ylabel('新增节点数量', fontsize=12)
    ax1.set_xlabel('年份', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # 添加数值标签
    for bar, value in zip(bars1, new_nodes):
        if value > 0:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    str(value), ha='center', va='bottom', fontweight='bold')
    
    # 累计节点数量
    ax1_twin = ax1.twinx()
    line1 = ax1_twin.plot(years, cumulative_nodes, 'r-', linewidth=3, marker='o', 
                          markersize=8, label='累计节点')
    ax1_twin.set_ylabel('累计节点数量', fontsize=12, color='red')
    ax1_twin.tick_params(axis='y', labelcolor='red')
    
    # 图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    # 可用区数量
    bars2 = ax2.bar(years, new_azs, color='lightgreen', alpha=0.7, label='新增可用区')
    ax2.set_title('阿里云全球可用区年度新增数量', fontsize=16, fontweight='bold')
    ax2.set_ylabel('新增可用区数量', fontsize=12)
    ax2.set_xlabel('年份', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # 添加数值标签
    for bar, value in zip(bars2, new_azs):
        if value > 0:
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    str(value), ha='center', va='bottom', fontweight='bold')
    
    # 累计可用区数量
    ax2_twin = ax2.twinx()
    line2 = ax2_twin.plot(years, cumulative_azs, 'purple', linewidth=3, marker='s', 
                          markersize=8, label='累计可用区')
    ax2_twin.set_ylabel('累计可用区数量', fontsize=12, color='purple')
    ax2_twin.tick_params(axis='y', labelcolor='purple')
    
    # 图例
    lines3, labels3 = ax2.get_legend_handles_labels()
    lines4, labels4 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines3 + lines4, labels3 + labels4, loc='upper left')
    
    plt.tight_layout()
    plt.savefig('docs/alibaba_cloud_timeline.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_geographic_chart(overview_data):
    """创建地理分布图表"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # 按国家分布
    countries = list(overview_data['countries'].keys())
    counts = list(overview_data['countries'].values())
    
    # 只显示前10个国家
    if len(countries) > 10:
        sorted_data = sorted(zip(countries, counts), key=lambda x: x[1], reverse=True)
        countries = [x[0] for x in sorted_data[:10]]
        counts = [x[1] for x in sorted_data[:10]]
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(countries)))
    bars1 = ax1.barh(countries, counts, color=colors)
    ax1.set_title('阿里云全球节点按国家分布', fontsize=16, fontweight='bold')
    ax1.set_xlabel('节点数量', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # 添加数值标签
    for bar, count in zip(bars1, counts):
        ax1.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                str(count), ha='left', va='center', fontweight='bold')
    
    # 按地区分布
    regions = list(overview_data['regions'].keys())
    region_counts = list(overview_data['regions'].values())
    
    # 只显示前8个地区
    if len(regions) > 8:
        sorted_data = sorted(zip(regions, region_counts), key=lambda x: x[1], reverse=True)
        regions = [x[0] for x in sorted_data[:8]]
        region_counts = [x[1] for x in sorted_data[:8]]
    
    colors2 = plt.cm.Pastel1(np.linspace(0, 1, len(regions)))
    wedges, texts, autotexts = ax2.pie(region_counts, labels=regions, autopct='%1.1f%%', 
                                       colors=colors2, startangle=90)
    ax2.set_title('阿里云全球节点按地区分布', fontsize=16, fontweight='bold')
    
    # 设置文本样式
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.tight_layout()
    plt.savefig('docs/alibaba_cloud_geographic.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_growth_analysis_chart(timeline_data):
    """创建增长分析图表"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    years = [entry['year'] for entry in timeline_data]
    cumulative_nodes = [entry['cumulative_nodes'] for entry in timeline_data]
    cumulative_azs = [entry['cumulative_availability_zones'] for entry in timeline_data]
    
    # 双Y轴图表
    ax1 = ax
    ax2 = ax1.twinx()
    
    # 节点数量
    line1 = ax1.plot(years, cumulative_nodes, 'b-', linewidth=3, marker='o', 
                     markersize=8, label='累计节点数量')
    ax1.set_xlabel('年份', fontsize=12)
    ax1.set_ylabel('累计节点数量', fontsize=12, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.grid(True, alpha=0.3)
    
    # 可用区数量
    line2 = ax2.plot(years, cumulative_azs, 'r-', linewidth=3, marker='s', 
                     markersize=8, label='累计可用区数量')
    ax2.set_ylabel('累计可用区数量', fontsize=12, color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    
    # 添加数据标签
    for i, (year, nodes, azs) in enumerate(zip(years, cumulative_nodes, cumulative_azs)):
        ax1.annotate(f'{nodes}', (year, nodes), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=9, fontweight='bold')
        ax2.annotate(f'{azs}', (year, azs), textcoords="offset points", 
                    xytext=(0,-15), ha='center', fontsize=9, fontweight='bold', color='red')
    
    # 图例
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')
    
    ax1.set_title('阿里云全球基础设施增长趋势', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('docs/alibaba_cloud_growth.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_summary_infographic(overview_data, timeline_data):
    """创建总结信息图"""
    fig = plt.figure(figsize=(16, 12))
    
    # 创建网格布局
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. 总览统计
    ax1 = fig.add_subplot(gs[0, :])
    ax1.axis('off')
    
    stats_text = f"""
    阿里云全球基础设施总览
    
    总节点数量: {overview_data['total_nodes']} 个
    总可用区数量: {overview_data['total_availability_zones']} 个
    覆盖国家/地区: {len(overview_data['countries'])} 个
    覆盖地理区域: {len(overview_data['regions'])} 个
    发展时间跨度: {min(overview_data['years'].keys())} - {max(overview_data['years'].keys())} 年
    """
    
    ax1.text(0.5, 0.5, stats_text, transform=ax1.transAxes, fontsize=16, 
             ha='center', va='center', fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    
    # 2. 年度新增趋势
    ax2 = fig.add_subplot(gs[1, 0])
    years = [entry['year'] for entry in timeline_data]
    new_nodes = [entry['new_nodes'] for entry in timeline_data]
    ax2.bar(years, new_nodes, color='skyblue', alpha=0.7)
    ax2.set_title('年度新增节点', fontsize=12, fontweight='bold')
    ax2.set_xlabel('年份')
    ax2.set_ylabel('新增数量')
    ax2.tick_params(axis='x', rotation=45)
    
    # 3. 国家分布
    ax3 = fig.add_subplot(gs[1, 1])
    countries = list(overview_data['countries'].keys())[:5]  # 前5个国家
    counts = list(overview_data['countries'].values())[:5]
    ax3.pie(counts, labels=countries, autopct='%1.1f%%', startangle=90)
    ax3.set_title('主要国家分布', fontsize=12, fontweight='bold')
    
    # 4. 地区分布
    ax4 = fig.add_subplot(gs[1, 2])
    regions = list(overview_data['regions'].keys())[:5]  # 前5个地区
    region_counts = list(overview_data['regions'].values())[:5]
    ax4.barh(regions, region_counts, color='lightgreen', alpha=0.7)
    ax4.set_title('主要地区分布', fontsize=12, fontweight='bold')
    ax4.set_xlabel('节点数量')
    
    # 5. 增长趋势
    ax5 = fig.add_subplot(gs[2, :])
    cumulative_nodes = [entry['cumulative_nodes'] for entry in timeline_data]
    cumulative_azs = [entry['cumulative_availability_zones'] for entry in timeline_data]
    
    ax5_twin = ax5.twinx()
    line1 = ax5.plot(years, cumulative_nodes, 'b-', linewidth=2, marker='o', label='节点数量')
    line2 = ax5_twin.plot(years, cumulative_azs, 'r-', linewidth=2, marker='s', label='可用区数量')
    
    ax5.set_xlabel('年份')
    ax5.set_ylabel('累计节点数量', color='blue')
    ax5_twin.set_ylabel('累计可用区数量', color='red')
    ax5.set_title('基础设施增长趋势', fontsize=12, fontweight='bold')
    
    # 图例
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax5.legend(lines, labels, loc='upper left')
    
    plt.suptitle('阿里云全球基础设施发展报告', fontsize=20, fontweight='bold')
    plt.savefig('docs/alibaba_cloud_summary.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """主函数"""
    print("正在加载数据...")
    overview, timeline = load_data()
    
    print("正在生成时间线图表...")
    create_timeline_chart(timeline)
    
    print("正在生成地理分布图表...")
    create_geographic_chart(overview)
    
    print("正在生成增长分析图表...")
    create_growth_analysis_chart(timeline)
    
    print("正在生成总结信息图...")
    create_summary_infographic(overview, timeline)
    
    print("所有图表已生成完成！")

if __name__ == "__main__":
    main() 