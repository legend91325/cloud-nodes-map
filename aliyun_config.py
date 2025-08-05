#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云配置文件管理模块
"""

import json
import os
import base64
from pathlib import Path
from typing import Dict, Optional, Tuple

class AliyunConfig:
    """阿里云配置管理类"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".aliyun_config"
        self.config_file = self.config_dir / "credentials.json"
        self._ensure_config_dir()
    
    def _ensure_config_dir(self):
        """确保配置目录存在"""
        self.config_dir.mkdir(exist_ok=True)
        # 设置目录权限为只有用户可读写
        os.chmod(self.config_dir, 0o700)
    
    def _encode_credentials(self, access_key_id: str, access_key_secret: str) -> str:
        """简单编码凭据（不是加密，只是基本混淆）"""
        credentials = f"{access_key_id}:{access_key_secret}"
        return base64.b64encode(credentials.encode()).decode()
    
    def _decode_credentials(self, encoded_credentials: str) -> Tuple[str, str]:
        """解码凭据"""
        try:
            credentials = base64.b64decode(encoded_credentials.encode()).decode()
            access_key_id, access_key_secret = credentials.split(':', 1)
            return access_key_id, access_key_secret
        except Exception:
            return "", ""
    
    def save_credentials(self, access_key_id: str, access_key_secret: str) -> bool:
        """保存凭据到配置文件"""
        try:
            encoded_credentials = self._encode_credentials(access_key_id, access_key_secret)
            
            config_data = {
                "access_key_encoded": encoded_credentials,
                "saved_time": str(Path().stat().st_mtime) if self.config_file.exists() else ""
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2)
            
            # 设置文件权限为只有用户可读写
            os.chmod(self.config_file, 0o600)
            
            return True
        except Exception as e:
            print(f"保存凭据失败: {e}")
            return False
    
    def load_credentials(self) -> Tuple[str, str]:
        """从配置文件加载凭据"""
        try:
            if not self.config_file.exists():
                return "", ""
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            encoded_credentials = config_data.get("access_key_encoded", "")
            if encoded_credentials:
                return self._decode_credentials(encoded_credentials)
            
            return "", ""
        except Exception as e:
            print(f"加载凭据失败: {e}")
            return "", ""
    
    def has_credentials(self) -> bool:
        """检查是否有保存的凭据"""
        access_key_id, access_key_secret = self.load_credentials()
        return bool(access_key_id and access_key_secret)
    
    def clear_credentials(self) -> bool:
        """清除保存的凭据"""
        try:
            if self.config_file.exists():
                self.config_file.unlink()
            return True
        except Exception as e:
            print(f"清除凭据失败: {e}")
            return False
    
    def get_config_path(self) -> str:
        """获取配置文件路径"""
        return str(self.config_file)

def get_credentials() -> Tuple[str, str]:
    """获取阿里云凭据的便捷函数"""
    config = AliyunConfig()
    return config.load_credentials()

def save_credentials(access_key_id: str, access_key_secret: str) -> bool:
    """保存阿里云凭据的便捷函数"""
    config = AliyunConfig()
    return config.save_credentials(access_key_id, access_key_secret) 