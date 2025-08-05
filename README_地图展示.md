# 🌍 云服务提供商全球节点地图展示系统

## 概述

这是一个交互式的网页应用，用于展示阿里云、华为云、腾讯云三家云服务提供商的全球节点布局。通过平面地图的方式，直观地展示各家的数据中心分布情况。

## 功能特性

### 🗺️ 交互式地图
- **全球节点分布**: 在世界地图上显示各云服务提供商的数据中心位置
- **实时筛选**: 可以按云服务提供商筛选显示节点
- **悬停提示**: 鼠标悬停在节点上显示详细信息
- **响应式设计**: 支持不同屏幕尺寸的设备

### 📊 统计信息
- **区域统计**: 显示各家的可用区域数量
- **可用区统计**: 显示各家的可用区数量
- **区域列表**: 详细列出各家的所有区域名称

### 🎨 视觉设计
- **现代化UI**: 采用渐变背景和毛玻璃效果
- **色彩区分**: 不同云服务提供商使用不同颜色标识
- **动画效果**: 悬停和点击的平滑动画

## 数据来源

数据基于您提供的JSON文件：
- `output/aliyun_nodes_complete.json` - 阿里云节点数据
- `output/huaweicloud_nodes_complete.json` - 华为云节点数据  
- `output/tencentcloud_nodes_complete.json` - 腾讯云节点数据

## 使用方法

### 方法一：使用Python服务器（推荐）

1. **启动服务器**：
   ```bash
   python serve_map.py
   ```

2. **访问页面**：
   服务器会自动打开浏览器，或手动访问：
   ```
   http://localhost:8000/cloud_nodes_map.html
   ```

3. **停止服务器**：
   在终端中按 `Ctrl+C`

### 方法二：直接打开文件

直接在浏览器中打开 `cloud_nodes_map.html` 文件（某些功能可能受限）

### 方法三：使用其他HTTP服务器

```bash
# 使用Python内置服务器
python -m http.server 8000

# 使用Node.js的http-server
npx http-server -p 8000

# 使用PHP内置服务器
php -S localhost:8000
```

## 文件结构

```
cloud_singal_scripts/
├── cloud_nodes_map.html      # 主页面文件
├── serve_map.py              # HTTP服务器脚本
├── README_地图展示.md         # 本说明文档
└── output/                   # 数据文件目录
    ├── aliyun_nodes_complete.json
    ├── huaweicloud_nodes_complete.json
    └── tencentcloud_nodes_complete.json
```

## 技术实现

### 前端技术
- **HTML5**: 页面结构
- **CSS3**: 样式和动画效果
- **JavaScript**: 交互逻辑和数据处理

### 地图实现
- **自定义地图**: 使用CSS定位实现的世界地图
- **坐标转换**: 经纬度到屏幕坐标的转换
- **响应式布局**: 适配不同屏幕尺寸

### 数据可视化
- **节点标记**: 不同颜色的圆点表示数据中心
- **统计卡片**: 展示各家的数据统计
- **筛选功能**: 按云服务提供商筛选显示

## 自定义配置

### 修改端口
```bash
python serve_map.py 8080  # 使用8080端口
```

### 添加新的云服务提供商
1. 在 `cloudData` 对象中添加新的提供商数据
2. 在HTML中添加对应的统计卡片
3. 在CSS中添加对应的颜色样式

### 修改地图样式
- 修改 `.world-map` 的CSS样式来改变地图外观
- 调整 `.node` 的样式来改变节点外观
- 修改颜色变量来改变主题色彩

## 浏览器兼容性

- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 12+
- ✅ Edge 79+

## 故障排除

### 端口被占用
```bash
# 查看端口占用
lsof -i :8000

# 使用其他端口
python serve_map.py 8080
```

### 文件不存在
确保 `cloud_nodes_map.html` 文件在当前目录中

### 浏览器无法打开
手动访问 `http://localhost:8000/cloud_nodes_map.html`

## 更新日志

### v1.0.0 (2025-08-04)
- ✨ 初始版本发布
- 🌍 添加全球节点地图展示
- 📊 添加统计信息展示
- 🎨 添加现代化UI设计
- 🔧 添加HTTP服务器脚本

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 许可证

MIT License 