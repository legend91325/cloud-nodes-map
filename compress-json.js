const fs = require('fs');
const path = require('path');

// 压缩 JSON 文件
function compressJsonFiles() {
    const files = [
        'aliyun_nodes_complete.json',
        'huaweicloud_nodes_complete.json',
        'tencentcloud_nodes_complete.json'
    ];

    files.forEach(file => {
        if (fs.existsSync(file)) {
            try {
                const data = fs.readFileSync(file, 'utf8');
                const json = JSON.parse(data);
                
                // 创建压缩版本（移除不必要的空格和换行）
                const compressed = JSON.stringify(json);
                
                // 保存压缩版本
                const compressedFile = file.replace('.json', '_min.json');
                fs.writeFileSync(compressedFile, compressed);
                
                const originalSize = fs.statSync(file).size;
                const compressedSize = fs.statSync(compressedFile).size;
                const reduction = ((originalSize - compressedSize) / originalSize * 100).toFixed(2);
                
                console.log(`${file}: ${originalSize} bytes -> ${compressedSize} bytes (减少 ${reduction}%)`);
            } catch (error) {
                console.error(`处理 ${file} 时出错:`, error.message);
            }
        }
    });
}

// 运行压缩
compressJsonFiles(); 