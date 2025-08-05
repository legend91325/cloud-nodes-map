#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华为云节点获取工具使用示例
"""

import os
import sys
from huaweicloud_api_nodes import HuaweiCloudAPINodes, HuaweiCloudConfig

def example_basic_usage():
    """基本使用示例"""
    print("=== 华为云节点获取工具使用示例 ===")
    
    # 方法1: 使用环境变量
    access_key_id = os.environ.get("HUAWEICLOUD_ACCESS_KEY_ID")
    secret_access_key = os.environ.get("HUAWEICLOUD_SECRET_ACCESS_KEY")
    project_id = os.environ.get("HUAWEICLOUD_PROJECT_ID")
    
    if access_key_id and secret_access_key:
        print("使用环境变量中的凭据")
        api = HuaweiCloudAPINodes(access_key_id, secret_access_key, project_id)
    else:
        # 方法2: 使用配置文件
        config = HuaweiCloudConfig()
        if config.has_credentials():
            print("使用配置文件中的凭据")
            access_key_id, secret_access_key, project_id = config.load_credentials()
            api = HuaweiCloudAPINodes(access_key_id, secret_access_key, project_id)
        else:
            print("未找到凭据，请先配置华为云凭据")
            print("方法1: 设置环境变量 HUAWEICLOUD_ACCESS_KEY_ID 和 HUAWEICLOUD_SECRET_ACCESS_KEY")
            print("方法2: 在 ~/.huaweicloud/credentials 文件中配置")
            return
    
    # 获取区域信息
    print("\n正在获取区域信息...")
    regions = api.get_regions_via_api()
    
    if regions:
        print(f"成功获取 {len(regions)} 个区域")
        print("\n前5个区域:")
        for i, region in enumerate(regions[:5]):
            print(f"  {i+1}. {region['region_name']} ({region['region_id']}) - {region['region_state']}")
    
    # 获取某个区域的可用区信息
    if regions:
        test_region = regions[0]['region_id']
        print(f"\n正在获取 {test_region} 的可用区信息...")
        zones = api.get_zones_via_api(test_region)
        
        if zones:
            print(f"成功获取 {len(zones)} 个可用区")
            for zone in zones:
                print(f"  - {zone['zone_name']} ({zone['zone_id']}) - {zone['zone_state']}")

def example_save_data():
    """数据保存示例"""
    print("\n=== 数据保存示例 ===")
    
    # 创建API实例（需要有效凭据）
    access_key_id = os.environ.get("HUAWEICLOUD_ACCESS_KEY_ID")
    secret_access_key = os.environ.get("HUAWEICLOUD_SECRET_ACCESS_KEY")
    project_id = os.environ.get("HUAWEICLOUD_PROJECT_ID")
    
    if not access_key_id or not secret_access_key:
        print("请设置环境变量 HUAWEICLOUD_ACCESS_KEY_ID 和 HUAWEICLOUD_SECRET_ACCESS_KEY")
        return
    
    api = HuaweiCloudAPINodes(access_key_id, secret_access_key, project_id)
    
    # 获取所有数据
    print("正在获取所有区域和可用区信息...")
    all_data = api.get_all_regions_with_zones()
    
    if all_data:
        # 保存为JSON
        json_file = api.save_to_json(all_data, "example_huaweicloud_nodes.json")
        if json_file:
            print(f"JSON文件已保存: {json_file}")
        
        # 保存为CSV
        regions = all_data['regions']
        zones_by_region = all_data['zones_by_region']
        
        # 扁平化数据
        flat_data = []
        for region in regions:
            region_data = {
                'region_id': region['region_id'],
                'region_name': region['region_name'],
                'region_state': region['region_state'],
                'zone_id': '',
                'zone_name': '',
                'zone_state': '',
                'fetch_time': region['fetch_time']
            }
            flat_data.append(region_data)
            
            zones = zones_by_region.get(region['region_id'], [])
            for zone in zones:
                zone_data = {
                    'region_id': region['region_id'],
                    'region_name': region['region_name'],
                    'region_state': region['region_state'],
                    'zone_id': zone['zone_id'],
                    'zone_name': zone['zone_name'],
                    'zone_state': zone['zone_state'],
                    'fetch_time': zone['fetch_time']
                }
                flat_data.append(zone_data)
        
        csv_file = api.save_to_csv(flat_data, "example_huaweicloud_nodes.csv")
        if csv_file:
            print(f"CSV文件已保存: {csv_file}")

def example_config_management():
    """配置管理示例"""
    print("\n=== 配置管理示例 ===")
    
    config = HuaweiCloudConfig()
    
    # 检查是否有保存的凭据
    if config.has_credentials():
        print("发现已保存的凭据")
        access_key_id, secret_access_key, project_id = config.load_credentials()
        print(f"AccessKeyId: {access_key_id[:8]}...")
        print(f"SecretAccessKey: {secret_access_key[:8]}...")
        if project_id:
            print(f"ProjectId: {project_id[:8]}...")
    else:
        print("未发现保存的凭据")
        
        # 示例：保存凭据（实际使用时需要真实的凭据）
        # access_key_id = "your_access_key_id"
        # secret_access_key = "your_secret_access_key"
        # project_id = "your_project_id"
        # if config.save_credentials(access_key_id, secret_access_key, project_id):
        #     print("凭据已保存")
        # else:
        #     print("凭据保存失败")

def example_region_analysis():
    """区域分析示例"""
    print("\n=== 区域分析示例 ===")
    
    # 创建API实例（需要有效凭据）
    access_key_id = os.environ.get("HUAWEICLOUD_ACCESS_KEY_ID")
    secret_access_key = os.environ.get("HUAWEICLOUD_SECRET_ACCESS_KEY")
    project_id = os.environ.get("HUAWEICLOUD_PROJECT_ID")
    
    if not access_key_id or not secret_access_key:
        print("请设置环境变量 HUAWEICLOUD_ACCESS_KEY_ID 和 HUAWEICLOUD_SECRET_ACCESS_KEY")
        return
    
    api = HuaweiCloudAPINodes(access_key_id, secret_access_key, project_id)
    
    # 获取区域信息
    regions = api.get_regions_via_api()
    
    if regions:
        # 按大洲分组分析
        continent_stats = {}
        for region in regions:
            region_id = region['region_id']
            
            # 根据region_id判断大洲
            if region_id.startswith('cn'):
                continent = '中国'
            elif region_id.startswith('ap'):
                continent = '亚太'
            elif region_id.startswith('eu'):
                continent = '欧洲'
            elif region_id.startswith('na'):
                continent = '北美'
            elif region_id.startswith('sa'):
                continent = '南美'
            elif region_id.startswith('af'):
                continent = '非洲'
            else:
                continent = '其他'
            
            if continent not in continent_stats:
                continent_stats[continent] = []
            continent_stats[continent].append(region)
        
        # 显示统计结果
        print("华为云区域分布统计:")
        print("-" * 40)
        for continent, continent_regions in continent_stats.items():
            print(f"{continent}: {len(continent_regions)} 个区域")
            for region in continent_regions[:3]:  # 只显示前3个
                print(f"  - {region['region_name']} ({region['region_id']})")
            if len(continent_regions) > 3:
                print(f"  ... 还有 {len(continent_regions) - 3} 个区域")

def main():
    """主函数"""
    print("华为云节点获取工具使用示例")
    print("=" * 50)
    
    try:
        # 基本使用示例
        example_basic_usage()
        
        # 配置管理示例
        example_config_management()
        
        # 区域分析示例
        example_region_analysis()
        
        # 数据保存示例（需要有效凭据）
        print("\n注意: 数据保存示例需要有效的华为云凭据")
        # example_save_data()
        
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请安装华为云SDK: pip install huaweicloudsdkcore huaweicloudsdkecs")
    except Exception as e:
        print(f"运行错误: {e}")

if __name__ == "__main__":
    main() 