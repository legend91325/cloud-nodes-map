#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云服务商数据验证脚本
用于验证所有云服务商数据文件的完整性和正确性
"""

import json
import os
from datetime import datetime

class DataValidator:
    def __init__(self):
        self.providers = [
            'alibaba-cloud', 'aws', 'azure', 'google-cloud',
            'huawei-cloud', 'tencent-cloud', 'volcano-engine',
            'oracle-cloud', 'ibm-cloud', 'ovh-cloud', 'digitalocean'
        ]
        self.errors = []
        self.warnings = []
        self.stats = {}
    
    def validate_all(self):
        """验证所有云服务商数据"""
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║              云服务商数据完整性验证工具                          ║")
        print("╚════════════════════════════════════════════════════════════════╝\n")
        
        for provider in self.providers:
            self.validate_provider(provider)
        
        self.print_summary()
    
    def validate_provider(self, provider_id):
        """验证单个云服务商数据"""
        file_path = f'data/{provider_id}/nodes.json'
        
        print(f"📋 验证 {provider_id}...")
        
        # 检查文件存在性
        if not os.path.exists(file_path):
            error_msg = f"文件不存在: {file_path}"
            self.errors.append((provider_id, error_msg))
            print(f"   ❌ {error_msg}")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 验证顶层字段
            self.validate_top_level_fields(provider_id, data)
            
            # 验证节点数据
            self.validate_nodes(provider_id, data.get('nodes', []))
            
            # 统计信息
            nodes_count = len(data.get('nodes', []))
            countries = set(node['location']['country'] for node in data.get('nodes', []))
            
            self.stats[provider_id] = {
                'nodes': nodes_count,
                'countries': len(countries),
                'version': data.get('version', 'N/A'),
                'last_updated': data.get('last_updated', 'N/A')
            }
            
            print(f"   ✅ 格式正确 - {nodes_count}个节点，覆盖{len(countries)}个国家")
            
        except json.JSONDecodeError as e:
            error_msg = f"JSON格式错误: {e}"
            self.errors.append((provider_id, error_msg))
            print(f"   ❌ {error_msg}")
        except Exception as e:
            error_msg = f"验证出错: {e}"
            self.errors.append((provider_id, error_msg))
            print(f"   ❌ {error_msg}")
    
    def validate_top_level_fields(self, provider_id, data):
        """验证顶层必需字段"""
        required_fields = ['provider', 'version', 'nodes']
        
        for field in required_fields:
            if field not in data:
                error_msg = f"缺少必需字段: {field}"
                self.errors.append((provider_id, error_msg))
        
        # 检查 provider 字段是否匹配
        if 'provider' in data:
            expected_provider = provider_id.replace('-', '_')
            if data['provider'] != expected_provider:
                warning_msg = f"provider字段不匹配: {data['provider']} != {expected_provider}"
                self.warnings.append((provider_id, warning_msg))
    
    def validate_nodes(self, provider_id, nodes):
        """验证节点数据"""
        if not nodes:
            warning_msg = "节点列表为空"
            self.warnings.append((provider_id, warning_msg))
            return
        
        for i, node in enumerate(nodes):
            # 验证必需字段
            required_node_fields = [
                'node_id', 'name', 'location', 'status'
            ]
            
            for field in required_node_fields:
                if field not in node:
                    error_msg = f"节点 {i} ({node.get('node_id', 'unknown')}) 缺少字段: {field}"
                    self.errors.append((provider_id, error_msg))
            
            # 验证 location 字段
            if 'location' in node:
                self.validate_location(provider_id, i, node['location'], node.get('node_id', 'unknown'))
            
            # 验证经纬度范围
            if 'location' in node:
                lat = node['location'].get('latitude')
                lon = node['location'].get('longitude')
                
                if lat is not None and (lat < -90 or lat > 90):
                    error_msg = f"节点 {node.get('node_id')} 纬度超出范围: {lat}"
                    self.errors.append((provider_id, error_msg))
                
                if lon is not None and (lon < -180 or lon > 180):
                    error_msg = f"节点 {node.get('node_id')} 经度超出范围: {lon}"
                    self.errors.append((provider_id, error_msg))
            
            # 检查状态
            if 'status' in node and node['status'] not in ['active', 'planned', 'retired']:
                warning_msg = f"节点 {node.get('node_id')} 状态异常: {node['status']}"
                self.warnings.append((provider_id, warning_msg))
    
    def validate_location(self, provider_id, node_index, location, node_id):
        """验证位置信息"""
        required_location_fields = ['country', 'city', 'latitude', 'longitude']
        
        for field in required_location_fields:
            if field not in location:
                error_msg = f"节点 {node_id} 位置信息缺少字段: {field}"
                self.errors.append((provider_id, error_msg))
    
    def print_summary(self):
        """打印验证摘要"""
        print("\n" + "="*66)
        print("📊 验证摘要\n")
        
        # 统计信息表格
        if self.stats:
            print("┌─────────────────┬────────┬──────────┬───────────┬────────────────┐")
            print("│  云服务商       │ 节点数 │ 国家数   │ 版本      │ 最后更新       │")
            print("├─────────────────┼────────┼──────────┼───────────┼────────────────┤")
            
            total_nodes = 0
            total_countries = set()
            
            for provider, stats in sorted(self.stats.items()):
                name = provider.replace('-', ' ').title()
                nodes = stats['nodes']
                countries = stats['countries']
                version = stats['version']
                updated = stats.get('last_updated', 'N/A')[:10]
                
                total_nodes += nodes
                
                print(f"│ {name:<15} │ {nodes:>6} │ {countries:>8} │ {version:<9} │ {updated:<14} │")
            
            print("└─────────────────┴────────┴──────────┴───────────┴────────────────┘")
            print(f"\n总计: {len(self.stats)}个云服务商，{total_nodes}个节点\n")
        
        # 错误信息
        if self.errors:
            print(f"❌ 发现 {len(self.errors)} 个错误:\n")
            for provider, error in self.errors:
                print(f"   [{provider}] {error}")
            print()
        else:
            print("✅ 未发现错误\n")
        
        # 警告信息
        if self.warnings:
            print(f"⚠️  发现 {len(self.warnings)} 个警告:\n")
            for provider, warning in self.warnings:
                print(f"   [{provider}] {warning}")
            print()
        else:
            print("✅ 未发现警告\n")
        
        # 最终结论
        print("="*66)
        if not self.errors:
            print("🎉 所有数据文件格式正确！")
        else:
            print("⚠️  请修复上述错误后重新验证")
        print("="*66)


def main():
    validator = DataValidator()
    validator.validate_all()


if __name__ == '__main__':
    main()

