#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用腾讯云API获取全球节点信息并保存到文件
需要安装: pip install tencentcloud-sdk-python
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TencentCloudConfig:
    """腾讯云配置管理类"""
    
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.tencentcloud")
        self.credentials_file = os.path.join(self.config_dir, "credentials")
        
        # 创建配置目录
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
    def save_credentials(self, secret_id: str, secret_key: str) -> bool:
        """保存腾讯云凭据到配置文件"""
        try:
            with open(self.credentials_file, 'w', encoding='utf-8') as f:
                f.write("[default]\n")
                f.write(f"secret_id = {secret_id}\n")
                f.write(f"secret_key = {secret_key}\n")
            logger.info("腾讯云凭据已保存")
            return True
        except Exception as e:
            logger.error(f"保存腾讯云凭据失败: {e}")
            return False
    
    def load_credentials(self) -> tuple:
        """从配置文件加载腾讯云凭据"""
        try:
            if not os.path.exists(self.credentials_file):
                return None, None
            
            secret_id = None
            secret_key = None
            
            with open(self.credentials_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('secret_id'):
                        secret_id = line.split('=')[1].strip()
                    elif line.startswith('secret_key'):
                        secret_key = line.split('=')[1].strip()
            
            return secret_id, secret_key
        except Exception as e:
            logger.error(f"加载腾讯云凭据失败: {e}")
            return None, None
    
    def has_credentials(self) -> bool:
        """检查是否有保存的凭据"""
        secret_id, secret_key = self.load_credentials()
        return secret_id is not None and secret_key is not None

class TencentCloudAPINodes:
    """使用腾讯云API获取节点信息"""
    
    def __init__(self, secret_id: str = None, secret_key: str = None):
        self.config = TencentCloudConfig()
        
        # 如果没有提供凭据，尝试从配置文件加载
        if not secret_id or not secret_key:
            secret_id, secret_key = self.config.load_credentials()
        
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.output_dir = "output"
        
        # 创建输出目录
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def get_regions_via_api(self) -> List[Dict]:
        """
        通过腾讯云API获取区域信息
        需要配置SecretId和SecretKey
        """
        try:
            # 检查SDK是否安装
            try:
                from tencentcloud.common import credential
                from tencentcloud.cvm.v20170312 import cvm_client, models
            except ImportError:
                logger.error("请安装腾讯云SDK: pip install tencentcloud-sdk-python")
                return []
            
            if not self.secret_id or not self.secret_key:
                logger.error("需要配置腾讯云SecretId和SecretKey")
                return []
            
            # 创建认证对象
            cred = credential.Credential(self.secret_id, self.secret_key)
            
            # 创建CVM客户端（使用默认区域）
            client = cvm_client.CvmClient(cred, "ap-guangzhou")
            
            # 创建请求对象
            req = models.DescribeRegionsRequest()
            
            # 发送请求
            response = client.DescribeRegions(req)
            
            regions = []
            for region in response.RegionSet:
                regions.append({
                    'region_id': region.Region,
                    'region_name': region.RegionName,
                    'region_state': region.RegionState,
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
            from tencentcloud.common import credential
            from tencentcloud.cvm.v20170312 import cvm_client, models
            
            if not self.secret_id or not self.secret_key:
                logger.error("需要配置腾讯云SecretId和SecretKey")
                return []
            
            # 创建认证对象
            cred = credential.Credential(self.secret_id, self.secret_key)
            
            # 创建CVM客户端
            client = cvm_client.CvmClient(cred, region_id)
            
            # 创建请求对象
            req = models.DescribeZonesRequest()
            
            # 发送请求
            response = client.DescribeZones(req)
            
            zones = []
            for zone in response.ZoneSet:
                zones.append({
                    'zone_id': zone.Zone,
                    'zone_name': zone.ZoneName,
                    'zone_state': zone.ZoneState,
                    'region_id': region_id,
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
            filename = f"tencentcloud_nodes_{timestamp}.json"
        
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
                filename = f"tencentcloud_nodes_{timestamp}.csv"
            
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
    print("腾讯云API节点信息获取工具")
    print("=" * 60)
    
    config = TencentCloudConfig()
    
    # 检查是否有保存的凭据
    if config.has_credentials():
        print("发现已保存的腾讯云凭据")
        use_saved = input("是否使用已保存的凭据? (y/n): ").strip().lower()
        
        if use_saved == 'y':
            secret_id, secret_key = config.load_credentials()
            print("使用已保存的凭据")
        else:
            # 输入新的凭据
            secret_id = input("请输入腾讯云SecretId: ").strip()
            secret_key = input("请输入腾讯云SecretKey: ").strip()
            
            # 询问是否保存新凭据
            if secret_id and secret_key:
                save_new = input("是否保存这些凭据供下次使用? (y/n): ").strip().lower()
                if save_new == 'y':
                    if config.save_credentials(secret_id, secret_key):
                        print("凭据已保存")
                    else:
                        print("凭据保存失败")
    else:
        # 没有保存的凭据，需要输入
        print("未发现保存的凭据")
        secret_id = input("请输入腾讯云SecretId: ").strip()
        secret_key = input("请输入腾讯云SecretKey: ").strip()
        
        # 询问是否保存凭据
        if secret_id and secret_key:
            save_new = input("是否保存这些凭据供下次使用? (y/n): ").strip().lower()
            if save_new == 'y':
                if config.save_credentials(secret_id, secret_key):
                    print("凭据已保存")
                else:
                    print("凭据保存失败")
    
    if not secret_id or not secret_key:
        print("错误: 必须提供SecretId和SecretKey")
        return
    
    tencentcloud_api = TencentCloudAPINodes(secret_id, secret_key)
    
    print("\n正在获取腾讯云全球节点信息...")
    
    # 获取所有区域和可用区信息
    all_data = tencentcloud_api.get_all_regions_with_zones()
    
    if all_data:
        regions = all_data['regions']
        print(f"\n成功获取 {len(regions)} 个区域:")
        print("-" * 60)
        
        # 按大洲分组显示
        grouped = {}
        for region in regions:
            # 根据region_id判断大洲
            region_id = region['region_id']
            if region_id.startswith('ap-'):
                if 'guangzhou' in region_id or 'shenzhen' in region_id or 'shanghai' in region_id or 'beijing' in region_id:
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
            tencentcloud_api.save_to_json(all_data, "tencentcloud_nodes_complete.json")
        elif choice == "2":
            # 将数据扁平化为CSV格式
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
                
                # 添加可用区信息
                zones = all_data['zones_by_region'].get(region['region_id'], [])
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
            
            tencentcloud_api.save_to_csv(flat_data, "tencentcloud_nodes_complete.csv")
        elif choice == "3":
            tencentcloud_api.save_to_json(all_data, "tencentcloud_nodes_complete.json")
            
            # 扁平化数据用于CSV
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
                
                zones = all_data['zones_by_region'].get(region['region_id'], [])
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
            
            tencentcloud_api.save_to_csv(flat_data, "tencentcloud_nodes_complete.csv")
        else:
            print("未选择保存")
        
        print("\n获取完成！")
    else:
        print("获取腾讯云节点信息失败")

if __name__ == "__main__":
    main() 