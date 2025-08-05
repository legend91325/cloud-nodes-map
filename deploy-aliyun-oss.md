# 🚀 阿里云 OSS + CDN 部署指南

## 优势
- ✅ 中国大陆访问速度快
- ✅ 成本极低（按量计费）
- ✅ 全球 CDN 加速
- ✅ 支持自定义域名
- ✅ 高可用性

## 部署步骤

### 1. 开通阿里云 OSS
1. 访问 [阿里云 OSS 控制台](https://oss.console.aliyun.com/)
2. 创建 Bucket（存储空间）
3. 设置权限为"公共读"

### 2. 上传文件
```bash
# 使用阿里云 CLI 工具
pip install ossutil
ossutil config
ossutil cp index.html oss://your-bucket-name/
ossutil cp *.json oss://your-bucket-name/
```

### 3. 配置静态网站托管
1. 在 OSS 控制台开启"静态网站托管"
2. 设置默认首页为 `index.html`

### 4. 配置 CDN 加速（可选）
1. 开通阿里云 CDN
2. 添加加速域名
3. 配置源站为 OSS 域名

## 成本估算
- OSS 存储：约 0.12元/GB/月
- CDN 流量：约 0.24元/GB
- 对于小型项目，月成本通常 < 1元

---

## 自动化部署脚本

创建 `deploy-aliyun.js`:
```javascript
const fs = require('fs');
const { exec } = require('child_process');

const files = [
    'index.html',
    'aliyun_nodes_complete_min.json',
    'huaweicloud_nodes_complete_min.json',
    'tencentcloud_nodes_complete_min.json'
];

console.log('📦 检查部署文件...');
files.forEach(file => {
    if (fs.existsSync(file)) {
        const stats = fs.statSync(file);
        console.log(`✅ ${file} (${(stats.size/1024).toFixed(2)} KB)`);
    } else {
        console.log(`❌ ${file} - 缺失`);
    }
});

console.log('\n🚀 部署命令:');
console.log('1. 安装 ossutil: pip install ossutil');
console.log('2. 配置: ossutil config');
console.log('3. 上传: ossutil cp . oss://your-bucket-name/ -r');
console.log('4. 设置静态网站托管');
``` 