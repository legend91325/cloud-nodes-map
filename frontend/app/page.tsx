'use client';

import Link from 'next/link';
import { useEffect } from 'react';

export default function Home() {
  useEffect(() => {
    // 开发模式下，加载 Analytics 调试工具
    if (process.env.NODE_ENV === 'development' && typeof window !== 'undefined') {
      import('@/lib/analytics-debug').then(({ showAnalyticsDebugPanel }) => {
        setTimeout(() => {
          showAnalyticsDebugPanel();
        }, 2000);
      });
    }
  }, []);

  return (
    <div className="min-h-screen bg-neutral-50 pt-16">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-50 via-white to-primary-50 py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl md:text-6xl font-bold text-neutral-900 mb-6">
              云计算指北
            </h1>
            <p className="text-xl text-neutral-600 mb-8">
              专业的云计算资讯与服务平台
            </p>
            <p className="text-lg text-neutral-500 mb-12 max-w-2xl mx-auto">
              为您提供最新的云计算资讯、全球基础设施节点分布、云服务商对比分析等专业内容
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Link
                href="/services/infrastructure"
                className="px-6 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors font-medium shadow-sm"
              >
                查看全球基础设施
              </Link>
              <Link
                href="/news"
                className="px-6 py-3 bg-white text-primary-600 border border-primary-600 rounded-md hover:bg-primary-50 transition-colors font-medium shadow-sm"
              >
                阅读最新资讯
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-semibold text-neutral-900 text-center mb-12">
            核心功能
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="bg-white rounded-lg shadow-sm border border-neutral-200 p-6 hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">🌍</span>
              </div>
              <h3 className="text-xl font-semibold text-neutral-900 mb-2">
                全球基础设施
              </h3>
              <p className="text-neutral-600 mb-4">
                可视化展示全球主要云服务商的数据中心分布情况，包括 AWS、Azure、Google Cloud 等
              </p>
              <Link
                href="/services/infrastructure"
                className="text-primary-600 hover:text-primary-700 font-medium text-sm"
              >
                查看详情 →
              </Link>
            </div>

            {/* Feature 2 */}
            <div className="bg-white rounded-lg shadow-sm border border-neutral-200 p-6 hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">📊</span>
              </div>
              <h3 className="text-xl font-semibold text-neutral-900 mb-2">
                数据分析
              </h3>
              <p className="text-neutral-600 mb-4">
                提供详细的云服务商对比分析、节点分布统计、增长趋势等数据可视化
              </p>
              <Link
                href="/services/infrastructure"
                className="text-primary-600 hover:text-primary-700 font-medium text-sm"
              >
                查看详情 →
              </Link>
            </div>

            {/* Feature 3 */}
            <div className="bg-white rounded-lg shadow-sm border border-neutral-200 p-6 hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">📰</span>
              </div>
              <h3 className="text-xl font-semibold text-neutral-900 mb-2">
                最新资讯
              </h3>
              <p className="text-neutral-600 mb-4">
                及时更新云计算行业的最新动态、技术趋势、产品发布等专业资讯
              </p>
              <Link
                href="/news"
                className="text-primary-600 hover:text-primary-700 font-medium text-sm"
              >
                查看详情 →
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-4xl font-bold text-primary-600 mb-2">11+</div>
              <div className="text-neutral-600">云服务商</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-primary-600 mb-2">208+</div>
              <div className="text-neutral-600">全球节点</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-primary-600 mb-2">36+</div>
              <div className="text-neutral-600">覆盖国家</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-primary-600 mb-2">268+</div>
              <div className="text-neutral-600">可用区</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-primary-600 to-primary-700 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-semibold mb-4">
            开始探索全球云基础设施
          </h2>
          <p className="text-primary-50 mb-8 max-w-2xl mx-auto">
            深入了解全球主要云服务商的数据中心分布，做出更明智的技术决策
          </p>
          <Link
            href="/services/infrastructure"
            className="inline-block px-8 py-3 bg-white text-primary-600 rounded-md hover:bg-neutral-50 transition-colors font-medium shadow-lg"
          >
            立即查看
          </Link>
        </div>
      </section>
    </div>
  );
}
