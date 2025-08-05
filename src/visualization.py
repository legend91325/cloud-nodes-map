"""
云节点数据可视化工具
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from typing import Dict, List, Optional
import json
import os
from datetime import datetime

from .data_loader import CloudDataLoader
from .models import CloudProvider, ServiceType, NodeStatus


class CloudDataVisualizer:
    """云节点数据可视化器"""
    
    def __init__(self, data_loader: CloudDataLoader):
        """
        初始化可视化器
        
        Args:
            data_loader: 数据加载器实例
        """
        self.loader = data_loader
        self.provider_colors = {
            CloudProvider.ALIBABA_CLOUD: '#FF6A00',
            CloudProvider.HUAWEI_CLOUD: '#FF0000',
            CloudProvider.TENCENT_CLOUD: '#00A4FF',
            CloudProvider.AWS: '#FF9900',
            CloudProvider.AZURE: '#0078D4',
            CloudProvider.GOOGLE_CLOUD: '#4285F4'
        }
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    
    def plot_provider_comparison(self, save_path: Optional[str] = None):
        """
        绘制云厂商对比图
        
        Args:
            save_path: 保存路径，如果为None则显示图片
        """
        stats = self.loader.get_provider_statistics()
        
        providers = list(stats.keys())
        node_counts = [stats[p]['total_nodes'] for p in providers]
        country_counts = [len(stats[p]['countries']) for p in providers]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 节点数量对比
        bars1 = ax1.bar(providers, node_counts, color=list(self.provider_colors.values())[:len(providers)])
        ax1.set_title('各云厂商节点数量对比', fontsize=14, fontweight='bold')
        ax1.set_ylabel('节点数量')
        ax1.tick_params(axis='x', rotation=45)
        
        # 添加数值标签
        for bar, count in zip(bars1, node_counts):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(count), ha='center', va='bottom')
        
        # 覆盖国家数量对比
        bars2 = ax2.bar(providers, country_counts, color=list(self.provider_colors.values())[:len(providers)])
        ax2.set_title('各云厂商覆盖国家数量对比', fontsize=14, fontweight='bold')
        ax2.set_ylabel('国家数量')
        ax2.tick_params(axis='x', rotation=45)
        
        # 添加数值标签
        for bar, count in zip(bars2, country_counts):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                    str(count), ha='center', va='bottom')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"图表已保存到: {save_path}")
        else:
            plt.show()
    
    def plot_global_coverage(self, top_n: int = 15, save_path: Optional[str] = None):
        """
        绘制全球覆盖分布图
        
        Args:
            top_n: 显示前N个国家
            save_path: 保存路径，如果为None则显示图片
        """
        coverage = self.loader.get_global_coverage()
        
        # 获取前N个国家
        top_countries = list(coverage.items())[:top_n]
        countries = [item[0] for item in top_countries]
        counts = [item[1] for item in top_countries]
        
        plt.figure(figsize=(12, 8))
        bars = plt.barh(countries, counts, color='skyblue', edgecolor='navy', alpha=0.7)
        
        plt.title(f'全球云节点覆盖分布 (前{top_n}个国家)', fontsize=16, fontweight='bold')
        plt.xlabel('节点数量')
        plt.ylabel('国家/地区')
        
        # 添加数值标签
        for bar, count in zip(bars, counts):
            plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                    str(count), ha='left', va='center', fontweight='bold')
        
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"图表已保存到: {save_path}")
        else:
            plt.show()
    
    def plot_service_type_distribution(self, save_path: Optional[str] = None):
        """
        绘制服务类型分布图
        
        Args:
            save_path: 保存路径，如果为None则显示图片
        """
        stats = self.loader.get_provider_statistics()
        
        # 统计各服务类型的总节点数
        service_counts = {}
        for provider_stats in stats.values():
            for service_type, count in provider_stats['service_types'].items():
                service_counts[service_type] = service_counts.get(service_type, 0) + count
        
        # 服务类型中文映射
        service_names = {
            'compute': '计算',
            'storage': '存储',
            'network': '网络',
            'database': '数据库',
            'cdn': 'CDN',
            'ai': 'AI',
            'security': '安全'
        }
        
        services = [service_names.get(s, s) for s in service_counts.keys()]
        counts = list(service_counts.values())
        
        plt.figure(figsize=(10, 8))
        colors = plt.cm.Set3(np.linspace(0, 1, len(services)))
        
        wedges, texts, autotexts = plt.pie(counts, labels=services, autopct='%1.1f%%',
                                          colors=colors, startangle=90)
        
        plt.title('云服务类型分布', fontsize=16, fontweight='bold')
        
        # 设置文本样式
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.axis('equal')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"图表已保存到: {save_path}")
        else:
            plt.show()
    
    def plot_regional_distribution(self, save_path: Optional[str] = None):
        """
        绘制地区分布图
        
        Args:
            save_path: 保存路径，如果为None则显示图片
        """
        all_data = self.loader.load_all_providers()
        
        # 统计各地区节点数量
        region_counts = {}
        for provider_data in all_data.values():
            for node in provider_data.nodes:
                region = node.location.region
                region_counts[region] = region_counts.get(region, 0) + 1
        
        # 按节点数量排序
        sorted_regions = sorted(region_counts.items(), key=lambda x: x[1], reverse=True)
        regions = [item[0] for item in sorted_regions]
        counts = [item[1] for item in sorted_regions]
        
        plt.figure(figsize=(12, 8))
        bars = plt.bar(regions, counts, color='lightcoral', edgecolor='darkred', alpha=0.7)
        
        plt.title('云节点地区分布', fontsize=16, fontweight='bold')
        plt.xlabel('地区')
        plt.ylabel('节点数量')
        plt.xticks(rotation=45, ha='right')
        
        # 添加数值标签
        for bar, count in zip(bars, counts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(count), ha='center', va='bottom', fontweight='bold')
        
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"图表已保存到: {save_path}")
        else:
            plt.show()
    
    def plot_network_performance(self, save_path: Optional[str] = None):
        """
        绘制网络性能对比图
        
        Args:
            save_path: 保存路径，如果为None则显示图片
        """
        all_data = self.loader.load_all_providers()
        
        # 收集网络延迟数据
        provider_latencies = {}
        for provider, provider_data in all_data.items():
            latencies = []
            for node in provider_data.nodes:
                if node.network_info and node.network_info.latency:
                    latencies.append(node.network_info.latency)
            
            if latencies:
                provider_latencies[provider.value] = {
                    'mean': np.mean(latencies),
                    'median': np.median(latencies),
                    'min': np.min(latencies),
                    'max': np.max(latencies)
                }
        
        if not provider_latencies:
            print("没有可用的网络延迟数据")
            return
        
        providers = list(provider_latencies.keys())
        means = [provider_latencies[p]['mean'] for p in providers]
        medians = [provider_latencies[p]['median'] for p in providers]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 平均延迟对比
        bars1 = ax1.bar(providers, means, color=list(self.provider_colors.values())[:len(providers)])
        ax1.set_title('各云厂商平均网络延迟对比', fontsize=14, fontweight='bold')
        ax1.set_ylabel('延迟 (毫秒)')
        ax1.tick_params(axis='x', rotation=45)
        
        # 添加数值标签
        for bar, mean in zip(bars1, means):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{mean:.1f}', ha='center', va='bottom')
        
        # 中位数延迟对比
        bars2 = ax2.bar(providers, medians, color=list(self.provider_colors.values())[:len(providers)])
        ax2.set_title('各云厂商中位数网络延迟对比', fontsize=14, fontweight='bold')
        ax2.set_ylabel('延迟 (毫秒)')
        ax2.tick_params(axis='x', rotation=45)
        
        # 添加数值标签
        for bar, median in zip(bars2, medians):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{median:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"图表已保存到: {save_path}")
        else:
            plt.show()
    
    def plot_launch_timeline(self, save_path: Optional[str] = None):
        """
        绘制节点上线时间线图
        
        Args:
            save_path: 保存路径，如果为None则显示图片
        """
        all_data = self.loader.load_all_providers()
        
        # 收集上线时间数据
        launch_data = {}
        for provider, provider_data in all_data.items():
            for node in provider_data.nodes:
                if node.launch_date:
                    year = node.launch_date.year
                    if year not in launch_data:
                        launch_data[year] = {}
                    
                    provider_name = provider.value
                    if provider_name not in launch_data[year]:
                        launch_data[year][provider_name] = 0
                    
                    launch_data[year][provider_name] += 1
        
        if not launch_data:
            print("没有可用的上线时间数据")
            return
        
        # 准备绘图数据
        years = sorted(launch_data.keys())
        providers = list(self.provider_colors.keys())
        provider_names = [p.value for p in providers]
        
        # 创建堆叠柱状图数据
        data = []
        for provider_name in provider_names:
            provider_data = []
            for year in years:
                count = launch_data[year].get(provider_name, 0)
                provider_data.append(count)
            data.append(provider_data)
        
        # 绘制堆叠柱状图
        plt.figure(figsize=(14, 8))
        
        bottom = np.zeros(len(years))
        for i, (provider_name, provider_data) in enumerate(zip(provider_names, data)):
            color = list(self.provider_colors.values())[i] if i < len(self.provider_colors) else 'gray'
            plt.bar(years, provider_data, bottom=bottom, label=provider_name, color=color, alpha=0.8)
            bottom += np.array(provider_data)
        
        plt.title('云节点上线时间线', fontsize=16, fontweight='bold')
        plt.xlabel('年份')
        plt.ylabel('新增节点数量')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"图表已保存到: {save_path}")
        else:
            plt.show()
    
    def create_dashboard(self, save_dir: str = "charts"):
        """
        创建完整的可视化仪表板
        
        Args:
            save_dir: 保存目录
        """
        import os
        os.makedirs(save_dir, exist_ok=True)
        
        print("正在生成可视化图表...")
        
        # 生成各种图表
        self.plot_provider_comparison(os.path.join(save_dir, "provider_comparison.png"))
        self.plot_global_coverage(save_path=os.path.join(save_dir, "global_coverage.png"))
        self.plot_service_type_distribution(save_path=os.path.join(save_dir, "service_distribution.png"))
        self.plot_regional_distribution(save_path=os.path.join(save_dir, "regional_distribution.png"))
        self.plot_network_performance(save_path=os.path.join(save_dir, "network_performance.png"))
        self.plot_launch_timeline(save_path=os.path.join(save_dir, "launch_timeline.png"))
        
        print(f"所有图表已保存到 {save_dir} 目录")
        
        # 生成HTML报告
        self.generate_html_report(save_dir)
    
    def generate_html_report(self, save_dir: str):
        """
        生成HTML报告
        
        Args:
            save_dir: 保存目录
        """
        stats = self.loader.get_provider_statistics()
        coverage = self.loader.get_global_coverage()
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>云厂商全球节点数据报告</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #333; text-align: center; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
                h2 {{ color: #007bff; margin-top: 30px; }}
                .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }}
                .stat-card {{ background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #007bff; }}
                .chart-container {{ text-align: center; margin: 20px 0; }}
                .chart-container img {{ max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #007bff; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .footer {{ text-align: center; margin-top: 40px; color: #666; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🌍 云厂商全球节点数据报告</h1>
                
                <h2>📊 总体统计</h2>
                <div class="stats-grid">
        """
        
        # 添加总体统计
        total_nodes = sum(stat['total_nodes'] for stat in stats.values())
        total_countries = len(coverage)
        total_providers = len(stats)
        
        html_content += f"""
                    <div class="stat-card">
                        <h3>总节点数</h3>
                        <p style="font-size: 24px; font-weight: bold; color: #007bff;">{total_nodes}</p>
                    </div>
                    <div class="stat-card">
                        <h3>覆盖国家/地区</h3>
                        <p style="font-size: 24px; font-weight: bold; color: #28a745;">{total_countries}</p>
                    </div>
                    <div class="stat-card">
                        <h3>云厂商数量</h3>
                        <p style="font-size: 24px; font-weight: bold; color: #ffc107;">{total_providers}</p>
                    </div>
                </div>
        """
        
        # 添加各云厂商统计表格
        html_content += """
                <h2>🏢 各云厂商详细统计</h2>
                <table>
                    <thead>
                        <tr>
                            <th>云厂商</th>
                            <th>节点数量</th>
                            <th>覆盖国家</th>
                            <th>服务类型</th>
                            <th>最后更新</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for provider, stat in stats.items():
            html_content += f"""
                        <tr>
                            <td><strong>{provider}</strong></td>
                            <td>{stat['total_nodes']}</td>
                            <td>{len(stat['countries'])}</td>
                            <td>{', '.join(stat['service_types'].keys())}</td>
                            <td>{stat['last_updated'][:10]}</td>
                        </tr>
            """
        
        html_content += """
                    </tbody>
                </table>
        """
        
        # 添加图表
        html_content += """
                <h2>📈 可视化图表</h2>
        """
        
        chart_files = [
            ("provider_comparison.png", "云厂商对比"),
            ("global_coverage.png", "全球覆盖分布"),
            ("service_distribution.png", "服务类型分布"),
            ("regional_distribution.png", "地区分布"),
            ("network_performance.png", "网络性能对比"),
            ("launch_timeline.png", "上线时间线")
        ]
        
        for chart_file, title in chart_files:
            chart_path = os.path.join(save_dir, chart_file)
            if os.path.exists(chart_path):
                html_content += f"""
                <div class="chart-container">
                    <h3>{title}</h3>
                    <img src="{chart_file}" alt="{title}">
                </div>
                """
        
        # 添加全球覆盖统计
        html_content += """
                <h2>🌐 全球覆盖统计 (前20个国家/地区)</h2>
                <table>
                    <thead>
                        <tr>
                            <th>排名</th>
                            <th>国家/地区</th>
                            <th>节点数量</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for i, (country, count) in enumerate(list(coverage.items())[:20], 1):
            html_content += f"""
                        <tr>
                            <td>{i}</td>
                            <td>{country}</td>
                            <td>{count}</td>
                        </tr>
            """
        
        html_content += """
                    </tbody>
                </table>
                
                <div class="footer">
                    <p>报告生成时间: """ + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + """</p>
                    <p>数据来源: 各云厂商官方文档</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # 保存HTML文件
        html_path = os.path.join(save_dir, "report.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML报告已生成: {html_path}")


if __name__ == "__main__":
    # 示例使用
    loader = CloudDataLoader()
    visualizer = CloudDataVisualizer(loader)
    visualizer.create_dashboard() 