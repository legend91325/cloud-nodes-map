'use client';

import { useState, useMemo } from 'react';
import { CloudNode } from '@/types';
import { getAvailabilityZoneCount } from '@/lib/data';

interface ProviderCountryStatsTableProps {
  nodes: CloudNode[];
  providers: Record<string, { name: string; color: string }>;
}

interface ProviderCountryStat {
  provider: string;
  providerName: string;
  country: string;
  nodeCount: number;
  azCount: number;
}

export default function ProviderCountryStatsTable({ nodes, providers }: ProviderCountryStatsTableProps) {
  const [currentPage, setCurrentPage] = useState(1);
  const [providerFilter, setProviderFilter] = useState<string>('all');
  const itemsPerPage = 20;

  // 计算云服务商国家统计数据
  const stats = useMemo(() => {
    const statsMap: Record<string, ProviderCountryStat> = {};

    nodes.forEach(node => {
      const key = `${node.provider}-${node.location.country}`;
      if (!statsMap[key]) {
        const provider = providers[node.provider];
        statsMap[key] = {
          provider: node.provider,
          providerName: provider?.name || node.provider,
          country: node.location.country,
          nodeCount: 0,
          azCount: 0,
        };
      }
      statsMap[key].nodeCount++;
      statsMap[key].azCount += getAvailabilityZoneCount(node);
    });

    return Object.values(statsMap).sort((a, b) => {
      // 先按云服务商排序，再按国家排序
      if (a.providerName !== b.providerName) {
        return a.providerName.localeCompare(b.providerName, 'zh-CN');
      }
      return a.country.localeCompare(b.country, 'zh-CN');
    });
  }, [nodes, providers]);

  // 过滤数据
  const filteredStats = useMemo(() => {
    if (providerFilter === 'all') {
      return stats;
    }
    return stats.filter(stat => stat.provider === providerFilter);
  }, [stats, providerFilter]);

  const totalPages = Math.ceil(filteredStats.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const pageData = filteredStats.slice(startIndex, endIndex);

  return (
    <div className="bg-white rounded-lg shadow-md border border-neutral-200 overflow-hidden">
      <div className="px-6 py-4 bg-gradient-to-r from-primary-500 to-primary-600 text-white">
        <h2 className="text-lg font-semibold">云服务商国家覆盖明细</h2>
        <p className="text-sm text-primary-50 mt-1 opacity-90">各云服务商在各国家的节点和可用区分布情况</p>
      </div>

      {/* 筛选器 */}
      <div className="px-6 py-4 bg-white border-b border-neutral-200 flex flex-wrap gap-4">
        <div className="flex items-center gap-2">
          <label className="text-sm font-medium text-neutral-700">云服务商:</label>
          <select
            value={providerFilter}
            onChange={(e) => {
              setProviderFilter(e.target.value);
              setCurrentPage(1);
            }}
            className="px-3 py-2 text-sm border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          >
            <option value="all">全部</option>
            {Object.entries(providers).map(([id, provider]) => (
              <option key={id} value={id}>{provider.name}</option>
            ))}
          </select>
        </div>
        <div className="ml-auto text-sm text-neutral-500">
          共 {filteredStats.length} 条记录
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-primary-50 border-b border-neutral-200">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-semibold text-primary-700 uppercase tracking-wider">
                云服务商
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-primary-700 uppercase tracking-wider">
                国家
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-primary-700 uppercase tracking-wider">
                节点数
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-primary-700 uppercase tracking-wider">
                可用区数
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-neutral-200">
            {pageData.map((stat, index) => (
              <tr key={`${stat.provider}-${stat.country}-${index}`} className="hover:bg-primary-50 transition-colors">
                <td className="px-4 py-3 whitespace-nowrap">
                  <div className="flex items-center gap-3">
                    <div
                      className="w-4 h-4 rounded-full"
                      style={{ backgroundColor: providers[stat.provider]?.color || '#999' }}
                    />
                    <span className="font-medium text-neutral-900">{stat.providerName}</span>
                  </div>
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-neutral-900">
                  {stat.country}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-neutral-900">
                  {stat.nodeCount} 个
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-neutral-900 font-medium">
                  {stat.azCount} 个
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="px-6 py-4 bg-white border-t border-neutral-200 flex items-center justify-between">
          <div className="text-sm text-neutral-500">
            显示 {startIndex + 1} - {Math.min(endIndex, filteredStats.length)} 条，共 {filteredStats.length} 条
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
              disabled={currentPage === 1}
              className="px-4 py-2 text-sm font-medium text-neutral-700 bg-white border border-neutral-300 rounded-md hover:bg-neutral-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
            >
              上一页
            </button>
            <span className="px-4 py-2 text-sm font-medium text-neutral-500">
              {currentPage} / {totalPages}
            </span>
            <button
              onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
              disabled={currentPage === totalPages}
              className="px-4 py-2 text-sm font-medium text-neutral-700 bg-white border border-neutral-300 rounded-md hover:bg-neutral-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
            >
              下一页
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

