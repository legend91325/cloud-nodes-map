#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云API简单测试
用于验证SDK安装和基本功能
"""

import os
import sys

def test_tencentcloud_sdk():
    """测试腾讯云SDK是否正常安装"""
    try:
        from tencentcloud.common import credential
        from tencentcloud.cvm.v20170312 import cvm_client, models
        print("✓ 腾讯云SDK导入成功")
        return True
    except ImportError as e:
        print(f"✗ 腾讯云SDK导入失败: {e}")
        print("请运行: pip install tencentcloud-sdk-python")
        return False

def test_credentials():
    """测试凭据配置"""
    # 检查环境变量
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
    
    if secret_id and secret_key:
        print("✓ 发现环境变量中的腾讯云凭据")
        return secret_id, secret_key
    
    # 检查配置文件
    config_dir = os.path.expanduser("~/.tencentcloud")
    credentials_file = os.path.join(config_dir, "credentials")
    
    if os.path.exists(credentials_file):
        try:
            secret_id = None
            secret_key = None
            
            with open(credentials_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('secret_id'):
                        secret_id = line.split('=')[1].strip()
                    elif line.startswith('secret_key'):
                        secret_key = line.split('=')[1].strip()
            
            if secret_id and secret_key:
                print("✓ 发现配置文件中的腾讯云凭据")
                return secret_id, secret_key
        except Exception as e:
            print(f"✗ 读取配置文件失败: {e}")
    
    print("✗ 未发现腾讯云凭据")
    print("请设置环境变量 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY")
    print("或在 ~/.tencentcloud/credentials 文件中配置")
    return None, None

def test_api_connection(secret_id, secret_key):
    """测试API连接"""
    try:
        from tencentcloud.common import credential
        from tencentcloud.cvm.v20170312 import cvm_client, models
        
        # 创建认证对象
        cred = credential.Credential(secret_id, secret_key)
        
        # 创建CVM客户端
        client = cvm_client.CvmClient(cred, "ap-guangzhou")
        
        # 创建请求对象
        req = models.DescribeRegionsRequest()
        
        # 发送请求
        response = client.DescribeRegions(req)
        
        print(f"✓ API连接成功，获取到 {len(response.RegionSet)} 个区域")
        
        # 显示前几个区域
        print("\n前5个区域:")
        for i, region in enumerate(response.RegionSet[:5]):
            print(f"  {i+1}. {region.RegionName} ({region.Region}) - {region.RegionState}")
        
        return True
        
    except Exception as e:
        print(f"✗ API连接失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("腾讯云API简单测试")
    print("=" * 50)
    
    # 测试SDK安装
    if not test_tencentcloud_sdk():
        sys.exit(1)
    
    # 测试凭据
    secret_id, secret_key = test_credentials()
    if not secret_id or not secret_key:
        print("\n如需手动输入凭据进行测试，请修改此脚本")
        sys.exit(1)
    
    # 测试API连接
    if test_api_connection(secret_id, secret_key):
        print("\n✓ 所有测试通过！")
    else:
        print("\n✗ 测试失败")
        sys.exit(1)

if __name__ == "__main__":
    main() 