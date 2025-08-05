#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版阿里云节点信息获取测试
"""

import json
import logging
from datetime import datetime

# 导入配置管理模块
from aliyun_config import AliyunConfig, get_credentials, save_credentials

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_regions_simple(access_key_id: str, access_key_secret: str):
    """简化版获取区域信息"""
    try:
        from aliyunsdkcore.client import AcsClient
        from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest
        
        # 创建ACS客户端
        client = AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')
        
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
        logger.error(f"获取区域信息失败: {e}")
        return []

def main():
    print("=" * 50)
    print("阿里云节点信息获取测试")
    print("=" * 50)
    
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
    
    print("\n正在获取区域信息...")
    regions = get_regions_simple(access_key_id, access_key_secret)
    
    if regions:
        print(f"\n成功获取 {len(regions)} 个区域:")
        for region in regions:
            print(f"  - {region['region_name']} ({region['region_id']})")
        
        # 保存到文件
        with open('regions_test.json', 'w', encoding='utf-8') as f:
            json.dump(regions, f, ensure_ascii=False, indent=2)
        print(f"\n区域信息已保存到 regions_test.json")
    else:
        print("获取区域信息失败")

if __name__ == "__main__":
    main() 