const fs = require('fs');
const path = require('path');

console.log('🚀 云服务提供商全球节点地图 - 部署工具\n');

// 检查必要文件
const requiredFiles = [
    'index.html',
    'aliyun_nodes_complete_min.json',
    'huaweicloud_nodes_complete_min.json',
    'tencentcloud_nodes_complete_min.json'
];

console.log('📁 检查部署文件:');
let allFilesExist = true;
requiredFiles.forEach(file => {
    if (fs.existsSync(file)) {
        const stats = fs.statSync(file);
        console.log(`  ✅ ${file} (${(stats.size/1024).toFixed(2)} KB)`);
    } else {
        console.log(`  ❌ ${file} - 缺失`);
        allFilesExist = false;
    }
});

if (!allFilesExist) {
    console.log('\n❌ 请先运行 npm run compress 压缩 JSON 文件');
    process.exit(1);
}

console.log('\n🌍 推荐部署平台（中国大陆访问速度快）:');
console.log('\n1️⃣ 腾讯云 CloudBase (推荐)');
console.log('   ✅ 免费额度充足');
console.log('   ✅ 中国大陆访问速度快');
console.log('   ✅ 自动 HTTPS + CDN');
console.log('   🔗 https://console.cloud.tencent.com/tcb');
console.log('   💰 免费额度：1GB 存储 + 5GB 流量/月');

console.log('\n2️⃣ 阿里云 OSS + CDN');
console.log('   ✅ 成本极低');
console.log('   ✅ 全球 CDN 加速');
console.log('   ✅ 高可用性');
console.log('   🔗 https://oss.console.aliyun.com/');
console.log('   💰 约 0.12元/GB/月');

console.log('\n3️⃣ 华为云 OBS');
console.log('   ✅ 免费额度');
console.log('   ✅ 中国大陆访问速度快');
console.log('   🔗 https://console.huaweicloud.com/obs/');
console.log('   💰 免费额度：5GB 存储');

console.log('\n4️⃣ Netlify');
console.log('   ✅ 部分节点访问较快');
console.log('   ✅ 免费额度充足');
console.log('   🔗 https://app.netlify.com/');
console.log('   💰 免费额度：100GB 流量/月');

console.log('\n📋 部署步骤:');
console.log('1. 选择上述任一平台');
console.log('2. 注册账号并开通服务');
console.log('3. 上传以下文件:');
requiredFiles.forEach(file => {
    console.log(`   - ${file}`);
});
console.log('4. 配置静态网站托管');
console.log('5. 获得访问地址');

console.log('\n💡 提示:');
console.log('- 建议选择腾讯云 CloudBase，操作简单且免费额度充足');
console.log('- 如需自定义域名，可绑定到部署平台');
console.log('- 所有平台都支持 HTTPS 和 CDN 加速');

console.log('\n🔧 其他命令:');
console.log('npm run compress  # 压缩 JSON 文件');
console.log('npm run verify    # 验证项目配置');
console.log('npm run dev       # 本地开发'); 