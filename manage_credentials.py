#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云凭据管理工具
"""

from aliyun_config import AliyunConfig

def main():
    print("=" * 50)
    print("阿里云凭据管理工具")
    print("=" * 50)
    
    config = AliyunConfig()
    
    while True:
        print("\n请选择操作:")
        print("1. 查看凭据状态")
        print("2. 保存新凭据")
        print("3. 清除已保存的凭据")
        print("4. 退出")
        
        choice = input("\n请输入选择 (1-4): ").strip()
        
        if choice == "1":
            print("\n" + "=" * 30)
            print("凭据状态")
            print("=" * 30)
            
            if config.has_credentials():
                print("✓ 已保存凭据")
                print(f"配置文件路径: {config.get_config_path()}")
                
                # 测试凭据是否有效
                access_key_id, access_key_secret = config.load_credentials()
                print(f"AccessKey ID: {access_key_id[:8]}...")
                print(f"AccessKey Secret: {access_key_secret[:8]}...")
            else:
                print("✗ 未保存凭据")
                print(f"配置文件路径: {config.get_config_path()}")
        
        elif choice == "2":
            print("\n" + "=" * 30)
            print("保存新凭据")
            print("=" * 30)
            
            access_key_id = input("请输入阿里云AccessKey ID: ").strip()
            access_key_secret = input("请输入阿里云AccessKey Secret: ").strip()
            
            if access_key_id and access_key_secret:
                if config.save_credentials(access_key_id, access_key_secret):
                    print("✓ 凭据保存成功")
                else:
                    print("✗ 凭据保存失败")
            else:
                print("✗ AccessKey ID和Secret不能为空")
        
        elif choice == "3":
            print("\n" + "=" * 30)
            print("清除凭据")
            print("=" * 30)
            
            confirm = input("确定要清除已保存的凭据吗? (y/n): ").strip().lower()
            if confirm == 'y':
                if config.clear_credentials():
                    print("✓ 凭据已清除")
                else:
                    print("✗ 凭据清除失败")
            else:
                print("操作已取消")
        
        elif choice == "4":
            print("退出程序")
            break
        
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main() 