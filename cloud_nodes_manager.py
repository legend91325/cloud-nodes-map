#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一云服务商节点信息获取工具
支持阿里云和腾讯云
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Union
from abc import ABC, abstractmethod

# 导入各个云服务商的模块
try:
    from aliyun_api_nodes import AliyunAPINodes, AliyunConfig
except ImportError:
    AliyunAPINodes = None
    AliyunConfig = None

try:
    from tencentcloud_api_nodes import TencentCloudAPINodes, TencentCloudConfig
except ImportError:
    TencentCloudAPINodes = None
    TencentCloudConfig = None

try:
    from huaweicloud_api_nodes import HuaweiCloudAPINodes, HuaweiCloudConfig
except ImportError:
    HuaweiCloudAPINodes = None
    HuaweiCloudConfig = None

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CloudProvider(ABC):
    """云服务商抽象基类"""
    
    @abstractmethod
    def get_regions(self) -> List[Dict]:
        """获取区域信息"""
        pass
    
    @abstractmethod
    def get_zones(self, region_id: str) -> List[Dict]:
        """获取可用区信息"""
        pass
    
    @abstractmethod
    def get_all_data(self) -> Dict:
        """获取所有数据"""
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """获取服务商名称"""
        pass

class AliyunProvider(CloudProvider):
    """阿里云服务商实现"""
    
    def __init__(self, access_key_id: str = None, access_key_secret: str = None):
        if AliyunAPINodes is None:
            raise ImportError("阿里云SDK未安装，请运行: pip install aliyun-python-sdk-core aliyun-python-sdk-ecs")
        
        self.client = AliyunAPINodes(access_key_id, access_key_secret)
    
    def get_regions(self) -> List[Dict]:
        return self.client.get_regions_via_api()
    
    def get_zones(self, region_id: str) -> List[Dict]:
        return self.client.get_zones_via_api(region_id)
    
    def get_all_data(self) -> Dict:
        return self.client.get_all_regions_with_zones()
    
    def get_provider_name(self) -> str:
        return "阿里云"

class TencentCloudProvider(CloudProvider):
    """腾讯云服务商实现"""
    
    def __init__(self, secret_id: str = None, secret_key: str = None):
        if TencentCloudAPINodes is None:
            raise ImportError("腾讯云SDK未安装，请运行: pip install tencentcloud-sdk-python")
        
        self.client = TencentCloudAPINodes(secret_id, secret_key)
    
    def get_regions(self) -> List[Dict]:
        return self.client.get_regions_via_api()
    
    def get_zones(self, region_id: str) -> List[Dict]:
        return self.client.get_zones_via_api(region_id)
    
    def get_all_data(self) -> Dict:
        return self.client.get_all_regions_with_zones()
    
    def get_provider_name(self) -> str:
        return "腾讯云"

class HuaweiCloudProvider(CloudProvider):
    """华为云服务商实现"""
    
    def __init__(self, access_key_id: str = None, secret_access_key: str = None, project_id: str = None):
        if HuaweiCloudAPINodes is None:
            raise ImportError("华为云SDK未安装，请运行: pip install huaweicloudsdkcore huaweicloudsdkecs")
        
        self.client = HuaweiCloudAPINodes(access_key_id, secret_access_key, project_id)
    
    def get_regions(self) -> List[Dict]:
        return self.client.get_regions_via_api()
    
    def get_zones(self, region_id: str) -> List[Dict]:
        return self.client.get_zones_via_api(region_id)
    
    def get_all_data(self) -> Dict:
        return self.client.get_all_regions_with_zones()
    
    def get_provider_name(self) -> str:
        return "华为云"

class CloudNodesManager:
    """统一云服务商节点管理器"""
    
    def __init__(self):
        self.output_dir = "output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def get_available_providers(self) -> List[str]:
        """获取可用的云服务商列表"""
        providers = []
        
        if AliyunAPINodes is not None:
            providers.append("aliyun")
        
        if TencentCloudAPINodes is not None:
            providers.append("tencentcloud")
        
        if HuaweiCloudAPINodes is not None:
            providers.append("huaweicloud")
        
        return providers
    
    def create_provider(self, provider_name: str, **kwargs) -> CloudProvider:
        """创建云服务商实例"""
        if provider_name.lower() == "aliyun":
            return AliyunProvider(**kwargs)
        elif provider_name.lower() == "tencentcloud":
            return TencentCloudProvider(**kwargs)
        elif provider_name.lower() == "huaweicloud":
            return HuaweiCloudProvider(**kwargs)
        else:
            raise ValueError(f"不支持的云服务商: {provider_name}")
    
    def save_to_json(self, data: Dict, filename: str) -> str:
        """保存数据到JSON文件"""
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"数据已保存到: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"保存JSON文件失败: {e}")
            return ""
    
    def save_to_csv(self, data: List[Dict], filename: str) -> str:
        """保存数据到CSV文件"""
        try:
            import csv
            
            filepath = os.path.join(self.output_dir, filename)
            
            if data:
                fieldnames = data[0].keys()
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)
                
                logger.info(f"数据已保存到: {filepath}")
                return filepath
            else:
                logger.warning("没有数据可保存")
                return ""
                
        except ImportError:
            logger.error("CSV模块导入失败")
            return ""
        except Exception as e:
            logger.error(f"保存CSV文件失败: {e}")
            return ""
    
    def get_provider_credentials(self, provider_name: str) -> tuple:
        """获取云服务商凭据"""
        if provider_name.lower() == "aliyun":
            if AliyunConfig is None:
                return None, None
            
            config = AliyunConfig()
            if config.has_credentials():
                return config.load_credentials()
            else:
                return None, None
        
        elif provider_name.lower() == "tencentcloud":
            if TencentCloudConfig is None:
                return None, None
            
            config = TencentCloudConfig()
            if config.has_credentials():
                return config.load_credentials()
            else:
                return None, None
        
        elif provider_name.lower() == "huaweicloud":
            if HuaweiCloudConfig is None:
                return None, None, None
            
            config = HuaweiCloudConfig()
            if config.has_credentials():
                return config.load_credentials()
            else:
                return None, None, None
        
        return None, None
    
    def display_regions_by_continent(self, regions: List[Dict], zones_by_region: Dict, provider_name: str):
        """按大洲分组显示区域信息"""
        print(f"\n{provider_name}区域分布:")
        print("-" * 60)
        
        # 按大洲分组
        grouped = {}
        for region in regions:
            region_id = region['region_id']
            
            # 根据region_id判断大洲
            if provider_name == "阿里云":
                if region_id.startswith('cn'):
                    continent = '中国'
                elif region_id.startswith('ap'):
                    continent = '亚太'
                elif region_id.startswith('eu'):
                    continent = '欧洲'
                elif region_id.startswith('us'):
                    continent = '美洲'
                elif region_id.startswith('me'):
                    continent = '中东'
                else:
                    continent = '其他'
            elif provider_name == "腾讯云":
                if region_id.startswith('ap-'):
                    if any(city in region_id for city in ['guangzhou', 'shenzhen', 'shanghai', 'beijing']):
                        continent = '中国'
                    else:
                        continent = '亚太'
                elif region_id.startswith('na-'):
                    continent = '北美'
                elif region_id.startswith('eu-'):
                    continent = '欧洲'
                elif region_id.startswith('sa-'):
                    continent = '南美'
                else:
                    continent = '其他'
            else:  # 华为云
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
            
            if continent not in grouped:
                grouped[continent] = []
            grouped[continent].append(region)
        
        # 显示分组结果
        for continent, continent_regions in grouped.items():
            print(f"\n{continent} ({len(continent_regions)} 个区域):")
            for region in continent_regions:
                zone_count = len(zones_by_region.get(region['region_id'], []))
                region_name = region.get('region_name', region.get('region_id'))
                print(f"  - {region_name} ({region['region_id']}) - {zone_count} 个可用区")

def main():
    """主函数"""
    print("=" * 60)
    print("统一云服务商节点信息获取工具")
    print("=" * 60)
    
    manager = CloudNodesManager()
    available_providers = manager.get_available_providers()
    
    if not available_providers:
        print("错误: 未安装任何云服务商SDK")
        print("请安装以下依赖:")
        print("  - 阿里云: pip install aliyun-python-sdk-core aliyun-python-sdk-ecs")
        print("  - 腾讯云: pip install tencentcloud-sdk-python")
        return
    
    print(f"可用的云服务商: {', '.join(available_providers)}")
    
    # 选择云服务商
    if len(available_providers) == 1:
        provider_name = available_providers[0]
        print(f"自动选择: {provider_name}")
    else:
        print("\n请选择云服务商:")
        for i, provider in enumerate(available_providers, 1):
            print(f"{i}. {provider}")
        
        choice = input(f"\n请输入选择 (1-{len(available_providers)}): ").strip()
        try:
            provider_name = available_providers[int(choice) - 1]
        except (ValueError, IndexError):
            print("无效选择")
            return
    
    # 获取凭据
    credentials = manager.get_provider_credentials(provider_name)
    
    if provider_name == "aliyun":
        cred1, cred2 = credentials
        if cred1 and cred2:
            print("发现已保存的阿里云凭据")
            use_saved = input("是否使用已保存的凭据? (y/n): ").strip().lower()
            if use_saved != 'y':
                cred1 = input("请输入阿里云AccessKey ID: ").strip()
                cred2 = input("请输入阿里云AccessKey Secret: ").strip()
        else:
            cred1 = input("请输入阿里云AccessKey ID: ").strip()
            cred2 = input("请输入阿里云AccessKey Secret: ").strip()
    elif provider_name == "tencentcloud":
        cred1, cred2 = credentials
        if cred1 and cred2:
            print("发现已保存的腾讯云凭据")
            use_saved = input("是否使用已保存的凭据? (y/n): ").strip().lower()
            if use_saved != 'y':
                cred1 = input("请输入腾讯云SecretId: ").strip()
                cred2 = input("请输入腾讯云SecretKey: ").strip()
        else:
            cred1 = input("请输入腾讯云SecretId: ").strip()
            cred2 = input("请输入腾讯云SecretKey: ").strip()
    else:  # huaweicloud
        cred1, cred2, cred3 = credentials
        if cred1 and cred2:
            print("发现已保存的华为云凭据")
            use_saved = input("是否使用已保存的凭据? (y/n): ").strip().lower()
            if use_saved != 'y':
                cred1 = input("请输入华为云AccessKey ID: ").strip()
                cred2 = input("请输入华为云SecretAccessKey: ").strip()
                cred3 = input("请输入华为云Project ID (可选): ").strip()
        else:
            cred1 = input("请输入华为云AccessKey ID: ").strip()
            cred2 = input("请输入华为云SecretAccessKey: ").strip()
            cred3 = input("请输入华为云Project ID (可选): ").strip()
    
    if not cred1 or not cred2:
        print("错误: 必须提供凭据")
        return
    
    try:
        # 创建云服务商实例
        if provider_name == "aliyun":
            provider = manager.create_provider(provider_name, access_key_id=cred1, access_key_secret=cred2)
        elif provider_name == "tencentcloud":
            provider = manager.create_provider(provider_name, secret_id=cred1, secret_key=cred2)
        else:  # huaweicloud
            provider = manager.create_provider(provider_name, access_key_id=cred1, secret_access_key=cred2, project_id=cred3)
        
        print(f"\n正在获取{provider.get_provider_name()}全球节点信息...")
        
        # 获取所有数据
        all_data = provider.get_all_data()
        
        if all_data:
            regions = all_data['regions']
            zones_by_region = all_data['zones_by_region']
            
            print(f"\n成功获取 {len(regions)} 个区域:")
            
            # 显示区域分布
            manager.display_regions_by_continent(regions, zones_by_region, provider.get_provider_name())
            
            print(f"\n总计: {all_data['total_regions']} 个区域, {all_data['total_zones']} 个可用区")
            
            # 保存数据
            print("\n" + "=" * 60)
            print("保存选项:")
            print("1. 保存为JSON文件")
            print("2. 保存为CSV文件")
            print("3. 两者都保存")
            print("4. 不保存")
            
            choice = input("\n请选择保存选项 (1-4): ").strip()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"{provider_name}_nodes_{timestamp}"
            
            if choice == "1":
                manager.save_to_json(all_data, f"{base_filename}.json")
            elif choice == "2":
                # 扁平化数据用于CSV
                flat_data = []
                for region in regions:
                    region_data = {
                        'provider': provider.get_provider_name(),
                        'region_id': region['region_id'],
                        'region_name': region.get('region_name', ''),
                        'region_state': region.get('region_state', region.get('status', '')),
                        'zone_id': '',
                        'zone_name': '',
                        'zone_state': '',
                        'fetch_time': region['fetch_time']
                    }
                    flat_data.append(region_data)
                    
                    zones = zones_by_region.get(region['region_id'], [])
                    for zone in zones:
                        zone_data = {
                            'provider': provider.get_provider_name(),
                            'region_id': region['region_id'],
                            'region_name': region.get('region_name', ''),
                            'region_state': region.get('region_state', region.get('status', '')),
                            'zone_id': zone['zone_id'],
                            'zone_name': zone.get('zone_name', ''),
                            'zone_state': zone.get('zone_state', zone.get('status', '')),
                            'fetch_time': zone['fetch_time']
                        }
                        flat_data.append(zone_data)
                
                manager.save_to_csv(flat_data, f"{base_filename}.csv")
            elif choice == "3":
                manager.save_to_json(all_data, f"{base_filename}.json")
                
                # 扁平化数据用于CSV
                flat_data = []
                for region in regions:
                    region_data = {
                        'provider': provider.get_provider_name(),
                        'region_id': region['region_id'],
                        'region_name': region.get('region_name', ''),
                        'region_state': region.get('region_state', region.get('status', '')),
                        'zone_id': '',
                        'zone_name': '',
                        'zone_state': '',
                        'fetch_time': region['fetch_time']
                    }
                    flat_data.append(region_data)
                    
                    zones = zones_by_region.get(region['region_id'], [])
                    for zone in zones:
                        zone_data = {
                            'provider': provider.get_provider_name(),
                            'region_id': region['region_id'],
                            'region_name': region.get('region_name', ''),
                            'region_state': region.get('region_state', region.get('status', '')),
                            'zone_id': zone['zone_id'],
                            'zone_name': zone.get('zone_name', ''),
                            'zone_state': zone.get('zone_state', zone.get('status', '')),
                            'fetch_time': zone['fetch_time']
                        }
                        flat_data.append(zone_data)
                
                manager.save_to_csv(flat_data, f"{base_filename}.csv")
            else:
                print("未选择保存")
            
            print("\n获取完成！")
        else:
            print(f"获取{provider.get_provider_name()}节点信息失败")
    
    except Exception as e:
        logger.error(f"操作失败: {e}")
        print(f"错误: {e}")

if __name__ == "__main__":
    main() 