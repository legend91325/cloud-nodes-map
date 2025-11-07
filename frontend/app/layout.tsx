import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "全球云基础设施节点分布图 | Cloud Infrastructure Map",
  description: "可视化展示全球主要云服务商的数据中心分布情况，包括AWS、Azure、Google Cloud、阿里云等11家云服务商",
  keywords: "云基础设施,数据中心,云服务商,节点分布,AWS,Azure,Google Cloud,阿里云",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans antialiased`} suppressHydrationWarning>
        {children}
      </body>
    </html>
  );
}
