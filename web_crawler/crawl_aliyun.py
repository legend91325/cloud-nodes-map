#!/usr/bin/env python3
"""
阿里云全球基础设施爬虫脚本
爬取 https://www.alibabacloud.com/zh/global-locations 页面数据
生成符合项目数据格式的 nodes.json 文件
"""

import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, quote
import urllib3

import requests
from bs4 import BeautifulSoup

# 禁用SSL警告（如果使用verify=False）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AliyunCrawler:
    """阿里云基础设施爬虫类"""
    
    def __init__(self, use_api: bool = True):
        """
        初始化爬虫
        
        Args:
            use_api: 是否使用API获取坐标和大洲信息（默认True）
                     如果为False，将使用内置的备用数据
        """
        self.base_url = "https://www.alibabacloud.com/zh/global-locations"
        self.use_api = use_api
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        
        # API配置
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.restcountries_url = "https://restcountries.com/v3.1"
        
        # 缓存机制，避免重复请求
        self.coordinates_cache: Dict[str, Tuple[float, float]] = {}
        self.continent_cache: Dict[str, str] = {}
        
        # 国家名称映射（中文到英文，用于API查询）
        self.country_name_mapping = {
            "中国": "China",
            "印度尼西亚": "Indonesia",
            "新加坡": "Singapore",
            "日本": "Japan",
            "沙特阿拉伯": "Saudi Arabia",
            "泰国": "Thailand",
            "菲律宾": "Philippines",
            "阿联酋": "United Arab Emirates",
            "韩国": "South Korea",
            "马来西亚": "Malaysia",
            "德国": "Germany",
            "英国": "United Kingdom",
            "墨西哥": "Mexico",
            "美国": "United States",
        }
        
        # 区域ID映射规则
        self.region_id_mapping = {
            "华北1（青岛）": "cn-qingdao",
            "华北2（北京）": "cn-beijing",
            "华北3（张家口）": "cn-zhangjiakou",
            "华北5（呼和浩特）": "cn-huhehaote",
            "华北6（乌兰察布）": "cn-wulanchabu",
            "华东1（杭州）": "cn-hangzhou",
            "华东2（上海）": "cn-shanghai",
            "华东5（南京-本地地域）": "cn-nanjing",
            "华东6（福州-本地地域）": "cn-fuzhou",
            "华南1（深圳）": "cn-shenzhen",
            "华南2（河源）": "cn-heyuan",
            "华南3（广州）": "cn-guangzhou",
            "西南1（成都）": "cn-chengdu",
            "华中1（武汉-本地地域）": "cn-wuhan",
            "中国香港": "cn-hongkong",
            "新加坡": "ap-southeast-1",
            "泰国（曼谷）": "ap-southeast-6",
            "马来西亚（吉隆坡）": "ap-southeast-3",
            "印度尼西亚（雅加达）": "ap-southeast-4",
            "菲律宾（马尼拉）": "ap-southeast-5",
            "日本（东京）": "ap-northeast-1",
            "韩国（首尔）": "ap-northeast-2",
            "美国（弗吉尼亚）": "us-east-1",
            "美国（硅谷）": "us-west-1",
            "墨西哥（克雷塔罗）": "us-mexico-1",
            "德国（法兰克福）": "eu-central-1",
            "英国（伦敦）": "eu-west-1",
            "阿联酋（迪拜）": "me-east-1",
            "沙特（利雅得-合作伙伴运营）": "me-south-1",
        }
    
    def fetch_page(self) -> Optional[str]:
        """获取页面内容"""
        try:
            print(f"正在获取页面: {self.base_url}")
            # 尝试使用verify=True（默认），如果失败则尝试verify=False
            try:
                response = self.session.get(self.base_url, timeout=30, verify=True)
                response.raise_for_status()
            except requests.exceptions.SSLError:
                print("  ⚠ SSL证书验证失败，尝试禁用SSL验证...")
                # 如果SSL验证失败，尝试禁用验证（仅用于开发环境）
                response = self.session.get(self.base_url, timeout=30, verify=False)
                response.raise_for_status()
                print("  ⚠ 警告: SSL验证已禁用，仅用于开发环境")
            
            response.encoding = 'utf-8'
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"获取页面失败: {e}")
            print("提示: 如果遇到SSL证书问题，可以尝试安装certifi: pip install certifi")
            return None
        except Exception as e:
            print(f"获取页面失败: {e}")
            return None
    
    def parse_region_info(self, text: str) -> List[Dict]:
        """从页面文本中解析区域信息"""
        regions = []
        
        # 使用正则表达式匹配区域信息
        # 格式: * 区域名称\n可用区： 数量\n推出于 年份
        pattern = r'\*\s+([^\n]+)\s*\n可用区：\s*(\d+)\s*\n推出于\s*(\d{4})'
        matches = re.findall(pattern, text)
        
        for match in matches:
            name = match[0].strip()
            az_count = int(match[1])
            launch_year = int(match[2])
            
            # 解析城市和国家
            city, country = self.parse_location_from_name(name)
            
            # 获取坐标
            lat, lon = self.get_coordinates(city, country)
            
            # 获取大洲（优先使用API，失败则使用默认值）
            if self.use_api:
                continent = self.get_continent_from_api(country) or "亚洲"
            else:
                # 使用备用大洲映射
                continent = self._get_continent_fallback(country)
            
            # 获取区域ID
            node_id = self.region_id_mapping.get(name, self.generate_node_id(name, country))
            
            # 生成可用区列表
            availability_zones = self.generate_availability_zones(node_id, az_count)
            
            region = {
                "location": {
                    "country": country,
                    "city": city,
                    "latitude": lat,
                    "longitude": lon,
                    "continent": continent
                },
                "status": "active",
                "launch_date": f"{launch_year}-01-01T00:00:00",
                "node_id": node_id,
                "name": name,
                "availability_zones": availability_zones
            }
            
            # 检查是否是关停中的区域
            if "关停中" in name:
                region["status"] = "deprecated"
            
            regions.append(region)
        
        return regions
    
    def parse_location_from_name(self, name: str) -> tuple:
        """从区域名称解析城市和国家"""
        # 中国区域
        if name.startswith("华北") or name.startswith("华东") or name.startswith("华南") or \
           name.startswith("西南") or name.startswith("华中"):
            # 提取城市名
            city_match = re.search(r'（([^）]+)）', name)
            if city_match:
                city = city_match.group(1).split('-')[0].split('（')[0]
                return city, "中国"
            return "未知", "中国"
        
        # 中国香港
        if "香港" in name:
            return "香港", "中国"
        
        # 国际区域
        # 格式: 国家（城市）或 城市
        if "（" in name and "）" in name:
            # 提取国家名和城市名
            match = re.match(r'([^（]+)（([^）]+)）', name)
            if match:
                country = match.group(1).strip()
                city = match.group(2).strip()
                # 处理特殊情况
                if "合作伙伴运营" in city:
                    city = city.split('-')[0]
                return city, country
        
        # 如果没有括号，可能是城市名
        if name in ["新加坡"]:
            return name, name
        
        return "未知", "未知"
    
    def get_coordinates_from_api(self, city: str, country: str) -> Optional[Tuple[float, float]]:
        """使用Nominatim API获取城市坐标"""
        cache_key = f"{city},{country}"
        if cache_key in self.coordinates_cache:
            return self.coordinates_cache[cache_key]
        
        try:
            # 构建查询字符串
            # 处理特殊情况
            if city == "硅谷":
                query = "San Jose, California, United States"
            elif city == "弗吉尼亚":
                query = "Virginia, United States"
            elif country == "中国":
                query = f"{city}, China"
            else:
                query = f"{city}, {country}"
            
            params = {
                'q': query,
                'format': 'json',
                'limit': 1,
                'addressdetails': 1
            }
            
            # 添加延迟，遵守Nominatim的使用政策（1秒1次请求）
            time.sleep(1)
            
            response = self.session.get(self.nominatim_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data and len(data) > 0:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                self.coordinates_cache[cache_key] = (lat, lon)
                print(f"  ✓ 从API获取 {city}, {country} 的坐标: ({lat}, {lon})")
                return (lat, lon)
        except Exception as e:
            print(f"  ⚠ 获取 {city}, {country} 坐标失败: {e}")
        
        return None
    
    def get_continent_from_api(self, country: str) -> Optional[str]:
        """使用REST Countries API获取国家所属大洲"""
        if country in self.continent_cache:
            return self.continent_cache[country]
        
        try:
            # 将中文国家名转换为英文
            country_en = self.country_name_mapping.get(country, country)
            
            # 构建查询URL
            url = f"{self.restcountries_url}/name/{quote(country_en)}"
            params = {'fields': 'continents'}
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data and len(data) > 0:
                # REST Countries API返回的continents是数组
                continents = data[0].get('continents', [])
                if continents:
                    continent = continents[0]
                    # 映射到中文大洲名
                    continent_mapping = {
                        'Asia': '亚洲',
                        'Europe': '欧洲',
                        'North America': '北美洲',
                        'South America': '南美洲',
                        'Africa': '非洲',
                        'Oceania': '大洋洲',
                        'Antarctica': '南极洲'
                    }
                    continent_cn = continent_mapping.get(continent, continent)
                    self.continent_cache[country] = continent_cn
                    print(f"  ✓ 从API获取 {country} 的大洲: {continent_cn}")
                    return continent_cn
        except Exception as e:
            print(f"  ⚠ 获取 {country} 大洲失败: {e}")
        
        return None
    
    def _get_continent_fallback(self, country: str) -> str:
        """获取大洲信息（备用方法，不使用API）"""
        country_to_continent = {
            "中国": "亚洲",
            "印度尼西亚": "亚洲",
            "新加坡": "亚洲",
            "日本": "亚洲",
            "沙特阿拉伯": "亚洲",
            "泰国": "亚洲",
            "菲律宾": "亚洲",
            "阿联酋": "亚洲",
            "韩国": "亚洲",
            "马来西亚": "亚洲",
            "德国": "欧洲",
            "英国": "欧洲",
            "墨西哥": "北美洲",
            "美国": "北美洲",
        }
        return country_to_continent.get(country, "亚洲")
    
    def get_coordinates(self, city: str, country: str) -> tuple:
        """获取城市坐标（优先使用API，失败则使用备用数据）"""
        # 如果启用API，先尝试从API获取
        if self.use_api:
            coords = self.get_coordinates_from_api(city, country)
            if coords:
                return coords
        
        # API失败时使用备用坐标数据
        backup_coordinates = {
            "北京": (39.9042, 116.4074),
            "成都": (30.5728, 104.0668),
            "福州": (26.0745, 119.2965),
            "广州": (23.1291, 113.2644),
            "杭州": (30.2741, 120.1551),
            "河源": (23.7435, 114.6978),
            "香港": (22.3193, 114.1694),
            "呼和浩特": (40.8429, 111.7492),
            "南京": (32.0603, 118.7969),
            "青岛": (36.0671, 120.3826),
            "上海": (31.2304, 121.4737),
            "深圳": (22.3193, 114.1694),
            "武汉": (30.5928, 114.3055),
            "乌兰察布": (41.0173, 113.1145),
            "张家口": (40.7686, 114.8867),
            "雅加达": (-6.2088, 106.8456),
            "新加坡": (1.3521, 103.8198),
            "东京": (35.6762, 139.6503),
            "利雅得": (24.7136, 46.6753),
            "曼谷": (13.7563, 100.5018),
            "马尼拉": (14.5995, 120.9842),
            "迪拜": (25.2048, 55.2708),
            "首尔": (37.5665, 126.978),
            "吉隆坡": (3.139, 101.6869),
            "法兰克福": (50.1109, 8.6821),
            "伦敦": (51.5074, -0.1278),
            "克雷塔罗": (20.5888, -100.3899),
            "弗吉尼亚": (37.4316, -78.6569),
            "硅谷": (37.7749, -122.4194),
        }
        
        if city in backup_coordinates:
            print(f"  ℹ 使用备用坐标: {city}")
            return backup_coordinates[city]
        
        # 如果城市名不匹配，尝试模糊匹配
        for key, coords in backup_coordinates.items():
            if key in city or city in key:
                print(f"  ℹ 使用备用坐标（模糊匹配）: {city} -> {key}")
                return coords
        
        # 默认返回北京的坐标
        print(f"  ⚠ 未找到 {city} 的坐标，使用默认坐标（北京）")
        return (39.9042, 116.4074)
    
    def generate_node_id(self, name: str, country: str) -> str:
        """生成节点ID"""
        # 如果已经在映射表中，直接返回
        if name in self.region_id_mapping:
            return self.region_id_mapping[name]
        
        # 中国区域
        if country == "中国":
            city_match = re.search(r'（([^）]+)）', name)
            if city_match:
                city = city_match.group(1).split('-')[0].split('（')[0]
                # 转换为拼音简写（简化处理）
                city_map = {
                    "北京": "beijing",
                    "上海": "shanghai",
                    "杭州": "hangzhou",
                    "深圳": "shenzhen",
                    "青岛": "qingdao",
                    "成都": "chengdu",
                    "广州": "guangzhou",
                    "武汉": "wuhan",
                    "南京": "nanjing",
                    "福州": "fuzhou",
                }
                city_en = city_map.get(city, city.lower())
                return f"cn-{city_en}"
        
        # 国际区域
        # 简化处理，实际应该使用更准确的映射
        return name.lower().replace("（", "-").replace("）", "").replace(" ", "-")
    
    def generate_availability_zones(self, node_id: str, count: int) -> List[str]:
        """生成可用区列表"""
        zones = []
        for i in range(count):
            # 根据节点ID格式生成可用区ID
            if node_id.startswith("cn-"):
                # 中国区域格式: cn-beijing-a, cn-beijing-b, ...
                zone_id = f"{node_id}-{chr(97 + i)}"  # 97是'a'的ASCII码
            else:
                # 国际区域格式: ap-southeast-1a, ap-southeast-1b, ...
                zone_id = f"{node_id}{chr(97 + i)}"
            zones.append(zone_id)
        return zones
    
    def parse_html(self, html: str) -> List[Dict]:
        """解析HTML内容"""
        soup = BeautifulSoup(html, 'html.parser')
        regions = []
        
        # 方法1: 尝试从文本内容中提取
        text_content = soup.get_text()
        regions = self.parse_region_info(text_content)
        
        if regions:
            print(f"从页面文本中解析到 {len(regions)} 个区域")
            return regions
        
        # 方法2: 尝试查找特定的HTML结构
        # 查找包含区域信息的列表项或div
        region_elements = soup.find_all(['li', 'div'], string=re.compile(r'可用区：'))
        
        if region_elements:
            print(f"找到 {len(region_elements)} 个区域元素")
            # 进一步解析这些元素
        
        # 方法3: 尝试查找包含区域名称的元素
        # 查找包含城市名称的元素
        city_patterns = [
            r'新加坡', r'泰国', r'马来西亚', r'印度尼西亚', r'菲律宾',
            r'日本', r'韩国', r'美国', r'墨西哥', r'德国', r'英国',
            r'阿联酋', r'沙特', r'中国香港', r'华北', r'华东', r'华南',
            r'西南', r'华中'
        ]
        
        return regions
    
    def save_to_json(self, regions: List[Dict], output_path: Path):
        """保存数据到JSON文件"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "provider": "alibaba_cloud",
            "version": "1.0.6",
            "last_updated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "nodes": regions
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"数据已保存到: {output_path}")
        print(f"共爬取 {len(regions)} 个区域")
    
    def crawl(self, output_path: Optional[Path] = None):
        """执行爬取任务"""
        if output_path is None:
            output_path = Path(__file__).parent / "aliyun" / "nodes.json"
        
        # 获取页面
        html = self.fetch_page()
        if not html:
            print("无法获取页面内容")
            return
        
        # 解析数据
        print("正在解析页面数据...")
        regions = self.parse_html(html)
        
        if not regions:
            print("未能从页面解析到区域数据，使用备用数据...")
            print("提示: 如果页面结构发生变化，可能需要更新解析逻辑")
            # 如果解析失败，使用已知数据作为备用
            regions = self.get_fallback_data()
        else:
            print(f"成功从页面解析到 {len(regions)} 个区域")
        
        # 按node_id排序
        regions.sort(key=lambda x: x['node_id'])
        
        # 保存数据
        self.save_to_json(regions, output_path)
    
    def get_fallback_data(self) -> List[Dict]:
        """获取备用数据（基于已知信息）"""
        # 从网页内容中提取的已知数据
        known_regions = [
            {"name": "新加坡", "az_count": 3, "year": 2015, "city": "新加坡", "country": "新加坡"},
            {"name": "泰国（曼谷）", "az_count": 2, "year": 2022, "city": "曼谷", "country": "泰国"},
            {"name": "马来西亚（吉隆坡）", "az_count": 3, "year": 2017, "city": "吉隆坡", "country": "马来西亚"},
            {"name": "印度尼西亚（雅加达）", "az_count": 3, "year": 2018, "city": "雅加达", "country": "印度尼西亚"},
            {"name": "菲律宾（马尼拉）", "az_count": 2, "year": 2021, "city": "马尼拉", "country": "菲律宾"},
            {"name": "日本（东京）", "az_count": 3, "year": 2016, "city": "东京", "country": "日本"},
            {"name": "韩国（首尔）", "az_count": 2, "year": 2022, "city": "首尔", "country": "韩国"},
            {"name": "美国（弗吉尼亚）", "az_count": 2, "year": 2015, "city": "弗吉尼亚", "country": "美国"},
            {"name": "美国（硅谷）", "az_count": 2, "year": 2014, "city": "硅谷", "country": "美国"},
            {"name": "墨西哥（克雷塔罗）", "az_count": 1, "year": 2025, "city": "克雷塔罗", "country": "墨西哥"},
            {"name": "德国（法兰克福）", "az_count": 3, "year": 2016, "city": "法兰克福", "country": "德国"},
            {"name": "英国（伦敦）", "az_count": 2, "year": 2018, "city": "伦敦", "country": "英国"},
            {"name": "阿联酋（迪拜）", "az_count": 2, "year": 2016, "city": "迪拜", "country": "阿联酋"},
            {"name": "沙特（利雅得-合作伙伴运营）", "az_count": 2, "year": 2022, "city": "利雅得", "country": "沙特阿拉伯"},
            {"name": "中国香港", "az_count": 3, "year": 2014, "city": "香港", "country": "中国"},
            {"name": "华北1（青岛）", "az_count": 2, "year": 2012, "city": "青岛", "country": "中国"},
            {"name": "华北2（北京）", "az_count": 12, "year": 2013, "city": "北京", "country": "中国"},
            {"name": "华北3（张家口）", "az_count": 3, "year": 2014, "city": "张家口", "country": "中国"},
            {"name": "华北5（呼和浩特）", "az_count": 2, "year": 2017, "city": "呼和浩特", "country": "中国"},
            {"name": "华北6（乌兰察布）", "az_count": 3, "year": 2020, "city": "乌兰察布", "country": "中国"},
            {"name": "华东1（杭州）", "az_count": 8, "year": 2011, "city": "杭州", "country": "中国"},
            {"name": "华东2（上海）", "az_count": 12, "year": 2015, "city": "上海", "country": "中国"},
            {"name": "华东5（南京-本地地域）", "az_count": 1, "year": 2021, "city": "南京", "country": "中国"},
            {"name": "华东6（福州-本地地域）", "az_count": 1, "year": 2022, "city": "福州", "country": "中国"},
            {"name": "华南1（深圳）", "az_count": 6, "year": 2014, "city": "深圳", "country": "中国"},
            {"name": "华南2（河源）", "az_count": 2, "year": 2020, "city": "河源", "country": "中国"},
            {"name": "华南3（广州）", "az_count": 2, "year": 2020, "city": "广州", "country": "中国"},
            {"name": "西南1（成都）", "az_count": 2, "year": 2020, "city": "成都", "country": "中国"},
            {"name": "华中1（武汉-本地地域）", "az_count": 1, "year": 2023, "city": "武汉", "country": "中国"},
        ]
        
        regions = []
        for region_info in known_regions:
            city = region_info["city"]
            country = region_info["country"]
            name = region_info["name"]
            
            lat, lon = self.get_coordinates(city, country)
            if self.use_api:
                continent = self.get_continent_from_api(country) or "亚洲"
            else:
                continent = self._get_continent_fallback(country)
            node_id = self.region_id_mapping.get(name, self.generate_node_id(name, country))
            availability_zones = self.generate_availability_zones(node_id, region_info["az_count"])
            
            region = {
                "location": {
                    "country": country,
                    "city": city,
                    "latitude": lat,
                    "longitude": lon,
                    "continent": continent
                },
                "status": "active",
                "launch_date": f"{region_info['year']}-01-01T00:00:00",
                "node_id": node_id,
                "name": name,
                "availability_zones": availability_zones
            }
            
            if "关停中" in name:
                region["status"] = "deprecated"
            
            regions.append(region)
        
        return regions


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='阿里云全球基础设施爬虫')
    parser.add_argument(
        '--no-api',
        action='store_true',
        help='不使用API获取坐标和大洲信息（使用备用数据，速度更快）'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='输出文件路径（默认: web_crawler/aliyun/nodes.json）'
    )
    
    args = parser.parse_args()
    
    # 创建爬虫实例
    use_api = not args.no_api
    crawler = AliyunCrawler(use_api=use_api)
    
    # 设置输出路径
    if args.output:
        output_path = Path(args.output)
    else:
        script_dir = Path(__file__).parent
        output_path = script_dir / "aliyun" / "nodes.json"
    
    print("=" * 60)
    print("阿里云全球基础设施爬虫")
    print("=" * 60)
    if use_api:
        print("✓ 已启用API模式（将使用OpenStreetMap和REST Countries API）")
        print("  提示: 如需快速运行，可使用 --no-api 参数")
    else:
        print("✓ 已禁用API模式（将使用备用数据）")
    print("=" * 60)
    
    # 执行爬取
    crawler.crawl(output_path)
    
    print("\n爬取完成！")


if __name__ == "__main__":
    main()

