#!/usr/bin/env python3
"""
云节点数据使用示例
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import CloudDataLoader
from src.models import CloudProvider, ServiceType, NodeStatus


def main():
    """主函数"""
    print("=== 云厂商全球节点数据使用示例 ===\n")
    
    # 初始化数据加载器
    loader = CloudDataLoader()
    
    # 1. 获取各云厂商统计信息
    print("1. 各云厂商统计信息:")
    stats = loader.get_provider_statistics()
    for provider, stat in stats.items():
        print(f"  {provider}:")
        print(f"    总节点数: {stat['total_nodes']}")
        print(f"    覆盖国家数: {len(stat['countries'])}")
        print(f"    服务类型: {list(stat['service_types'].keys())}")
        print(f"    最后更新: {stat['last_updated']}")
        print()
    
    # 2. 获取全球覆盖统计
    print("2. 全球覆盖统计 (前10个国家):")
    coverage = loader.get_global_coverage()
    for i, (country, count) in enumerate(list(coverage.items())[:10]):
        print(f"  {i+1}. {country}: {count} 个节点")
    print()
    
    # 3. 按国家查询节点
    print("3. 中国地区的云节点:")
    china_nodes = loader.get_nodes_by_country("中国")
    for node in china_nodes[:5]:  # 只显示前5个
        print(f"  - {node.provider.value}: {node.name} ({node.location.city})")
    print(f"  总计: {len(china_nodes)} 个节点")
    print()
    
    # 4. 按服务类型查询节点
    print("4. 支持AI服务的节点数量:")
    ai_nodes = loader.get_nodes_by_service_type(ServiceType.AI)
    print(f"  总计: {len(ai_nodes)} 个节点支持AI服务")
    print()
    
    # 5. 搜索特定节点
    print("5. 搜索包含'北京'的节点:")
    beijing_nodes = loader.search_nodes("北京")
    for node in beijing_nodes:
        print(f"  - {node.provider.value}: {node.name}")
    print()
    
    # 6. 获取特定云厂商的数据
    print("6. 阿里云节点信息:")
    alibaba_data = loader.load_provider_data(CloudProvider.ALIBABA_CLOUD)
    if alibaba_data:
        print(f"  总节点数: {len(alibaba_data.nodes)}")
        print(f"  覆盖国家: {list(set(node.location.country for node in alibaba_data.nodes))}")
        print(f"  最后更新: {alibaba_data.last_updated}")
    print()
    
    # 7. 验证数据完整性
    print("7. 数据验证:")
    errors = loader.validate_data()
    if errors:
        print("  发现以下错误:")
        for provider, provider_errors in errors.items():
            print(f"    {provider}:")
            for error in provider_errors:
                print(f"      - {error}")
    else:
        print("  数据验证通过，未发现错误")
    print()
    
    # 8. 导出数据到CSV
    print("8. 导出数据到CSV文件:")
    try:
        loader.export_to_csv("cloud_nodes_data.csv")
        print("  数据已成功导出到 cloud_nodes_data.csv")
    except Exception as e:
        print(f"  导出失败: {e}")
    print()
    
    # 9. 按地区查询节点
    print("9. 亚太地区的云节点统计:")
    asia_nodes = loader.get_nodes_by_region("东亚")
    print(f"  东亚地区: {len(asia_nodes)} 个节点")
    
    southeast_asia_nodes = loader.get_nodes_by_region("东南亚")
    print(f"  东南亚地区: {len(southeast_asia_nodes)} 个节点")
    
    south_asia_nodes = loader.get_nodes_by_region("南亚")
    print(f"  南亚地区: {len(south_asia_nodes)} 个节点")
    print()
    
    # 10. 按状态查询节点
    print("10. 节点状态统计:")
    active_nodes = loader.get_nodes_by_status(NodeStatus.ACTIVE)
    print(f"  活跃节点: {len(active_nodes)} 个")
    
    maintenance_nodes = loader.get_nodes_by_status(NodeStatus.MAINTENANCE)
    print(f"  维护中节点: {len(maintenance_nodes)} 个")
    
    planned_nodes = loader.get_nodes_by_status(NodeStatus.PLANNED)
    print(f"  计划中节点: {len(planned_nodes)} 个")
    print()
    
    print("=== 示例演示完成 ===")


if __name__ == "__main__":
    main() 