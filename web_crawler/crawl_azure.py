#!/usr/bin/env python3
"""
Azure全球基础设施爬虫脚本
爬取 https://datacenters.microsoft.com/globe/explore?view=table 页面数据
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


class AzureCrawler:
    """Azure基础设施爬虫类"""
    
    def __init__(self, use_api: bool = True):
        """
        初始化爬虫
        
        Args:
            use_api: 是否使用API获取坐标和大洲信息（默认True）
                     如果为False，将使用内置的备用数据
        """
        self.base_url = "https://datacenters.microsoft.com/globe/explore?view=table"
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
            "美国": "United States",
            "加拿大": "Canada",
            "墨西哥": "Mexico",
            "巴西": "Brazil",
            "智利": "Chile",
            "阿根廷": "Argentina",
            "英国": "United Kingdom",
            "爱尔兰": "Ireland",
            "法国": "France",
            "德国": "Germany",
            "意大利": "Italy",
            "西班牙": "Spain",
            "瑞典": "Sweden",
            "瑞士": "Switzerland",
            "荷兰": "Netherlands",
            "比利时": "Belgium",
            "波兰": "Poland",
            "挪威": "Norway",
            "芬兰": "Finland",
            "丹麦": "Denmark",
            "奥地利": "Austria",
            "阿联酋": "United Arab Emirates",
            "巴林": "Bahrain",
            "以色列": "Israel",
            "沙特阿拉伯": "Saudi Arabia",
            "卡塔尔": "Qatar",
            "南非": "South Africa",
            "肯尼亚": "Kenya",
            "埃及": "Egypt",
            "印度": "India",
            "印度尼西亚": "Indonesia",
            "新加坡": "Singapore",
            "日本": "Japan",
            "韩国": "South Korea",
            "泰国": "Thailand",
            "马来西亚": "Malaysia",
            "菲律宾": "Philippines",
            "越南": "Vietnam",
            "澳大利亚": "Australia",
            "新西兰": "New Zealand",
            "台湾": "Taiwan",
        }
        
        # Azure区域名称到区域ID的映射
        self.region_name_to_id = {
            "East Asia": "eastasia",
            "Southeast Asia": "southeastasia",
            "Central India": "centralindia",
            "South India": "southindia",
            "West India": "westindia",
            "Japan East": "japaneast",
            "Japan West": "japanwest",
            "Korea Central": "koreacentral",
            "Korea South": "koreasouth",
            "Australia East": "australiaeast",
            "Australia Southeast": "australiasoutheast",
            "Australia Central": "australiacentral",
            "Australia Central 2": "australiacentral2",
            "East US": "eastus",
            "East US 2": "eastus2",
            "East US 3": "eastus3",
            "West US": "westus",
            "West US 2": "westus2",
            "West US 3": "westus3",
            "Central US": "centralus",
            "North Central US": "northcentralus",
            "South Central US": "southcentralus",
            "West Central US": "westcentralus",
            "Canada Central": "canadacentral",
            "Canada East": "canadaeast",
            "UK South": "uksouth",
            "UK West": "ukwest",
            "West Europe": "westeurope",
            "North Europe": "northeurope",
            "France Central": "francecentral",
            "France South": "francesouth",
            "Germany West Central": "germanywestcentral",
            "Germany North": "germanynorth",
            "Switzerland North": "switzerlandnorth",
            "Switzerland West": "switzerlandwest",
            "Italy North": "italynorth",
            "Norway East": "norwayeast",
            "Norway West": "norwaywest",
            "Sweden Central": "swedencentral",
            "Poland Central": "polandcentral",
            "UAE North": "uaenorth",
            "UAE Central": "uaecentral",
            "Qatar Central": "qatarcentral",
            "South Africa North": "southafricanorth",
            "South Africa West": "southafricawest",
            "Brazil South": "brazilsouth",
            "Brazil Southeast": "brazilsoutheast",
            "Chile Central": "chilecentral",
            "Mexico Central": "mexicocentral",
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
    
    def get_coordinates_from_api(self, city: str, country: str) -> Optional[Tuple[float, float]]:
        """使用Nominatim API获取城市坐标"""
        cache_key = f"{city},{country}"
        if cache_key in self.coordinates_cache:
            return self.coordinates_cache[cache_key]
        
        try:
            # 构建查询字符串
            if country == "中国":
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
            "美国": "北美洲",
            "加拿大": "北美洲",
            "墨西哥": "北美洲",
            "巴西": "南美洲",
            "智利": "南美洲",
            "阿根廷": "南美洲",
            "英国": "欧洲",
            "爱尔兰": "欧洲",
            "法国": "欧洲",
            "德国": "欧洲",
            "意大利": "欧洲",
            "西班牙": "欧洲",
            "瑞典": "欧洲",
            "瑞士": "欧洲",
            "荷兰": "欧洲",
            "比利时": "欧洲",
            "波兰": "欧洲",
            "挪威": "欧洲",
            "芬兰": "欧洲",
            "丹麦": "欧洲",
            "奥地利": "欧洲",
            "阿联酋": "亚洲",
            "巴林": "亚洲",
            "以色列": "亚洲",
            "沙特阿拉伯": "亚洲",
            "卡塔尔": "亚洲",
            "南非": "非洲",
            "肯尼亚": "非洲",
            "埃及": "非洲",
            "印度": "亚洲",
            "印度尼西亚": "亚洲",
            "新加坡": "亚洲",
            "日本": "亚洲",
            "韩国": "亚洲",
            "泰国": "亚洲",
            "马来西亚": "亚洲",
            "菲律宾": "亚洲",
            "越南": "亚洲",
            "澳大利亚": "大洋洲",
            "新西兰": "大洋洲",
            "台湾": "亚洲",
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
            "香港": (22.3193, 114.1694),
            "新加坡": (1.3521, 103.8198),
            "浦那": (18.5204, 73.8567),
            "金奈": (13.0827, 80.2707),
            "孟买": (19.076, 72.8777),
            "东京": (35.6762, 139.6503),
            "大阪": (34.6937, 135.5023),
            "首尔": (37.5665, 126.978),
            "釜山": (35.1796, 129.0756),
            "悉尼": (-33.8688, 151.2093),
            "墨尔本": (-37.8136, 144.9631),
            "堪培拉": (-35.2809, 149.1300),
            "弗吉尼亚": (38.9072, -77.0369),
            "爱荷华": (41.5908, -93.6208),
            "伊利诺伊": (41.8781, -87.6298),
            "德克萨斯": (29.7604, -95.3698),
            "加利福尼亚": (37.7749, -122.4194),
            "华盛顿": (47.6062, -122.3321),
            "亚利桑那": (33.4484, -112.0740),
            "怀俄明": (41.1403, -104.8197),
            "多伦多": (43.6532, -79.3832),
            "魁北克": (46.8139, -71.2080),
            "伦敦": (51.5074, -0.1278),
            "卡迪夫": (51.4816, -3.1791),
            "阿姆斯特丹": (52.3676, 4.9041),
            "巴黎": (48.8566, 2.3522),
            "马赛": (43.2965, 5.3698),
            "法兰克福": (50.1109, 8.6821),
            "柏林": (52.5200, 13.4050),
            "苏黎世": (47.3769, 8.5417),
            "日内瓦": (46.2044, 6.1432),
            "米兰": (45.4642, 9.1900),
            "奥斯陆": (59.9139, 10.7522),
            "斯塔万格": (58.9700, 5.7331),
            "斯德哥尔摩": (59.3293, 18.0686),
            "华沙": (52.2297, 21.0122),
            "迪拜": (25.2048, 55.2708),
            "多哈": (25.2854, 51.5310),
            "约翰内斯堡": (-26.2041, 28.0473),
            "开普敦": (-33.9249, 18.4241),
            "圣保罗": (-23.5505, -46.6333),
            "里约热内卢": (-22.9068, -43.1729),
            "圣地亚哥": (-33.4489, -70.6693),
            "墨西哥城": (19.4326, -99.1332),
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
    
    def parse_region_name(self, region_name: str) -> tuple:
        """从Azure区域名称解析城市和国家"""
        # Azure区域名称格式示例：
        # "East Asia" -> ("香港", "中国")
        # "Southeast Asia" -> ("新加坡", "新加坡")
        # "Central India" -> ("浦那", "印度")
        
        # 处理亚太区域
        if "East Asia" in region_name:
            return "香港", "中国"
        elif "Southeast Asia" in region_name:
            return "新加坡", "新加坡"
        elif "Central India" in region_name:
            return "浦那", "印度"
        elif "South India" in region_name:
            return "金奈", "印度"
        elif "West India" in region_name:
            return "孟买", "印度"
        elif "Japan East" in region_name:
            return "东京", "日本"
        elif "Japan West" in region_name:
            return "大阪", "日本"
        elif "Korea Central" in region_name:
            return "首尔", "韩国"
        elif "Korea South" in region_name:
            return "釜山", "韩国"
        elif "Australia East" in region_name:
            return "悉尼", "澳大利亚"
        elif "Australia Southeast" in region_name:
            return "墨尔本", "澳大利亚"
        elif "Australia Central" in region_name or "Australia Central 2" in region_name:
            return "堪培拉", "澳大利亚"
        
        # 处理美国区域
        elif "East US" in region_name:
            return "弗吉尼亚", "美国"
        elif "West US" in region_name:
            return "加利福尼亚", "美国"
        elif "Central US" in region_name:
            return "爱荷华", "美国"
        elif "North Central US" in region_name:
            return "伊利诺伊", "美国"
        elif "South Central US" in region_name:
            return "德克萨斯", "美国"
        elif "West Central US" in region_name:
            return "怀俄明", "美国"
        
        # 处理加拿大区域
        elif "Canada Central" in region_name:
            return "多伦多", "加拿大"
        elif "Canada East" in region_name:
            return "魁北克", "加拿大"
        
        # 处理欧洲区域
        elif "UK South" in region_name:
            return "伦敦", "英国"
        elif "UK West" in region_name:
            return "卡迪夫", "英国"
        elif "West Europe" in region_name:
            return "阿姆斯特丹", "荷兰"
        elif "North Europe" in region_name:
            return "都柏林", "爱尔兰"
        elif "France Central" in region_name:
            return "巴黎", "法国"
        elif "France South" in region_name:
            return "马赛", "法国"
        elif "Germany West Central" in region_name:
            return "法兰克福", "德国"
        elif "Germany North" in region_name:
            return "柏林", "德国"
        elif "Switzerland North" in region_name:
            return "苏黎世", "瑞士"
        elif "Switzerland West" in region_name:
            return "日内瓦", "瑞士"
        elif "Italy North" in region_name:
            return "米兰", "意大利"
        elif "Norway East" in region_name:
            return "奥斯陆", "挪威"
        elif "Norway West" in region_name:
            return "斯塔万格", "挪威"
        elif "Sweden Central" in region_name:
            return "斯德哥尔摩", "瑞典"
        elif "Poland Central" in region_name:
            return "华沙", "波兰"
        
        # 处理中东区域
        elif "UAE North" in region_name or "UAE Central" in region_name:
            return "迪拜", "阿联酋"
        elif "Qatar Central" in region_name:
            return "多哈", "卡塔尔"
        
        # 处理非洲区域
        elif "South Africa North" in region_name:
            return "约翰内斯堡", "南非"
        elif "South Africa West" in region_name:
            return "开普敦", "南非"
        
        # 处理南美洲区域
        elif "Brazil South" in region_name:
            return "圣保罗", "巴西"
        elif "Brazil Southeast" in region_name:
            return "里约热内卢", "巴西"
        elif "Chile Central" in region_name:
            return "圣地亚哥", "智利"
        
        # 处理墨西哥区域
        elif "Mexico Central" in region_name:
            return "墨西哥城", "墨西哥"
        
        # 默认处理
        print(f"  ⚠ 无法解析区域名称: {region_name}")
        return "未知", "未知"
    
    def generate_availability_zones(self, node_id: str, count: int) -> List[str]:
        """生成可用区列表"""
        zones = []
        for i in range(count):
            zone_id = f"{node_id}-{i + 1}"
            zones.append(zone_id)
        return zones
    
    def parse_html(self, html: str) -> List[Dict]:
        """解析HTML内容"""
        soup = BeautifulSoup(html, 'html.parser')
        regions = []
        
        # Azure页面可能使用表格或JavaScript动态加载数据
        # 尝试查找表格数据
        tables = soup.find_all('table')
        
        if tables:
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # 跳过表头
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        region_name = cells[0].get_text(strip=True)
                        location = cells[1].get_text(strip=True)
                        
                        if region_name and location:
                            # 解析区域信息
                            city, country = self.parse_region_name(region_name)
                            if city != "未知":
                                # 获取可用区数量（如果有）
                                az_count = 1
                                if len(cells) >= 5:
                                    az_text = cells[4].get_text(strip=True)
                                    az_match = re.search(r'(\d+)', az_text)
                                    if az_match:
                                        az_count = int(az_match.group(1))
                                
                                # 获取年份（如果有）
                                year = 2010
                                if len(cells) >= 4:
                                    year_text = cells[3].get_text(strip=True)
                                    year_match = re.search(r'(\d{4})', year_text)
                                    if year_match:
                                        year = int(year_match.group(1))
                                
                                node_id = self.region_name_to_id.get(region_name, region_name.lower().replace(" ", ""))
                                
                                region = {
                                    "location": {
                                        "country": country,
                                        "city": city,
                                        "latitude": 0.0,
                                        "longitude": 0.0,
                                        "continent": "亚洲"
                                    },
                                    "status": "active",
                                    "launch_date": f"{year}-01-01T00:00:00",
                                    "node_id": node_id,
                                    "name": region_name,
                                    "availability_zones": self.generate_availability_zones(node_id, az_count)
                                }
                                
                                regions.append(region)
        
        return regions
    
    def get_fallback_data(self) -> List[Dict]:
        """获取备用数据（基于已知的Azure区域信息）"""
        # Azure区域数据（基于2024年数据）
        known_regions = [
            {"name": "East Asia", "az_count": 1, "year": 2010, "city": "香港", "country": "中国"},
            {"name": "Southeast Asia", "az_count": 1, "year": 2010, "city": "新加坡", "country": "新加坡"},
            {"name": "Central India", "az_count": 1, "year": 2015, "city": "浦那", "country": "印度"},
            {"name": "South India", "az_count": 1, "year": 2015, "city": "金奈", "country": "印度"},
            {"name": "West India", "az_count": 1, "year": 2015, "city": "孟买", "country": "印度"},
            {"name": "Japan East", "az_count": 1, "year": 2014, "city": "东京", "country": "日本"},
            {"name": "Japan West", "az_count": 1, "year": 2015, "city": "大阪", "country": "日本"},
            {"name": "Korea Central", "az_count": 1, "year": 2015, "city": "首尔", "country": "韩国"},
            {"name": "Korea South", "az_count": 1, "year": 2023, "city": "釜山", "country": "韩国"},
            {"name": "Australia East", "az_count": 1, "year": 2014, "city": "悉尼", "country": "澳大利亚"},
            {"name": "Australia Southeast", "az_count": 1, "year": 2014, "city": "墨尔本", "country": "澳大利亚"},
            {"name": "Australia Central", "az_count": 1, "year": 2018, "city": "堪培拉", "country": "澳大利亚"},
            {"name": "Australia Central 2", "az_count": 1, "year": 2021, "city": "堪培拉", "country": "澳大利亚"},
            {"name": "East US", "az_count": 1, "year": 2011, "city": "弗吉尼亚", "country": "美国"},
            {"name": "East US 2", "az_count": 1, "year": 2012, "city": "弗吉尼亚", "country": "美国"},
            {"name": "East US 3", "az_count": 1, "year": 2019, "city": "弗吉尼亚", "country": "美国"},
            {"name": "West US", "az_count": 1, "year": 2014, "city": "加利福尼亚", "country": "美国"},
            {"name": "West US 2", "az_count": 1, "year": 2016, "city": "华盛顿", "country": "美国"},
            {"name": "West US 3", "az_count": 1, "year": 2021, "city": "亚利桑那", "country": "美国"},
            {"name": "Central US", "az_count": 1, "year": 2011, "city": "爱荷华", "country": "美国"},
            {"name": "North Central US", "az_count": 1, "year": 2011, "city": "伊利诺伊", "country": "美国"},
            {"name": "South Central US", "az_count": 1, "year": 2011, "city": "德克萨斯", "country": "美国"},
            {"name": "West Central US", "az_count": 1, "year": 2019, "city": "怀俄明", "country": "美国"},
            {"name": "Canada Central", "az_count": 1, "year": 2016, "city": "多伦多", "country": "加拿大"},
            {"name": "Canada East", "az_count": 1, "year": 2016, "city": "魁北克", "country": "加拿大"},
            {"name": "UK South", "az_count": 1, "year": 2016, "city": "伦敦", "country": "英国"},
            {"name": "UK West", "az_count": 1, "year": 2017, "city": "卡迪夫", "country": "英国"},
            {"name": "West Europe", "az_count": 1, "year": 2010, "city": "阿姆斯特丹", "country": "荷兰"},
            {"name": "North Europe", "az_count": 1, "year": 2010, "city": "都柏林", "country": "爱尔兰"},
            {"name": "France Central", "az_count": 1, "year": 2014, "city": "巴黎", "country": "法国"},
            {"name": "France South", "az_count": 1, "year": 2017, "city": "马赛", "country": "法国"},
            {"name": "Germany West Central", "az_count": 1, "year": 2019, "city": "法兰克福", "country": "德国"},
            {"name": "Germany North", "az_count": 1, "year": 2021, "city": "柏林", "country": "德国"},
            {"name": "Switzerland North", "az_count": 1, "year": 2019, "city": "苏黎世", "country": "瑞士"},
            {"name": "Switzerland West", "az_count": 1, "year": 2021, "city": "日内瓦", "country": "瑞士"},
            {"name": "Italy North", "az_count": 1, "year": 2020, "city": "米兰", "country": "意大利"},
            {"name": "Norway East", "az_count": 1, "year": 2019, "city": "奥斯陆", "country": "挪威"},
            {"name": "Norway West", "az_count": 1, "year": 2021, "city": "斯塔万格", "country": "挪威"},
            {"name": "Sweden Central", "az_count": 1, "year": 2021, "city": "斯德哥尔摩", "country": "瑞典"},
            {"name": "Poland Central", "az_count": 1, "year": 2021, "city": "华沙", "country": "波兰"},
            {"name": "UAE North", "az_count": 1, "year": 2019, "city": "迪拜", "country": "阿联酋"},
            {"name": "UAE Central", "az_count": 1, "year": 2022, "city": "迪拜", "country": "阿联酋"},
            {"name": "Qatar Central", "az_count": 1, "year": 2022, "city": "多哈", "country": "卡塔尔"},
            {"name": "South Africa North", "az_count": 1, "year": 2019, "city": "约翰内斯堡", "country": "南非"},
            {"name": "South Africa West", "az_count": 1, "year": 2021, "city": "开普敦", "country": "南非"},
            {"name": "Brazil South", "az_count": 1, "year": 2014, "city": "圣保罗", "country": "巴西"},
            {"name": "Brazil Southeast", "az_count": 1, "year": 2021, "city": "里约热内卢", "country": "巴西"},
            {"name": "Chile Central", "az_count": 1, "year": 2023, "city": "圣地亚哥", "country": "智利"},
            {"name": "Mexico Central", "az_count": 1, "year": 2023, "city": "墨西哥城", "country": "墨西哥"},
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
            node_id = self.region_name_to_id.get(name, name.lower().replace(" ", ""))
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
            
            regions.append(region)
        
        return regions
    
    def save_to_json(self, regions: List[Dict], output_path: Path):
        """保存数据到JSON文件"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "provider": "azure",
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
            output_path = Path(__file__).parent / "azure" / "nodes.json"
        
        # 获取页面
        html = self.fetch_page()
        if not html:
            print("无法获取页面内容，使用备用数据")
            regions = self.get_fallback_data()
        else:
            # 解析数据
            print("正在解析页面数据...")
            regions = self.parse_html(html)
            
            if not regions:
                print("未能从页面解析到区域数据，使用备用数据...")
                print("提示: 如果页面结构发生变化，可能需要更新解析逻辑")
                regions = self.get_fallback_data()
            else:
                print(f"成功从页面解析到 {len(regions)} 个区域")
        
        # 按node_id排序
        regions.sort(key=lambda x: x['node_id'])
        
        # 保存数据
        self.save_to_json(regions, output_path)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Azure全球基础设施爬虫')
    parser.add_argument(
        '--no-api',
        action='store_true',
        help='不使用API获取坐标和大洲信息（使用备用数据，速度更快）'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='输出文件路径（默认: web_crawler/azure/nodes.json）'
    )
    
    args = parser.parse_args()
    
    # 创建爬虫实例
    use_api = not args.no_api
    crawler = AzureCrawler(use_api=use_api)
    
    # 设置输出路径
    if args.output:
        output_path = Path(args.output)
    else:
        script_dir = Path(__file__).parent
        output_path = script_dir / "azure" / "nodes.json"
    
    print("=" * 60)
    print("Azure全球基础设施爬虫")
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

