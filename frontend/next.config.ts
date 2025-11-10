import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // 输出配置 - Vercel 会自动处理，不需要静态导出
  // output: 'export', // 如果使用静态导出，取消注释此行
  
  // 图片优化配置
  images: {
    // 如果使用静态导出，需要设置为 true
    // unoptimized: true,
  },
  
  // 确保 public 目录正确服务
  // Next.js 默认会服务 public 目录，无需额外配置
  
  // 生产环境优化
  compress: true,
  
  // 环境变量
  env: {
    // 可以在这里添加环境变量
  },
};

export default nextConfig;
