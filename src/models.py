"""
云节点数据模型定义
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum
import json
from datetime import datetime


class CloudProvider(Enum):
    """云厂商枚举"""
    ALIBABA_CLOUD = "alibaba_cloud"
    HUAWEI_CLOUD = "huawei_cloud"
    TENCENT_CLOUD = "tencent_cloud"
    AWS = "aws"
    AZURE = "azure"
    GOOGLE_CLOUD = "google_cloud"


class ServiceType(Enum):
    """服务类型枚举"""
    COMPUTE = "compute"
    STORAGE = "storage"
    NETWORK = "network"
    DATABASE = "database"
    CDN = "cdn"
    AI = "ai"
    SECURITY = "security"


class NodeStatus(Enum):
    """节点状态枚举"""
    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    DEPRECATED = "deprecated"
    PLANNED = "planned"


@dataclass
class Location:
    """地理位置信息"""
    country: str
    region: str
    city: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass
class NetworkInfo:
    """网络信息"""
    bandwidth: Optional[str] = None
    latency: Optional[float] = None  # 毫秒
    uptime: Optional[float] = None   # 百分比


@dataclass
class CloudNode:
    """云节点数据模型"""
    node_id: str
    name: str
    provider: CloudProvider
    location: Location
    data_center: str
    availability_zone: str
    service_types: List[ServiceType]
    status: NodeStatus
    network_info: Optional[NetworkInfo] = None
    description: Optional[str] = None
    launch_date: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "node_id": self.node_id,
            "name": self.name,
            "provider": self.provider.value,
            "location": {
                "country": self.location.country,
                "region": self.location.region,
                "city": self.location.city,
                "latitude": self.location.latitude,
                "longitude": self.location.longitude
            },
            "data_center": self.data_center,
            "availability_zone": self.availability_zone,
            "service_types": [st.value for st in self.service_types],
            "status": self.status.value,
            "network_info": {
                "bandwidth": self.network_info.bandwidth,
                "latency": self.network_info.latency,
                "uptime": self.network_info.uptime
            } if self.network_info else None,
            "description": self.description,
            "launch_date": self.launch_date.isoformat() if self.launch_date else None,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CloudNode':
        """从字典创建实例"""
        return cls(
            node_id=data["node_id"],
            name=data["name"],
            provider=CloudProvider(data["provider"]),
            location=Location(**data["location"]),
            data_center=data["data_center"],
            availability_zone=data["availability_zone"],
            service_types=[ServiceType(st) for st in data["service_types"]],
            status=NodeStatus(data["status"]),
            network_info=NetworkInfo(**data["network_info"]) if data.get("network_info") else None,
            description=data.get("description"),
            launch_date=datetime.fromisoformat(data["launch_date"]) if data.get("launch_date") else None,
            metadata=data.get("metadata")
        )


@dataclass
class CloudProviderData:
    """云厂商数据集合"""
    provider: CloudProvider
    nodes: List[CloudNode]
    last_updated: datetime
    version: str = "1.0.0"

    def to_json(self, filepath: str) -> None:
        """保存为JSON文件"""
        data = {
            "provider": self.provider.value,
            "nodes": [node.to_dict() for node in self.nodes],
            "last_updated": self.last_updated.isoformat(),
            "version": self.version
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, filepath: str) -> 'CloudProviderData':
        """从JSON文件加载"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls(
            provider=CloudProvider(data["provider"]),
            nodes=[CloudNode.from_dict(node_data) for node_data in data["nodes"]],
            last_updated=datetime.fromisoformat(data["last_updated"]),
            version=data.get("version", "1.0.0")
        ) 