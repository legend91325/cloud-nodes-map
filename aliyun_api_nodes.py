#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用阿里云API获取全球节点信息并保存到文件
需要安装: pip install aliyun-python-sdk-core aliyun-python-sdk-ecs
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

# 导入配置管理模块
from aliyun_config import AliyunConfig, get_credentials, save_credentials

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AliyunAPINodes:
    """使用阿里云API获取节点信息"""
    
    def __init__(self, access_key_id: str = None, access_key_secret: str = None):
        self.config = AliyunConfig()
        
        # 如果没有提供凭据，尝试从配置文件加载
        if not access_key_id or not access_key_secret:
            access_key_id, access_key_secret = self.config.load_credentials()
        
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.output_dir = "output"
        
        # 创建输出目录
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
    def get_regions_via_api(self) -> List[Dict]:
        """
        通过阿里云API获取区域信息
        需要配置AccessKey和SecretKey
        """
        try:
            # 检查SDK是否安装
            try:
                import aliyunsdkcore
                import aliyunsdkecs
            except ImportError:
                logger.error("请安装阿里云SDK: pip install aliyun-python-sdk-core aliyun-python-sdk-ecs")
                return []
            
            from aliyunsdkcore.client import AcsClient
            from aliyunsdkecs.request.v20140526.DescribeRegionsRequest import DescribeRegionsRequest
            
            if not self.access_key_id or not self.access_key_secret:
                logger.error("需要配置阿里云AccessKey和SecretKey")
                return []
            
            # 创建ACS客户端
            client = AcsClient(self.access_key_id, self.access_key_secret, 'cn-hangzhou')
            
            # 创建请求
            request = DescribeRegionsRequest()
            request.set_accept_format('json')
            
            # 发送请求
            response = client.do_action_with_exception(request)
            response_json = json.loads(response)
            
            regions = []
            for region in response_json.get('Regions', {}).get('Region', []):
                regions.append({
                    'region_id': region.get('RegionId'),
                    'region_name': region.get('LocalName'),
                    'status': 'active',
                    'fetch_time': datetime.now().isoformat()
                })
            
            logger.info(f"通过API获取到 {len(regions)} 个区域")
            return regions
            
        except Exception as e:
            logger.error(f"通过API获取区域信息失败: {e}")
            return []
    
    def get_zones_via_api(self, region_id: str) -> List[Dict]:
        """
        获取指定区域的可用区信息
        """
        try:
            from aliyunsdkcore.client import AcsClient
            from aliyunsdkecs.request.v20140526.DescribeZonesRequest import DescribeZonesRequest
            
            if not self.access_key_id or not self.access_key_secret:
                logger.error("需要配置阿里云AccessKey和SecretKey")
                return []
            
            client = AcsClient(self.access_key_id, self.access_key_secret, region_id)
            request = DescribeZonesRequest()
            request.set_accept_format('json')
            
            response = client.do_action_with_exception(request)
            response_json = json.loads(response)
            
            zones = []
            for zone in response_json.get('Zones', {}).get('Zone', []):
                zones.append({
                    'zone_id': zone.get('ZoneId'),
                    'zone_name': zone.get('LocalName'),
                    'region_id': region_id,
                    'status': zone.get('Status'),
                    'fetch_time': datetime.now().isoformat()
                })
            
            return zones
            
        except Exception as e:
            logger.error(f"获取可用区信息失败: {e}")
            return []
    
    def save_to_json(self, data: List[Dict], filename: str = None) -> str:
        """
        保存数据到JSON文件
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"aliyun_nodes_{timestamp}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"数据已保存到: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"保存JSON文件失败: {e}")
            return ""
    
    def save_to_csv(self, data: List[Dict], filename: str = None) -> str:
        """
        保存数据到CSV文件
        """
        try:
            import csv
            
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"aliyun_nodes_{timestamp}.csv"
            
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
    
    def get_all_regions_with_zones(self) -> Dict:
        """
        获取所有区域及其可用区信息
        """
        regions = self.get_regions_via_api()
        if not regions:
            return {}
        
        all_data = {
            'regions': regions,
            'zones_by_region': {},
            'fetch_time': datetime.now().isoformat(),
            'total_regions': len(regions)
        }
        
        total_zones = 0
        for region in regions:
            region_id = region['region_id']
            zones = self.get_zones_via_api(region_id)
            all_data['zones_by_region'][region_id] = zones
            total_zones += len(zones)
            logger.info(f"获取 {region_id} 的可用区: {len(zones)} 个")
        
        all_data['total_zones'] = total_zones
        return all_data

def main():
    """主函数"""
    print("=" * 60)
    print("阿里云API节点信息获取工具")
    print("=" * 60)
    
    config = AliyunConfig()
    
    # 检查是否有保存的凭据
    if config.has_credentials():
        print("发现已保存的阿里云凭据")
        use_saved = input("是否使用已保存的凭据? (y/n): ").strip().lower()
        
        if use_saved == 'y':
            access_key_id, access_key_secret = config.load_credentials()
            print("使用已保存的凭据")
        else:
            # 输入新的凭据
            access_key_id = input("请输入阿里云AccessKey ID: ").strip()
            access_key_secret = input("请输入阿里云AccessKey Secret: ").strip()
            
            # 询问是否保存新凭据
            if access_key_id and access_key_secret:
                save_new = input("是否保存这些凭据供下次使用? (y/n): ").strip().lower()
                if save_new == 'y':
                    if config.save_credentials(access_key_id, access_key_secret):
                        print("凭据已保存")
                    else:
                        print("凭据保存失败")
    else:
        # 没有保存的凭据，需要输入
        print("未发现保存的凭据")
        access_key_id = input("请输入阿里云AccessKey ID: ").strip()
        access_key_secret = input("请输入阿里云AccessKey Secret: ").strip()
        
        # 询问是否保存凭据
        if access_key_id and access_key_secret:
            save_new = input("是否保存这些凭据供下次使用? (y/n): ").strip().lower()
            if save_new == 'y':
                if config.save_credentials(access_key_id, access_key_secret):
                    print("凭据已保存")
                else:
                    print("凭据保存失败")
    
    if not access_key_id or not access_key_secret:
        print("错误: 必须提供AccessKey ID和Secret")
        return
    
    aliyun_api = AliyunAPINodes(access_key_id, access_key_secret)
    
    print("\n正在获取阿里云全球节点信息...")
    
    # 获取所有区域和可用区信息
    all_data = aliyun_api.get_all_regions_with_zones()
    
    if all_data:
        regions = all_data['regions']
        print(f"\n成功获取 {len(regions)} 个区域:")
        print("-" * 60)
        
        # 按大洲分组显示
        grouped = {}
        for region in regions:
            # 根据region_id判断大洲
            region_id = region['region_id']
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
            
            if continent not in grouped:
                grouped[continent] = []
            grouped[continent].append(region)
        
        for continent, continent_regions in grouped.items():
            print(f"\n{continent} ({len(continent_regions)} 个区域):")
            for region in continent_regions:
                zone_count = len(all_data['zones_by_region'].get(region['region_id'], []))
                print(f"  - {region['region_name']} ({region['region_id']}) - {zone_count} 个可用区")
        
        print(f"\n总计: {all_data['total_regions']} 个区域, {all_data['total_zones']} 个可用区")
        
        # 保存数据
        print("\n" + "=" * 60)
        print("保存选项:")
        print("1. 保存为JSON文件")
        print("2. 保存为CSV文件")
        print("3. 两者都保存")
        print("4. 不保存")
        
        choice = input("\n请选择保存选项 (1-4): ").strip()
        
        if choice == "1":
            aliyun_api.save_to_json(all_data, "aliyun_nodes_complete.json")
        elif choice == "2":
            # 将数据扁平化为CSV格式
            flat_data = []
            for region in regions:
                region_data = {
                    'region_id': region['region_id'],
                    'region_name': region['region_name'],
                    'zone_id': '',
                    'zone_name': '',
                    'zone_status': '',
                    'fetch_time': region['fetch_time']
                }
                flat_data.append(region_data)
                
                # 添加可用区信息
                zones = all_data['zones_by_region'].get(region['region_id'], [])
                for zone in zones:
                    zone_data = {
                        'region_id': region['region_id'],
                        'region_name': region['region_name'],
                        'zone_id': zone['zone_id'],
                        'zone_name': zone['zone_name'],
                        'zone_status': zone['status'],
                        'fetch_time': zone['fetch_time']
                    }
                    flat_data.append(zone_data)
            
            aliyun_api.save_to_csv(flat_data, "aliyun_nodes_complete.csv")
        elif choice == "3":
            aliyun_api.save_to_json(all_data, "aliyun_nodes_complete.json")
            
            # 扁平化数据用于CSV
            flat_data = []
            for region in regions:
                region_data = {
                    'region_id': region['region_id'],
                    'region_name': region['region_name'],
                    'zone_id': '',
                    'zone_name': '',
                    'zone_status': '',
                    'fetch_time': region['fetch_time']
                }
                flat_data.append(region_data)
                
                zones = all_data['zones_by_region'].get(region['region_id'], [])
                for zone in zones:
                    zone_data = {
                        'region_id': region['region_id'],
                        'region_name': region['region_name'],
                        'zone_id': zone['zone_id'],
                        'zone_name': zone['zone_name'],
                        'zone_status': zone['status'],
                        'fetch_time': zone['fetch_time']
                    }
                    flat_data.append(zone_data)
            
            aliyun_api.save_to_csv(flat_data, "aliyun_nodes_complete.csv")
        else:
            print("未选择保存")
        
        print("\n获取完成！")
    else:
        print("获取阿里云节点信息失败")

if __name__ == "__main__":
    main() 