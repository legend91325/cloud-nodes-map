const fs = require('fs');
const path = require('path');

console.log('🌍 云厂商区域变化历史数据收集工具\n');

// 定义数据源
const dataSources = {
    aliyun: {
        name: '阿里云',
        currentRegions: 28,
        sources: [
            'https://help.aliyun.com/document_detail/40654.html',
            'https://www.alibabacloud.com/help/en/elastic-compute-service/latest/regions-and-zones',
            'https://www.alibabacloud.com/about/annual-report'
        ],
        wayback: 'https://web.archive.org/web/*/https://www.alibabacloud.com/help/en/elastic-compute-service/latest/regions-and-zones'
    },
    huawei: {
        name: '华为云',
        currentRegions: 26,
        sources: [
            'https://support.huaweicloud.com/intl/en-us/endpoint/index.html',
            'https://support.huaweicloud.com/intl/en-us/',
            'https://www.huawei.com/en/annual-report'
        ],
        wayback: 'https://web.archive.org/web/*/https://support.huaweicloud.com/intl/en-us/endpoint/index.html'
    },
    tencent: {
        name: '腾讯云',
        currentRegions: 16,
        sources: [
            'https://intl.cloud.tencent.com/document/product/213/6091',
            'https://intl.cloud.tencent.com/document',
            'https://www.tencent.com/en-us/investors.html'
        ],
        wayback: 'https://web.archive.org/web/*/https://intl.cloud.tencent.com/document/product/213/6091'
    }
};

// 显示数据源信息
console.log('📊 当前区域数量:');
Object.keys(dataSources).forEach(key => {
    const provider = dataSources[key];
    console.log(`  ${provider.name}: ${provider.currentRegions} 个区域`);
});

console.log('\n🔍 数据收集渠道:');

Object.keys(dataSources).forEach(key => {
    const provider = dataSources[key];
    console.log(`\n${provider.name}:`);
    provider.sources.forEach((source, index) => {
        console.log(`  ${index + 1}. ${source}`);
    });
    console.log(`  📚 Wayback Machine: ${provider.wayback}`);
});

console.log('\n📈 历史数据获取方法:');
console.log('\n1️⃣ Wayback Machine 历史快照');
console.log('   - 访问上述 Wayback Machine 链接');
console.log('   - 选择不同年份查看历史版本');
console.log('   - 对比区域列表变化');

console.log('\n2️⃣ 官方年度报告');
console.log('   - 查看各云厂商年度报告');
console.log('   - 关注基础设施投资章节');
console.log('   - 分析区域扩张计划');

console.log('\n3️⃣ 技术博客和新闻');
console.log('   - 关注官方博客发布');
console.log('   - 搜索区域开通新闻');
console.log('   - 查看产品发布历史');

console.log('\n4️⃣ 第三方报告');
console.log('   - Gartner 云基础设施报告');
console.log('   - IDC 云服务市场报告');
console.log('   - Forrester 云平台报告');

console.log('\n🛠️ 数据收集建议:');
console.log('1. 建立定期检查机制（每月/季度）');
console.log('2. 记录区域开通时间线');
console.log('3. 分析区域分布趋势');
console.log('4. 对比不同云厂商策略');

console.log('\n📋 建议收集的数据点:');
console.log('- 区域开通时间');
console.log('- 区域地理位置');
console.log('- 可用区数量');
console.log('- 服务类型覆盖');
console.log('- 合规认证情况');

console.log('\n💡 自动化建议:');
console.log('- 使用爬虫定期抓取官方文档');
console.log('- 设置 RSS 订阅官方博客');
console.log('- 建立数据库存储历史数据');
console.log('- 创建可视化图表展示趋势'); 