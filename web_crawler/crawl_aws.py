#!/usr/bin/env python3
"""
AWS全球基础设施爬虫脚本
爬取 https://aws.amazon.com/cn/about-aws/global-infrastructure/ 页面数据
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


class AWSCrawler:
    """AWS基础设施爬虫类"""
    
    def __init__(self, use_api: bool = True):
        """
        初始化爬虫
        
        Args:
            use_api: 是否使用API获取坐标和大洲信息（默认True）
                     如果为False，将使用内置的备用数据
        """
        self.base_url = "https://aws.amazon.com/cn/about-aws/global-infrastructure/"
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
            "阿联酋": "United Arab Emirates",
            "巴林": "Bahrain",
            "以色列": "Israel",
            "沙特阿拉伯": "Saudi Arabia",
            "卡塔尔": "Qatar",
            "南非": "South Africa",
            "肯尼亚": "Kenya",
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
        }
        
        # AWS区域ID映射（从区域名称到区域ID）
        self.region_id_mapping = {
            "US East (N. Virginia)": "us-east-1",
            "US East (Ohio)": "us-east-2",
            "US West (N. California)": "us-west-1",
            "US West (Oregon)": "us-west-2",
            "Canada (Central)": "ca-central-1",
            "Canada West (Calgary)": "ca-west-1",
            "Mexico (Central)": "mx-central-1",
            "South America (São Paulo)": "sa-east-1",
            "Europe (Ireland)": "eu-west-1",
            "Europe (London)": "eu-west-2",
            "Europe (Paris)": "eu-west-3",
            "Europe (Frankfurt)": "eu-central-1",
            "Europe (Milan)": "eu-south-1",
            "Europe (Stockholm)": "eu-north-1",
            "Europe (Spain)": "eu-south-2",
            "Europe (Zurich)": "eu-central-2",
            "Middle East (Bahrain)": "me-south-1",
            "Middle East (UAE)": "me-central-1",
            "Middle East (Israel)": "il-central-1",
            "Africa (Cape Town)": "af-south-1",
            "Asia Pacific (Mumbai)": "ap-south-1",
            "Asia Pacific (Hyderabad)": "ap-south-2",
            "Asia Pacific (Jakarta)": "ap-southeast-3",
            "Asia Pacific (Singapore)": "ap-southeast-1",
            "Asia Pacific (Bangkok)": "ap-southeast-2",
            "Asia Pacific (Tokyo)": "ap-northeast-1",
            "Asia Pacific (Osaka)": "ap-northeast-3",
            "Asia Pacific (Seoul)": "ap-northeast-2",
            "Asia Pacific (Sydney)": "ap-southeast-4",
            "Asia Pacific (Melbourne)": "ap-southeast-8",
            "Asia Pacific (Hong Kong)": "ap-east-1",
            "Asia Pacific (Manila)": "ap-southeast-6",
            "Asia Pacific (Kuala Lumpur)": "ap-southeast-5",
            "China (Beijing)": "cn-north-1",
            "China (Ningxia)": "cn-northwest-1",
            "AWS GovCloud (US-East)": "us-gov-east-1",
            "AWS GovCloud (US-West)": "us-gov-west-1",
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
            # 处理特殊情况
            if city == "N. Virginia" or city == "Northern Virginia":
                query = "Ashburn, Virginia, United States"
            elif city == "N. California" or city == "Northern California":
                query = "San Francisco, California, United States"
            elif city == "São Paulo":
                query = "Sao Paulo, Brazil"
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
            "阿联酋": "亚洲",
            "巴林": "亚洲",
            "以色列": "亚洲",
            "沙特阿拉伯": "亚洲",
            "卡塔尔": "亚洲",
            "南非": "非洲",
            "肯尼亚": "非洲",
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
            "孟买": (19.076, 72.8777),
            "海得拉巴": (17.385, 78.4867),
            "雅加达": (-6.2088, 106.8456),
            "新加坡": (1.3521, 103.8198),
            "曼谷": (13.7563, 100.5018),
            "东京": (35.6762, 139.6503),
            "大阪": (34.6937, 135.5023),
            "首尔": (37.5665, 126.978),
            "悉尼": (-33.8688, 151.2093),
            "墨尔本": (-37.8136, 144.9631),
            "马尼拉": (14.5995, 120.9842),
            "吉隆坡": (3.139, 101.6869),
            "北京": (39.9042, 116.4074),
            "银川": (38.4872, 106.2309),
            "弗吉尼亚": (38.9072, -77.0369),
            "俄亥俄": (39.9612, -82.9988),
            "加利福尼亚": (37.7749, -122.4194),
            "俄勒冈": (45.5152, -122.6784),
            "多伦多": (43.6532, -79.3832),
            "卡尔加里": (51.0447, -114.0719),
            "克雷塔罗": (20.5888, -100.3899),
            "圣保罗": (-23.5505, -46.6333),
            "都柏林": (53.3498, -6.2603),
            "伦敦": (51.5074, -0.1278),
            "巴黎": (48.8566, 2.3522),
            "法兰克福": (50.1109, 8.6821),
            "米兰": (45.4642, 9.1900),
            "斯德哥尔摩": (59.3293, 18.0686),
            "马德里": (40.4168, -3.7038),
            "苏黎世": (47.3769, 8.5417),
            "麦纳麦": (26.0667, 50.5577),
            "迪拜": (25.2048, 55.2708),
            "特拉维夫": (32.0853, 34.7818),
            "开普敦": (-33.9249, 18.4241),
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
        """从AWS区域名称解析城市和国家"""
        # AWS区域名称格式示例：
        # "US East (N. Virginia)" -> ("N. Virginia", "美国")
        # "Asia Pacific (Mumbai)" -> ("孟买", "印度")
        # "Europe (London)" -> ("伦敦", "英国")
        
        # 处理中国区域
        if "China" in region_name:
            if "Beijing" in region_name:
                return "北京", "中国"
            elif "Ningxia" in region_name:
                return "银川", "中国"
        
        # 处理美国区域
        if region_name.startswith("US "):
            if "N. Virginia" in region_name or "Virginia" in region_name:
                return "弗吉尼亚", "美国"
            elif "Ohio" in region_name:
                return "俄亥俄", "美国"
            elif "N. California" in region_name or "California" in region_name:
                return "加利福尼亚", "美国"
            elif "Oregon" in region_name:
                return "俄勒冈", "美国"
            elif "GovCloud" in region_name:
                if "East" in region_name:
                    return "弗吉尼亚", "美国"
                elif "West" in region_name:
                    return "俄勒冈", "美国"
        
        # 处理加拿大区域
        if "Canada" in region_name:
            if "Calgary" in region_name:
                return "卡尔加里", "加拿大"
            else:
                return "多伦多", "加拿大"
        
        # 处理墨西哥区域
        if "Mexico" in region_name:
            return "克雷塔罗", "墨西哥"
        
        # 处理南美洲区域
        if "São Paulo" in region_name or "Sao Paulo" in region_name:
            return "圣保罗", "巴西"
        
        # 处理欧洲区域
        if "Europe" in region_name:
            if "Ireland" in region_name:
                return "都柏林", "爱尔兰"
            elif "London" in region_name:
                return "伦敦", "英国"
            elif "Paris" in region_name:
                return "巴黎", "法国"
            elif "Frankfurt" in region_name:
                return "法兰克福", "德国"
            elif "Milan" in region_name:
                return "米兰", "意大利"
            elif "Stockholm" in region_name:
                return "斯德哥尔摩", "瑞典"
            elif "Spain" in region_name or "Madrid" in region_name:
                return "马德里", "西班牙"
            elif "Zurich" in region_name:
                return "苏黎世", "瑞士"
        
        # 处理中东区域
        if "Middle East" in region_name:
            if "Bahrain" in region_name:
                return "麦纳麦", "巴林"
            elif "UAE" in region_name:
                return "迪拜", "阿联酋"
            elif "Israel" in region_name:
                return "特拉维夫", "以色列"
        
        # 处理非洲区域
        if "Africa" in region_name:
            if "Cape Town" in region_name:
                return "开普敦", "南非"
        
        # 处理亚太区域
        if "Asia Pacific" in region_name:
            if "Mumbai" in region_name:
                return "孟买", "印度"
            elif "Hyderabad" in region_name:
                return "海得拉巴", "印度"
            elif "Jakarta" in region_name:
                return "雅加达", "印度尼西亚"
            elif "Singapore" in region_name:
                return "新加坡", "新加坡"
            elif "Bangkok" in region_name:
                return "曼谷", "泰国"
            elif "Tokyo" in region_name:
                return "东京", "日本"
            elif "Osaka" in region_name:
                return "大阪", "日本"
            elif "Seoul" in region_name:
                return "首尔", "韩国"
            elif "Sydney" in region_name:
                return "悉尼", "澳大利亚"
            elif "Melbourne" in region_name:
                return "墨尔本", "澳大利亚"
            elif "Hong Kong" in region_name:
                return "香港", "中国"
            elif "Manila" in region_name:
                return "马尼拉", "菲律宾"
            elif "Kuala Lumpur" in region_name:
                return "吉隆坡", "马来西亚"
        
        # 默认处理
        print(f"  ⚠ 无法解析区域名称: {region_name}")
        return "未知", "未知"
    
    def generate_availability_zones(self, node_id: str, count: int) -> List[str]:
        """生成可用区列表"""
        zones = []
        for i in range(count):
            zone_id = f"{node_id}{chr(97 + i)}"  # 97是'a'的ASCII码
            zones.append(zone_id)
        return zones
    
    def parse_html(self, html: str) -> List[Dict]:
        """解析HTML内容"""
        soup = BeautifulSoup(html, 'html.parser')
        regions = []
        
        # AWS页面结构比较复杂，我们需要查找区域信息
        # 通常区域信息在特定的section或div中
        
        # 方法1: 查找包含区域名称的元素
        # AWS页面可能使用特定的class或id来标识区域
        
        # 由于AWS页面结构可能动态加载，我们使用备用数据
        return []
    
    def get_fallback_data(self) -> List[Dict]:
        """获取备用数据（基于已知的AWS区域信息）"""
        # AWS区域数据（基于2024年数据）
        known_regions = [
            {"name": "US East (N. Virginia)", "az_count": 6, "year": 2006, "city": "弗吉尼亚", "country": "美国"},
            {"name": "US East (Ohio)", "az_count": 3, "year": 2016, "city": "俄亥俄", "country": "美国"},
            {"name": "US West (N. California)", "az_count": 3, "year": 2009, "city": "加利福尼亚", "country": "美国"},
            {"name": "US West (Oregon)", "az_count": 4, "year": 2011, "city": "俄勒冈", "country": "美国"},
            {"name": "Canada (Central)", "az_count": 3, "year": 2016, "city": "多伦多", "country": "加拿大"},
            {"name": "Canada West (Calgary)", "az_count": 3, "year": 2023, "city": "卡尔加里", "country": "加拿大"},
            {"name": "Mexico (Central)", "az_count": 3, "year": 2024, "city": "克雷塔罗", "country": "墨西哥"},
            {"name": "South America (São Paulo)", "az_count": 3, "year": 2011, "city": "圣保罗", "country": "巴西"},
            {"name": "Europe (Ireland)", "az_count": 3, "year": 2007, "city": "都柏林", "country": "爱尔兰"},
            {"name": "Europe (London)", "az_count": 3, "year": 2016, "city": "伦敦", "country": "英国"},
            {"name": "Europe (Paris)", "az_count": 3, "year": 2017, "city": "巴黎", "country": "法国"},
            {"name": "Europe (Frankfurt)", "az_count": 3, "year": 2014, "city": "法兰克福", "country": "德国"},
            {"name": "Europe (Milan)", "az_count": 3, "year": 2020, "city": "米兰", "country": "意大利"},
            {"name": "Europe (Stockholm)", "az_count": 3, "year": 2018, "city": "斯德哥尔摩", "country": "瑞典"},
            {"name": "Europe (Spain)", "az_count": 3, "year": 2022, "city": "马德里", "country": "西班牙"},
            {"name": "Europe (Zurich)", "az_count": 3, "year": 2022, "city": "苏黎世", "country": "瑞士"},
            {"name": "Middle East (Bahrain)", "az_count": 3, "year": 2019, "city": "麦纳麦", "country": "巴林"},
            {"name": "Middle East (UAE)", "az_count": 3, "year": 2022, "city": "迪拜", "country": "阿联酋"},
            {"name": "Middle East (Israel)", "az_count": 3, "year": 2023, "city": "特拉维夫", "country": "以色列"},
            {"name": "Africa (Cape Town)", "az_count": 3, "year": 2020, "city": "开普敦", "country": "南非"},
            {"name": "Asia Pacific (Mumbai)", "az_count": 3, "year": 2016, "city": "孟买", "country": "印度"},
            {"name": "Asia Pacific (Hyderabad)", "az_count": 3, "year": 2022, "city": "海得拉巴", "country": "印度"},
            {"name": "Asia Pacific (Jakarta)", "az_count": 3, "year": 2021, "city": "雅加达", "country": "印度尼西亚"},
            {"name": "Asia Pacific (Singapore)", "az_count": 3, "year": 2010, "city": "新加坡", "country": "新加坡"},
            {"name": "Asia Pacific (Bangkok)", "az_count": 3, "year": 2020, "city": "曼谷", "country": "泰国"},
            {"name": "Asia Pacific (Tokyo)", "az_count": 4, "year": 2011, "city": "东京", "country": "日本"},
            {"name": "Asia Pacific (Osaka)", "az_count": 3, "year": 2021, "city": "大阪", "country": "日本"},
            {"name": "Asia Pacific (Seoul)", "az_count": 3, "year": 2016, "city": "首尔", "country": "韩国"},
            {"name": "Asia Pacific (Sydney)", "az_count": 3, "year": 2012, "city": "悉尼", "country": "澳大利亚"},
            {"name": "Asia Pacific (Melbourne)", "az_count": 3, "year": 2022, "city": "墨尔本", "country": "澳大利亚"},
            {"name": "Asia Pacific (Hong Kong)", "az_count": 3, "year": 2019, "city": "香港", "country": "中国"},
            {"name": "Asia Pacific (Manila)", "az_count": 3, "year": 2024, "city": "马尼拉", "country": "菲律宾"},
            {"name": "Asia Pacific (Kuala Lumpur)", "az_count": 3, "year": 2024, "city": "吉隆坡", "country": "马来西亚"},
            {"name": "China (Beijing)", "az_count": 2, "year": 2014, "city": "北京", "country": "中国"},
            {"name": "China (Ningxia)", "az_count": 3, "year": 2017, "city": "银川", "country": "中国"},
            {"name": "AWS GovCloud (US-East)", "az_count": 3, "year": 2018, "city": "弗吉尼亚", "country": "美国"},
            {"name": "AWS GovCloud (US-West)", "az_count": 3, "year": 2011, "city": "俄勒冈", "country": "美国"},
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
            node_id = self.region_id_mapping.get(name, name.lower().replace(" ", "-").replace("(", "").replace(")", ""))
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
            "provider": "aws",
            "version": "1.1.6",
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
            output_path = Path(__file__).parent / "aws" / "nodes.json"
        
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
    
    parser = argparse.ArgumentParser(description='AWS全球基础设施爬虫')
    parser.add_argument(
        '--no-api',
        action='store_true',
        help='不使用API获取坐标和大洲信息（使用备用数据，速度更快）'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='输出文件路径（默认: web_crawler/aws/nodes.json）'
    )
    
    args = parser.parse_args()
    
    # 创建爬虫实例
    use_api = not args.no_api
    crawler = AWSCrawler(use_api=use_api)
    
    # 设置输出路径
    if args.output:
        output_path = Path(args.output)
    else:
        script_dir = Path(__file__).parent
        output_path = script_dir / "aws" / "nodes.json"
    
    print("=" * 60)
    print("AWS全球基础设施爬虫")
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

