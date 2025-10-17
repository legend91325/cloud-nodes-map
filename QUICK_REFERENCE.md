# 快速参考指南

## 🚀 3步启动

```bash
# 1. 进入项目目录
cd cloud-nodes-map

# 2. 启动服务器
python3 serve.py

# 3. 打开浏览器访问
open http://localhost:8000/cloud-infrastructure-map.html
```

## 📊 供应商速查表

| 供应商 | ID | 节点数 | 国家 | 可用区 | 颜色 |
|--------|-----|--------|------|--------|------|
| Google Cloud | `google_cloud` | 36 | 24 | 36 | 🔵 #4285F4 |
| Azure | `azure` | 34 | 19 | 34 | 🔵 #0078D4 |
| 阿里云 | `alibaba_cloud` | 29 | 14 | 89 | 🟠 #FF6A00 |
| AWS | `aws` | 24 | 18 | 24 | 🟠 #FF9900 |
| 甲骨文云 | `oracle_cloud` | 21 | 15 | 21 | 🔴 #F80000 |
| 腾讯云 | `tencent_cloud` | 18 | 9 | 18 | 🔵 #006EFF |
| 华为云 | `huawei_cloud` | 16 | 10 | 16 | 🔴 #D0021B |
| IBM 云 | `ibm_cloud` | 11 | 7 | 11 | 🔵 #0F62FE |
| DigitalOcean | `digitalocean` | 10 | 8 | 10 | 🔵 #0080FF |
| OVH 云 | `ovh_cloud` | 9 | 7 | 9 | 🔵 #123F6D |

## 🗂️ 关键文件路径

```
主应用:           cloud-infrastructure-map.html
本地服务器:       serve.py
供应商配置:       data/providers-metadata.json
阿里云数据:       data/alibaba-cloud/nodes.json
AWS数据:          data/aws/nodes.json
Azure数据:        data/azure/nodes.json
Google Cloud:     data/google-cloud/nodes.json
华为云数据:       data/huawei-cloud/nodes.json
腾讯云数据:       data/tencent-cloud/nodes.json
Oracle Cloud:     data/oracle-cloud/nodes.json
IBM Cloud:        data/ibm-cloud/nodes.json
OVHcloud:         data/ovh-cloud/nodes.json
DigitalOcean:     data/digitalocean/nodes.json
```

## 🎨 HTML文件对比

| 文件 | 特点 | 推荐度 |
|------|------|--------|
| `cloud-infrastructure-map.html` | 完整功能，10供应商，统计+图表+地图+明细 | ⭐⭐⭐⭐⭐ |
| `cloud-infrastructure-map-simple.html` | 简化版，基础展示 | ⭐⭐⭐ |
| `cloud-infrastructure-scatter.html` | 散点图版 | ⭐⭐ |

## 🔧 常用操作

### 添加新节点
1. 编辑对应供应商的 `nodes.json`
2. 添加节点对象到 `nodes` 数组
3. 更新 `last_updated` 字段
4. 刷新浏览器

### 修改供应商颜色
1. 打开 `cloud-infrastructure-map.html`
2. 找到 `const providers = {...}` (约692行)
3. 修改对应供应商的 `color` 值
4. 同时更新HTML中的图例颜色 (约605行)
5. 刷新浏览器

### 更改地图初始视图
在 `createMap()` 函数中修改：
```javascript
geo: {
    zoom: 1.2,        // 缩放级别 (1.0-2.0)
    center: [0, 20]   // 中心点 [经度, 纬度]
}
```

## 📈 数据统计速查

```
总节点数:    208
云服务商:    10家
覆盖国家:    36个
可用区总数:  268个
最新更新:    2025年1月
```

## 🎯 功能速查

| 功能 | 位置 | 快捷操作 |
|------|------|----------|
| 统计分析 | 页面顶部 | 滚动到顶部 |
| 图表分析 | 统计下方 | 4个图表并排 |
| 交互地图 | 中间部分 | 滚轮缩放，拖拽平移 |
| 重置地图 | 地图左下角 | 点击🔄按钮 |
| 节点明细 | 页面底部 | 搜索框/筛选器 |
| 云服务商筛选 | 明细表上方 | 下拉选择 |
| 节点搜索 | 明细表上方 | 输入关键词 |
| 分页浏览 | 明细表下方 | 上一页/下一页 |

## 🔍 搜索技巧

### 节点搜索支持
- 节点ID: `us-east-1`, `cn-beijing`
- 节点名称: `东京`, `伦敦`, `Virginia`
- 城市: `北京`, `上海`, `东京`
- 国家: `中国`, `美国`, `日本`

### 筛选组合
1. **单一供应商**: 选择"阿里云" → 查看29个节点
2. **状态筛选**: 选择"运行中" → 查看所有活跃节点
3. **搜索+筛选**: 选择"AWS" + 搜索"east" → 查看AWS东部节点
4. **地理搜索**: 搜索"欧洲" → 查看所有欧洲节点（需国家包含欧洲）

## 💡 常见问题快速解答

**Q: 页面无法加载？**  
A: 确保启动了 `python3 serve.py`

**Q: 地图不显示？**  
A: 检查浏览器控制台（F12），确保没有跨域错误

**Q: 数据不更新？**  
A: 清除浏览器缓存（Ctrl+Shift+R 或 Cmd+Shift+R）

**Q: 图表显示不全？**  
A: 放大浏览器窗口或刷新页面

**Q: 筛选无结果？**  
A: 检查是否同时设置了多个冲突的筛选条件

## 🎨 配色方案速查

### 橙色系（阿里、AWS）
- 阿里云: `#FF6A00` - 偏红橙
- AWS: `#FF9900` - 偏黄橙

### 蓝色系（Azure、Google、腾讯、IBM、DO、OVH）
- Azure: `#0078D4` - 中蓝
- Google Cloud: `#4285F4` - 亮蓝
- 腾讯云: `#006EFF` - 深蓝
- IBM 云: `#0F62FE` - 鲜蓝
- DigitalOcean: `#0080FF` - 天蓝
- OVH 云: `#123F6D` - 深海蓝

### 红色系（华为、Oracle）
- 华为云: `#D0021B` - 深红
- 甲骨文云: `#F80000` - 鲜红

## 📱 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl/Cmd + F` | 浏览器内搜索 |
| `Ctrl/Cmd + +` | 放大页面 |
| `Ctrl/Cmd + -` | 缩小页面 |
| `Ctrl/Cmd + 0` | 重置缩放 |
| `F5` | 刷新页面 |
| `Ctrl/Cmd + Shift + R` | 强制刷新（清除缓存） |
| `F12` | 打开开发者工具 |

## 🌐 浏览器兼容性

| 浏览器 | 支持 | 备注 |
|--------|------|------|
| Chrome 90+ | ✅ | 推荐，最佳性能 |
| Safari 14+ | ✅ | macOS推荐 |
| Firefox 88+ | ✅ | 可能需要清除缓存 |
| Edge 90+ | ✅ | Windows推荐 |
| IE 11 | ❌ | 不支持 |

## 📊 数据格式示例

### 最小节点对象
```json
{
  "node_id": "unique-id",
  "name": "显示名称",
  "location": {
    "country": "国家",
    "city": "城市",
    "latitude": 0.0,
    "longitude": 0.0
  },
  "availability_zones": 3,
  "status": "active",
  "launch_date": "2020-01-01T00:00:00"
}
```

## 🔗 有用的链接

- [完整项目结构](PROJECT_STRUCTURE.md)
- [更新日志](UPDATE_SUMMARY.md)
- [主README](README.md)
- [地图功能说明](CLOUD_MAP_README.md)

## 📞 获取帮助

1. 查看 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 详细文档
2. 查看 [常见问题](#💡-常见问题快速解答)
3. 检查浏览器控制台（F12）的错误信息
4. 提交 GitHub Issue

---

**提示**: 将本文档加入书签，方便快速查阅！  
**最后更新**: 2025年1月

