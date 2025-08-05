# 🚀 腾讯云 CloudBase 部署指南

## 优势
- ✅ 中国大陆访问速度快
- ✅ 免费额度：每月 1GB 存储 + 5GB 流量
- ✅ 自动 HTTPS
- ✅ 全球 CDN 加速
- ✅ 支持自定义域名

## 部署步骤

### 1. 注册腾讯云账号
访问 [腾讯云官网](https://cloud.tencent.com/) 注册账号

### 2. 开通 CloudBase
1. 进入 [CloudBase 控制台](https://console.cloud.tencent.com/tcb)
2. 创建环境（选择免费版）
3. 选择静态网站托管

### 3. 上传文件
```bash
# 方法一：通过控制台上传
# 在 CloudBase 控制台直接上传项目文件

# 方法二：使用 CLI 工具
npm install -g @cloudbase/cli
tcb login
tcb hosting:deploy . -e your-env-id
```

### 4. 配置域名
- 自动获得 `xxx.tcloudbaseapp.com` 域名
- 可绑定自定义域名

## 成本估算
- 免费额度足够个人项目使用
- 超出免费额度后按量计费，成本很低

---

## 快速部署脚本

创建 `deploy-tencent.js`:
```javascript
const fs = require('fs');
const path = require('path');

// 准备部署文件
const deployFiles = [
    'index.html',
    'aliyun_nodes_complete_min.json',
    'huaweicloud_nodes_complete_min.json',
    'tencentcloud_nodes_complete_min.json'
];

console.log('📦 准备部署文件...');
deployFiles.forEach(file => {
    if (fs.existsSync(file)) {
        console.log(`✅ ${file}`);
    } else {
        console.log(`❌ ${file} - 缺失`);
    }
});

console.log('\n🚀 部署步骤:');
console.log('1. 访问 https://console.cloud.tencent.com/tcb');
console.log('2. 创建新环境（选择免费版）');
console.log('3. 开通静态网站托管');
console.log('4. 上传上述文件');
console.log('5. 获得访问地址');
``` 