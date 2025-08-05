"""
云节点数据加载和处理工具
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

from .models import CloudProvider, CloudProviderData, CloudNode, Location, NetworkInfo, ServiceType, NodeStatus


class CloudDataLoader:
    """云节点数据加载器"""
    
    def __init__(self, data_dir: str = "data"):
        """
        初始化数据加载器
        
        Args:
            data_dir: 数据目录路径
        """
        self.data_dir = Path(data_dir)
        self.providers = {
            CloudProvider.ALIBABA_CLOUD: "alibaba-cloud",
            CloudProvider.HUAWEI_CLOUD: "huawei-cloud", 
            CloudProvider.TENCENT_CLOUD: "tencent-cloud",
            CloudProvider.AWS: "aws",
            CloudProvider.AZURE: "azure",
            CloudProvider.GOOGLE_CLOUD: "google-cloud"
        }
    
    def load_provider_data(self, provider: CloudProvider) -> Optional[CloudProviderData]:
        """
        加载指定云厂商的数据
        
        Args:
            provider: 云厂商枚举
            
        Returns:
            CloudProviderData对象，如果加载失败返回None
        """
        try:
            provider_dir = self.providers.get(provider)
            if not provider_dir:
                raise ValueError(f"不支持的云厂商: {provider}")
            
            data_file = self.data_dir / provider_dir / "nodes.json"
            if not data_file.exists():
                raise FileNotFoundError(f"数据文件不存在: {data_file}")
            
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 为每个节点添加provider信息
            nodes = []
            for node_data in data["nodes"]:
                # 为节点数据添加provider字段
                node_data_with_provider = node_data.copy()
                node_data_with_provider["provider"] = data["provider"]
                # 使用from_dict方法创建节点
                node = CloudNode.from_dict(node_data_with_provider)
                nodes.append(node)
            
            return CloudProviderData(
                provider=CloudProvider(data["provider"]),
                nodes=nodes,
                last_updated=datetime.fromisoformat(data["last_updated"]),
                version=data.get("version", "1.0.0")
            )
            
        except Exception as e:
            print(f"加载{provider.value}数据失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def load_all_providers(self) -> Dict[CloudProvider, CloudProviderData]:
        """
        加载所有云厂商的数据
        
        Returns:
            包含所有云厂商数据的字典
        """
        all_data = {}
        
        for provider in CloudProvider:
            data = self.load_provider_data(provider)
            if data:
                all_data[provider] = data
        
        return all_data
    
    def get_nodes_by_country(self, country: str) -> List[CloudNode]:
        """
        根据国家获取所有节点
        
        Args:
            country: 国家名称
            
        Returns:
            该国家的所有云节点列表
        """
        nodes = []
        all_data = self.load_all_providers()
        
        for provider_data in all_data.values():
            for node in provider_data.nodes:
                if node.location.country == country:
                    nodes.append(node)
        
        return nodes
    
    def get_nodes_by_region(self, region: str) -> List[CloudNode]:
        """
        根据地区获取所有节点
        
        Args:
            region: 地区名称
            
        Returns:
            该地区的所有云节点列表
        """
        nodes = []
        all_data = self.load_all_providers()
        
        for provider_data in all_data.values():
            for node in provider_data.nodes:
                if node.location.region == region:
                    nodes.append(node)
        
        return nodes
    
    def get_nodes_by_service_type(self, service_type: ServiceType) -> List[CloudNode]:
        """
        根据服务类型获取所有节点
        
        Args:
            service_type: 服务类型枚举
            
        Returns:
            支持该服务类型的所有云节点列表
        """
        nodes = []
        all_data = self.load_all_providers()
        
        for provider_data in all_data.values():
            for node in provider_data.nodes:
                if service_type in node.service_types:
                    nodes.append(node)
        
        return nodes
    
    def get_nodes_by_status(self, status: NodeStatus) -> List[CloudNode]:
        """
        根据节点状态获取所有节点
        
        Args:
            status: 节点状态枚举
            
        Returns:
            指定状态的所有云节点列表
        """
        nodes = []
        all_data = self.load_all_providers()
        
        for provider_data in all_data.values():
            for node in provider_data.nodes:
                if node.status == status:
                    nodes.append(node)
        
        return nodes
    
    def get_provider_statistics(self) -> Dict[str, Dict]:
        """
        获取各云厂商的统计信息
        
        Returns:
            包含各云厂商统计信息的字典
        """
        stats = {}
        all_data = self.load_all_providers()
        
        for provider, data in all_data.items():
            provider_name = provider.value
            
            # 按国家统计
            countries = {}
            for node in data.nodes:
                country = node.location.country
                countries[country] = countries.get(country, 0) + 1
            
            # 按服务类型统计
            service_types = {}
            for node in data.nodes:
                for service_type in node.service_types:
                    service_types[service_type.value] = service_types.get(service_type.value, 0) + 1
            
            # 按状态统计
            statuses = {}
            for node in data.nodes:
                status = node.status.value
                statuses[status] = statuses.get(status, 0) + 1
            
            stats[provider_name] = {
                "total_nodes": len(data.nodes),
                "countries": countries,
                "service_types": service_types,
                "statuses": statuses,
                "last_updated": data.last_updated.isoformat(),
                "version": data.version
            }
        
        return stats
    
    def search_nodes(self, keyword: str) -> List[CloudNode]:
        """
        搜索节点
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的云节点列表
        """
        nodes = []
        all_data = self.load_all_providers()
        
        keyword_lower = keyword.lower()
        
        for provider_data in all_data.values():
            for node in provider_data.nodes:
                # 搜索节点名称、描述、数据中心名称
                searchable_text = [
                    node.name.lower(),
                    node.description.lower() if node.description else "",
                    node.data_center.lower(),
                    node.location.country.lower(),
                    node.location.region.lower(),
                    node.location.city.lower()
                ]
                
                if any(keyword_lower in text for text in searchable_text):
                    nodes.append(node)
        
        return nodes
    
    def get_global_coverage(self) -> Dict[str, int]:
        """
        获取全球覆盖统计
        
        Returns:
            各国家的节点数量统计
        """
        coverage = {}
        all_data = self.load_all_providers()
        
        for provider_data in all_data.values():
            for node in provider_data.nodes:
                country = node.location.country
                coverage[country] = coverage.get(country, 0) + 1
        
        return dict(sorted(coverage.items(), key=lambda x: x[1], reverse=True))
    
    def export_to_csv(self, output_file: str, provider: Optional[CloudProvider] = None):
        """
        导出数据到CSV文件
        
        Args:
            output_file: 输出文件路径
            provider: 指定云厂商，如果为None则导出所有厂商
        """
        import csv
        
        if provider:
            all_data = {provider: self.load_provider_data(provider)}
        else:
            all_data = self.load_all_providers()
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # 写入表头
            writer.writerow([
                'Provider', 'Node ID', 'Name', 'Country', 'Region', 'City',
                'Latitude', 'Longitude', 'Data Center', 'Availability Zone',
                'Service Types', 'Status', 'Bandwidth', 'Latency', 'Uptime',
                'Description', 'Launch Date'
            ])
            
            # 写入数据
            for provider_enum, provider_data in all_data.items():
                if not provider_data:
                    continue
                    
                for node in provider_data.nodes:
                    writer.writerow([
                        provider_enum.value,
                        node.node_id,
                        node.name,
                        node.location.country,
                        node.location.region,
                        node.location.city,
                        node.location.latitude or '',
                        node.location.longitude or '',
                        node.data_center,
                        node.availability_zone,
                        ','.join([st.value for st in node.service_types]),
                        node.status.value,
                        node.network_info.bandwidth if node.network_info else '',
                        node.network_info.latency if node.network_info else '',
                        node.network_info.uptime if node.network_info else '',
                        node.description or '',
                        node.launch_date.isoformat() if node.launch_date else ''
                    ])
        
        print(f"数据已导出到: {output_file}")
    
    def validate_data(self) -> Dict[str, List[str]]:
        """
        验证数据完整性
        
        Returns:
            包含验证结果的字典
        """
        errors = {}
        all_data = self.load_all_providers()
        
        for provider, data in all_data.items():
            provider_errors = []
            
            if not data:
                provider_errors.append("无法加载数据文件")
                errors[provider.value] = provider_errors
                continue
            
            for i, node in enumerate(data.nodes):
                # 检查必需字段
                if not node.node_id:
                    provider_errors.append(f"节点 {i}: 缺少节点ID")
                
                if not node.name:
                    provider_errors.append(f"节点 {i}: 缺少节点名称")
                
                if not node.location.country:
                    provider_errors.append(f"节点 {i}: 缺少国家信息")
                
                if not node.location.city:
                    provider_errors.append(f"节点 {i}: 缺少城市信息")
                
                # 检查坐标范围
                if node.location.latitude is not None:
                    if not -90 <= node.location.latitude <= 90:
                        provider_errors.append(f"节点 {i}: 纬度超出范围")
                
                if node.location.longitude is not None:
                    if not -180 <= node.location.longitude <= 180:
                        provider_errors.append(f"节点 {i}: 经度超出范围")
                
                # 检查网络延迟
                if node.network_info and node.network_info.latency is not None:
                    if node.network_info.latency < 0:
                        provider_errors.append(f"节点 {i}: 网络延迟不能为负数")
            
            if provider_errors:
                errors[provider.value] = provider_errors
        
        return errors 