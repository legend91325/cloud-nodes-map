#!/usr/bin/env python3
"""
云节点数据可视化示例
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import CloudDataLoader
from src.visualization import CloudDataVisualizer


def main():
    """主函数"""
    print("=== 云节点数据可视化示例 ===\n")
    
    # 初始化数据加载器和可视化器
    loader = CloudDataLoader()
    visualizer = CloudDataVisualizer(loader)
    
    print("正在生成可视化图表和报告...\n")
    
    # 创建完整的可视化仪表板
    visualizer.create_dashboard("charts")
    
    print("\n=== 可视化完成 ===")
    print("生成的文件:")
    print("  - charts/provider_comparison.png (云厂商对比)")
    print("  - charts/global_coverage.png (全球覆盖分布)")
    print("  - charts/service_distribution.png (服务类型分布)")
    print("  - charts/regional_distribution.png (地区分布)")
    print("  - charts/network_performance.png (网络性能对比)")
    print("  - charts/launch_timeline.png (上线时间线)")
    print("  - charts/report.html (完整HTML报告)")
    
    print("\n您可以打开 charts/report.html 查看完整的可视化报告！")


if __name__ == "__main__":
    main() 