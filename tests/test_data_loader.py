"""
数据加载器测试
"""

import pytest
import tempfile
import json
import os
from pathlib import Path

from src.data_loader import CloudDataLoader
from src.models import CloudProvider, CloudProviderData, CloudNode, Location, NetworkInfo, ServiceType, NodeStatus


class TestCloudDataLoader:
    """CloudDataLoader测试类"""
    
    def setup_method(self):
        """测试前准备"""
        # 创建临时测试数据目录
        self.temp_dir = tempfile.mkdtemp()
        self.test_data_dir = Path(self.temp_dir) / "test_data"
        self.test_data_dir.mkdir()
        
        # 创建测试数据
        self.create_test_data()
        
        # 初始化加载器
        self.loader = CloudDataLoader(str(self.test_data_dir))
    
    def teardown_method(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_data(self):
        """创建测试数据"""
        # 创建阿里云测试数据
        alibaba_dir = self.test_data_dir / "alibaba-cloud"
        alibaba_dir.mkdir()
        
        alibaba_data = {
            "provider": "alibaba_cloud",
            "version": "1.0.0",
            "last_updated": "2024-01-15T00:00:00",
            "nodes": [
                {
                    "node_id": "cn-hangzhou",
                    "name": "华东1（杭州）",
                    "location": {
                        "country": "中国",
                        "region": "华东",
                        "city": "杭州",
                        "latitude": 30.2741,
                        "longitude": 120.1551
                    },
                    "data_center": "阿里云杭州数据中心",
                    "availability_zone": "cn-hangzhou-a",
                    "service_types": ["compute", "storage", "network", "database", "cdn", "ai", "security"],
                    "status": "active",
                    "network_info": {
                        "bandwidth": "100Gbps",
                        "latency": 5.2,
                        "uptime": 99.95
                    },
                    "description": "阿里云华东1区域主数据中心",
                    "launch_date": "2009-09-10T00:00:00"
                }
            ]
        }
        
        with open(alibaba_dir / "nodes.json", 'w', encoding='utf-8') as f:
            json.dump(alibaba_data, f, ensure_ascii=False, indent=2)
    
    def test_load_provider_data(self):
        """测试加载云厂商数据"""
        data = self.loader.load_provider_data(CloudProvider.ALIBABA_CLOUD)
        
        assert data is not None
        assert data.provider == CloudProvider.ALIBABA_CLOUD
        assert len(data.nodes) == 1
        assert data.nodes[0].node_id == "cn-hangzhou"
        assert data.nodes[0].name == "华东1（杭州）"
    
    def test_load_nonexistent_provider(self):
        """测试加载不存在的云厂商数据"""
        data = self.loader.load_provider_data(CloudProvider.AWS)
        assert data is None
    
    def test_get_nodes_by_country(self):
        """测试按国家查询节点"""
        nodes = self.loader.get_nodes_by_country("中国")
        assert len(nodes) == 1
        assert nodes[0].location.country == "中国"
    
    def test_get_nodes_by_region(self):
        """测试按地区查询节点"""
        nodes = self.loader.get_nodes_by_region("华东")
        assert len(nodes) == 1
        assert nodes[0].location.region == "华东"
    
    def test_get_nodes_by_service_type(self):
        """测试按服务类型查询节点"""
        nodes = self.loader.get_nodes_by_service_type(ServiceType.AI)
        assert len(nodes) == 1
        assert ServiceType.AI in nodes[0].service_types
    
    def test_get_nodes_by_status(self):
        """测试按状态查询节点"""
        nodes = self.loader.get_nodes_by_status(NodeStatus.ACTIVE)
        assert len(nodes) == 1
        assert nodes[0].status == NodeStatus.ACTIVE
    
    def test_search_nodes(self):
        """测试搜索节点"""
        nodes = self.loader.search_nodes("杭州")
        assert len(nodes) == 1
        assert "杭州" in nodes[0].location.city
    
    def test_get_provider_statistics(self):
        """测试获取云厂商统计信息"""
        stats = self.loader.get_provider_statistics()
        
        assert "alibaba_cloud" in stats
        alibaba_stats = stats["alibaba_cloud"]
        
        assert alibaba_stats["total_nodes"] == 1
        assert "中国" in alibaba_stats["countries"]
        assert alibaba_stats["countries"]["中国"] == 1
        assert "ai" in alibaba_stats["service_types"]
        assert alibaba_stats["statuses"]["active"] == 1
    
    def test_get_global_coverage(self):
        """测试获取全球覆盖统计"""
        coverage = self.loader.get_global_coverage()
        
        assert "中国" in coverage
        assert coverage["中国"] == 1
    
    def test_validate_data(self):
        """测试数据验证"""
        errors = self.loader.validate_data()
        
        # 测试数据应该是有效的
        assert not errors
    
    def test_validate_data_with_errors(self):
        """测试数据验证（包含错误）"""
        # 创建包含错误的数据
        invalid_data = {
            "provider": "alibaba_cloud",
            "version": "1.0.0",
            "last_updated": "2024-01-15T00:00:00",
            "nodes": [
                {
                    "node_id": "",  # 空节点ID
                    "name": "测试节点",
                    "location": {
                        "country": "中国",
                        "region": "华东",
                        "city": "杭州",
                        "latitude": 200.0,  # 无效纬度
                        "longitude": 120.1551
                    },
                    "data_center": "测试数据中心",
                    "availability_zone": "test-zone",
                    "service_types": ["compute"],
                    "status": "active",
                    "network_info": {
                        "bandwidth": "100Gbps",
                        "latency": -5.0,  # 负延迟
                        "uptime": 99.95
                    },
                    "description": "测试节点",
                    "launch_date": "2009-09-10T00:00:00"
                }
            ]
        }
        
        # 写入无效数据
        alibaba_dir = self.test_data_dir / "alibaba-cloud"
        with open(alibaba_dir / "nodes.json", 'w', encoding='utf-8') as f:
            json.dump(invalid_data, f, ensure_ascii=False, indent=2)
        
        # 重新加载并验证
        loader = CloudDataLoader(str(self.test_data_dir))
        errors = loader.validate_data()
        
        assert "alibaba_cloud" in errors
        assert len(errors["alibaba_cloud"]) > 0
    
    def test_export_to_csv(self):
        """测试导出到CSV"""
        import tempfile
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            csv_file = f.name
        
        try:
            self.loader.export_to_csv(csv_file)
            
            # 检查文件是否存在且不为空
            assert os.path.exists(csv_file)
            assert os.path.getsize(csv_file) > 0
            
            # 检查CSV内容
            with open(csv_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                assert len(lines) >= 2  # 至少包含表头和数据行
                assert "Provider" in lines[0]  # 包含表头
                assert "alibaba_cloud" in lines[1]  # 包含数据
                
        finally:
            if os.path.exists(csv_file):
                os.unlink(csv_file)


if __name__ == "__main__":
    pytest.main([__file__]) 