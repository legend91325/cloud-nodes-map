#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
地图数据更新脚本
从JSON文件中读取最新的云服务提供商节点数据并更新地图
"""

import json
import os
from pathlib import Path
from datetime import datetime

def load_json_data(file_path):
    """加载JSON数据文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ 文件不存在: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误 {file_path}: {e}")
        return None

def extract_region_data(data, provider_name):
    """从JSON数据中提取区域信息"""
    regions = []
    
    if not data or 'regions' not in data:
        print(f"⚠️  {provider_name} 数据格式不正确")
        return regions
    
    for region in data['regions']:
        region_info = {
            'id': region.get('region_id', ''),
            'name': region.get('region_name', ''),
            'status': region.get('status', region.get('region_state', '')),
            'fetch_time': region.get('fetch_time', '')
        }
        
        # 根据区域名称推断经纬度
        lat, lng = get_coordinates_by_name(region_info['name'])
        region_info['lat'] = lat
        region_info['lng'] = lng
        
        regions.append(region_info)
    
    return regions

def get_coordinates_by_name(region_name):
    """根据区域名称获取经纬度坐标"""
    # 中国地区
    if '北京' in region_name:
        return 39.9042, 116.4074
    elif '上海' in region_name:
        return 31.2304, 121.4737
    elif '广州' in region_name:
        return 23.1291, 113.2644
    elif '深圳' in region_name:
        return 22.5431, 114.0579
    elif '杭州' in region_name:
        return 30.2741, 120.1551
    elif '南京' in region_name:
        return 32.0603, 118.7969
    elif '成都' in region_name:
        return 30.5728, 104.0668
    elif '重庆' in region_name:
        return 29.4316, 106.9123
    elif '青岛' in region_name:
        return 36.0671, 120.3826
    elif '张家口' in region_name:
        return 40.7686, 114.8867
    elif '呼和浩特' in region_name:
        return 40.8429, 111.7494
    elif '乌兰察布' in region_name:
        return 41.0173, 113.1145
    elif '河源' in region_name:
        return 23.7435, 114.6978
    elif '福州' in region_name:
        return 26.0745, 119.2965
    elif '武汉' in region_name:
        return 30.5928, 114.3055
    elif '贵阳' in region_name:
        return 26.6470, 106.6302
    elif '香港' in region_name:
        return 22.3193, 114.1694
    
    # 亚太地区
    elif '东京' in region_name or '日本' in region_name:
        return 35.6762, 139.6503
    elif '首尔' in region_name or '韩国' in region_name:
        return 37.5665, 126.9780
    elif '新加坡' in region_name:
        return 1.3521, 103.8198
    elif '曼谷' in region_name or '泰国' in region_name:
        return 13.7563, 100.5018
    elif '雅加达' in region_name or '印度尼西亚' in region_name:
        return -6.2088, 106.8456
    elif '吉隆坡' in region_name or '马来西亚' in region_name:
        return 3.1390, 101.6869
    elif '马尼拉' in region_name or '菲律宾' in region_name:
        return 14.5995, 120.9842
    elif '大阪' in region_name:
        return 34.6937, 135.5023
    elif '孟买' in region_name or '印度' in region_name:
        return 19.0760, 72.8777
    
    # 美洲地区
    elif '硅谷' in region_name or '美国西部' in region_name:
        return 37.3382, -121.8863
    elif '弗吉尼亚' in region_name or '美国东部' in region_name:
        return 37.4316, -78.6569
    elif '墨西哥' in region_name:
        return 19.4326, -99.1332
    elif '圣保罗' in region_name or '巴西' in region_name:
        return -23.5505, -46.6333
    
    # 欧洲地区
    elif '法兰克福' in region_name or '德国' in region_name:
        return 50.1109, 8.6821
    elif '伦敦' in region_name or '英国' in region_name:
        return 51.5074, -0.1278
    elif '巴黎' in region_name or '法国' in region_name:
        return 48.8566, 2.3522
    elif '斯德哥尔摩' in region_name or '瑞典' in region_name:
        return 59.3293, 18.0686
    
    # 其他地区
    elif '迪拜' in region_name or '阿联酋' in region_name:
        return 25.2048, 55.2708
    elif '约翰内斯堡' in region_name or '南非' in region_name:
        return -26.2041, 28.0473
    
    # 默认坐标（中国中心）
    else:
        print(f"⚠️  未找到区域坐标: {region_name}")
        return 35.8617, 104.1954

def generate_js_data(aliyun_data, huawei_data, tencent_data):
    """生成JavaScript数据对象"""
    js_code = f"""// 云服务提供商节点数据 - 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
const cloudData = {{
    aliyun: {{
        regions: {json.dumps(aliyun_data, ensure_ascii=False, indent=8)}
    }},
    huawei: {{
        regions: {json.dumps(huawei_data, ensure_ascii=False, indent=8)}
    }},
    tencent: {{
        regions: {json.dumps(tencent_data, ensure_ascii=False, indent=8)}
    }}
}};"""
    
    return js_code

def update_html_file(js_data):
    """更新HTML文件中的JavaScript数据"""
    html_file = Path("cloud_nodes_map.html")
    
    if not html_file.exists():
        print("❌ cloud_nodes_map.html 文件不存在")
        return False
    
    # 读取HTML文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找并替换JavaScript数据
    start_marker = "// 云服务提供商节点数据"
    end_marker = "};"
    
    start_pos = content.find(start_marker)
    if start_pos == -1:
        print("❌ 在HTML文件中未找到数据标记")
        return False
    
    end_pos = content.find(end_marker, start_pos) + len(end_marker)
    
    # 替换数据
    new_content = content[:start_pos] + js_data + content[end_pos:]
    
    # 写回文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    """主函数"""
    print("🔄 开始更新地图数据...")
    print("=" * 50)
    
    # 文件路径
    output_dir = Path("output")
    aliyun_file = output_dir / "aliyun_nodes_complete.json"
    huawei_file = output_dir / "huaweicloud_nodes_complete.json"
    tencent_file = output_dir / "tencentcloud_nodes_complete.json"
    
    # 加载数据
    print("📂 加载JSON数据文件...")
    aliyun_data = load_json_data(aliyun_file)
    huawei_data = load_json_data(huawei_file)
    tencent_data = load_json_data(tencent_file)
    
    if not all([aliyun_data, huawei_data, tencent_data]):
        print("❌ 部分数据文件加载失败")
        return
    
    # 提取区域数据
    print("🔍 提取区域信息...")
    aliyun_regions = extract_region_data(aliyun_data, "阿里云")
    huawei_regions = extract_region_data(huawei_data, "华为云")
    tencent_regions = extract_region_data(tencent_data, "腾讯云")
    
    print(f"✅ 阿里云: {len(aliyun_regions)} 个区域")
    print(f"✅ 华为云: {len(huawei_regions)} 个区域")
    print(f"✅ 腾讯云: {len(tencent_regions)} 个区域")
    
    # 生成JavaScript数据
    print("📝 生成JavaScript数据...")
    js_data = generate_js_data(aliyun_regions, huawei_regions, tencent_regions)
    
    # 更新HTML文件
    print("💾 更新HTML文件...")
    if update_html_file(js_data):
        print("✅ 地图数据更新成功！")
        print("🌐 请刷新浏览器页面查看最新数据")
    else:
        print("❌ 地图数据更新失败")

if __name__ == "__main__":
    main() 