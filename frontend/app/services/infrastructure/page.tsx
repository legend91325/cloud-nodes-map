'use client';

import { useEffect, useState, useMemo } from 'react';
import dynamic from 'next/dynamic';
import StatsCard from '@/components/StatsCard';
import ProviderStatsTable from '@/components/ProviderStatsTable';
import ProviderCountryStatsTable from '@/components/ProviderCountryStatsTable';
import NodesTable from '@/components/NodesTable';
import { CloudNode, ProviderMetadata, ProviderStat } from '@/types';
import { loadAllNodes, loadProviderMetadata, getAvailabilityZoneCount } from '@/lib/data';

// 动态导入 MapChart，禁用 SSR 以避免 hydration 错误
const MapChart = dynamic(() => import('@/components/MapChart'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[600px] rounded-xl overflow-hidden shadow-lg bg-white flex items-center justify-center">
      <div className="text-center">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-2 border-primary-500 border-t-transparent mb-2"></div>
        <p className="text-sm text-neutral-500">加载地图中...</p>
      </div>
    </div>
  ),
});

// 动态导入图表组件，禁用 SSR
const GrowthTrendChart = dynamic(() => import('@/components/GrowthTrendChart'), { ssr: false });
const ContinentDistributionChart = dynamic(() => import('@/components/ContinentDistributionChart'), { ssr: false });
const ProviderComparisonChart = dynamic(() => import('@/components/ProviderComparisonChart'), { ssr: false });

export default function InfrastructurePage() {
  const [nodes, setNodes] = useState<CloudNode[]>([]);
  const [metadata, setMetadata] = useState<ProviderMetadata | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedProviders, setSelectedProviders] = useState<string[]>([]);
  const [mounted, setMounted] = useState(false);

  // 确保只在客户端执行
  useEffect(() => {
    setMounted(true);
    
    // 开发模式下，加载 Analytics 调试工具
    if (process.env.NODE_ENV === 'development' && typeof window !== 'undefined') {
      import('@/lib/analytics-debug').then(({ showAnalyticsDebugPanel }) => {
        setTimeout(() => {
          showAnalyticsDebugPanel();
        }, 2000);
      });
    }
  }, []);

  useEffect(() => {
    if (!mounted) return;
    
    async function fetchData() {
      setLoading(true);
      try {
        const [nodesData, metadataData] = await Promise.all([
          loadAllNodes(),
          loadProviderMetadata(),
        ]);
        setNodes(nodesData);
        setMetadata(metadataData);
      } catch (error) {
        console.error('Failed to load data:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [mounted]);

  // 计算统计数据
  const stats = useMemo(() => {
    if (!metadata || nodes.length === 0) {
      return {
        totalNodes: 0,
        totalCountries: 0,
        totalAZs: 0,
        totalProviders: 0,
      };
    }

    const countries = new Set(nodes.map(n => n.location.country));
    const totalAZs = nodes.reduce((sum, node) => sum + getAvailabilityZoneCount(node), 0);

    return {
      totalNodes: nodes.length,
      totalCountries: countries.size,
      totalAZs,
      totalProviders: Object.keys(metadata.providers).length,
    };
  }, [nodes, metadata]);

  // 计算云服务商统计
  const providerStats = useMemo(() => {
    if (!metadata || nodes.length === 0) return [];

    const statsMap: Record<string, ProviderStat> = {};
    
    nodes.forEach(node => {
      if (!statsMap[node.provider]) {
        const provider = metadata.providers[node.provider];
        statsMap[node.provider] = {
          provider: node.provider,
          name: provider.name,
          nodeCount: 0,
          countryCount: 0,
          azCount: 0,
          color: provider.color,
        };
      }
      
      statsMap[node.provider].nodeCount++;
      statsMap[node.provider].azCount += getAvailabilityZoneCount(node);
    });

    // 计算国家数
    Object.keys(statsMap).forEach(providerId => {
      const providerNodes = nodes.filter(n => n.provider === providerId);
      const countries = new Set(providerNodes.map(n => n.location.country));
      statsMap[providerId].countryCount = countries.size;
    });

    return Object.values(statsMap).sort((a, b) => b.nodeCount - a.nodeCount);
  }, [nodes, metadata]);

  if (loading || !mounted) {
    return (
      <div className="min-h-screen bg-neutral-50 pt-16">
        <div className="container mx-auto px-4 py-12">
          <div className="flex items-center justify-center h-96">
            <div className="text-center">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mb-4"></div>
              <p className="text-neutral-500">加载中...</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-neutral-50 pt-16">
      <div className="container mx-auto px-4 py-8">
        {/* 页面标题 */}
        <div className="mb-8">
          <h1 className="text-3xl font-semibold text-neutral-900 mb-2">
            全球云基础设施节点分布
          </h1>
          <p className="text-neutral-600">
            可视化展示全球主要云服务商的数据中心分布情况
          </p>
        </div>

        {/* 统计卡片 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsCard
            label="云服务商"
            number={stats.totalProviders}
            icon="☁️"
          />
          <StatsCard
            label="节点总数"
            number={stats.totalNodes}
            icon="📍"
          />
          <StatsCard
            label="覆盖国家"
            number={stats.totalCountries}
            icon="🌍"
          />
          <StatsCard
            label="可用区"
            number={stats.totalAZs}
            icon="⚡"
          />
        </div>

        {/* 地图 */}
        <div className="mb-8">
          <div className="bg-white rounded-lg shadow-md border border-neutral-200 p-6">
            <div className="mb-4">
              <h2 className="text-xl font-semibold text-primary-600 mb-1">全球节点分布地图</h2>
              <p className="text-sm text-neutral-500">点击图例可筛选云服务商，拖拽可缩放地图</p>
            </div>
            <MapChart
              nodes={nodes}
              providers={metadata?.providers || {}}
              selectedProviders={selectedProviders}
            />
          </div>
        </div>

        {/* 图表分析区域 */}
        {/* 节点数量对比 */}
        <div className="mb-8">
          <div className="bg-white rounded-lg shadow-md border border-neutral-200 p-6">
            <div className="mb-4">
              <h2 className="text-lg font-semibold text-primary-600 mb-1">各云服务商节点数量对比</h2>
              <p className="text-sm text-neutral-500">
                对比各大云服务商的全球数据中心节点总数。Google Cloud 以36个节点领先,Azure 紧随其后34个,阿里云以29个节点位列第三。节点数量直接影响服务可用性和用户访问速度,是评估云服务商基础设施实力的重要指标。
              </p>
            </div>
            <ProviderComparisonChart />
          </div>
        </div>

        {/* 大洲分布 */}
        <div className="mb-8">
          <div className="bg-white rounded-lg shadow-md border border-neutral-200 p-6">
            <div className="mb-4">
              <h2 className="text-lg font-semibold text-primary-600 mb-1">各大洲节点分布</h2>
              <p className="text-sm text-neutral-500">
                展示各云服务商在全球各大洲的节点分布情况。亚洲作为主要市场拥有最多节点(80+),其中中国云服务商优势明显。北美和欧洲市场由国际巨头主导。通过颜色区分可清晰看出各服务商的区域布局策略,帮助企业选择最适合业务地域的云服务商。
              </p>
            </div>
            <ContinentDistributionChart />
          </div>
        </div>

        {/* 增长趋势图 */}
        <div className="mb-8">
          <div className="bg-white rounded-lg shadow-md border border-neutral-200 p-6">
            <div className="mb-4">
              <h2 className="text-lg font-semibold text-primary-600 mb-1">云服务商 节点逐年增长趋势</h2>
              <p className="text-sm text-neutral-500">
                展示 2006-2025年各云服务商节点的累积增长轨迹。AWS作为先行者从2006年开始布局,Azure 和 Google Cloud 在2010年后快速追赶。中国云服务商(阿里云、华为云、腾讯云)从2010年代中期开始发力,增长势头强劲。曲线末端数值代表当前总节点数,反映各服务商的发展速度和市场策略。
              </p>
            </div>
            <GrowthTrendChart />
          </div>
        </div>

        {/* 云服务商统计表格 */}
        <div className="mb-8">
          <ProviderStatsTable stats={providerStats} />
        </div>

        {/* 云服务商国家覆盖明细表格 */}
        <div className="mb-8">
          <ProviderCountryStatsTable 
            nodes={nodes} 
            providers={metadata ? Object.entries(metadata.providers).reduce((acc, [id, provider]) => {
              acc[id] = { name: provider.name, color: provider.color };
              return acc;
            }, {} as Record<string, { name: string; color: string }>) : {}} 
          />
        </div>

        {/* 节点明细表 */}
        <div className="mb-8">
          <NodesTable 
            nodes={nodes} 
            providers={metadata ? Object.entries(metadata.providers).reduce((acc, [id, provider]) => {
              acc[id] = { name: provider.name, color: provider.color };
              return acc;
            }, {} as Record<string, { name: string; color: string }>) : {}} 
          />
        </div>
      </div>
    </div>
  );
}

