import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Analytics from "@/components/Analytics";
import VercelAnalytics from "@/components/VercelAnalytics";
import Navigation from "@/components/Navigation";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "云计算指北 | 专业的云计算资讯与服务平台",
  description: "为您提供最新的云计算资讯、全球基础设施节点分布、云服务商对比分析等专业内容",
  keywords: "云计算,云基础设施,数据中心,云服务商,节点分布,AWS,Azure,Google Cloud,阿里云",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans antialiased`} suppressHydrationWarning>
        <Navigation />
        {children}
        {/* Google Analytics 4 */}
        <Analytics gaId={process.env.NEXT_PUBLIC_GA_ID} />
        {/* Vercel Analytics & Speed Insights */}
        <VercelAnalytics />
      </body>
    </html>
  );
}
