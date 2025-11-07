'use client';

import { useState } from 'react';
import { CloudNode } from '@/types';
import { getAvailabilityZoneCount } from '@/lib/data';

interface NodesTableProps {
  nodes: CloudNode[];
  providers: Record<string, { name: string; color: string }>;
}

export default function NodesTable({ nodes, providers }: NodesTableProps) {
  const [currentPage, setCurrentPage] = useState(1);
  const [providerFilter, setProviderFilter] = useState<string>('all');
  const [continentFilter, setContinentFilter] = useState<string>('all');
  const itemsPerPage = 20;

  // 过滤节点
  let filteredNodes = nodes;
  if (providerFilter !== 'all') {
    filteredNodes = filteredNodes.filter(node => node.provider === providerFilter);
  }
  if (continentFilter !== 'all') {
    filteredNodes = filteredNodes.filter(node => node.location.continent === continentFilter);
  }

  const totalPages = Math.ceil(filteredNodes.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const pageData = filteredNodes.slice(startIndex, endIndex);

  const continents = Array.from(new Set(nodes.map(n => n.location.continent).filter(Boolean))).sort();

  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden">
      <div className="px-6 py-4 bg-gradient-to-r from-pink-600 to-rose-600 text-white">
        <h2 className="text-xl font-bold">节点明细</h2>
        <p className="text-sm text-pink-100 mt-1">所有云节点的详细信息</p>
      </div>
      
      {/* 筛选器 */}
      <div className="px-6 py-4 bg-gray-50 border-b border-gray-200 flex flex-wrap gap-4">
        <div className="flex items-center gap-2">
          <label className="text-sm font-medium text-gray-700">云服务商:</label>
          <select
            value={providerFilter}
            onChange={(e) => {
              setProviderFilter(e.target.value);
              setCurrentPage(1);
            }}
            className="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="all">全部</option>
            {Object.entries(providers).map(([id, provider]) => (
              <option key={id} value={id}>{provider.name}</option>
            ))}
          </select>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-sm font-medium text-gray-700">大洲:</label>
          <select
            value={continentFilter}
            onChange={(e) => {
              setContinentFilter(e.target.value);
              setCurrentPage(1);
            }}
            className="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="all">全部</option>
            {continents.map((continent, index) => (
              <option key={`continent-${continent}-${index}`} value={continent}>{continent}</option>
            ))}
          </select>
        </div>
        <div className="ml-auto text-sm text-gray-600">
          共 {filteredNodes.length} 个节点
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                节点ID
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                名称
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                云服务商
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                大洲
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                国家
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                城市
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                可用区
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                状态
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {pageData.map((node) => {
              const provider = providers[node.provider];
              const azCount = getAvailabilityZoneCount(node);
              return (
                <tr key={node.node_id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <code className="text-xs bg-gray-100 px-2 py-1 rounded text-gray-800">
                      {node.node_id}
                    </code>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">
                    {node.name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center gap-2">
                      <div
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: provider?.color || '#999' }}
                      />
                      <span className="text-sm">{provider?.name || node.provider}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 py-1 text-xs font-medium bg-indigo-100 text-indigo-800 rounded-full">
                      {node.location.continent}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-700">
                    {node.location.country}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-700">
                    {node.location.city}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-700 font-semibold">
                    {azCount} 个
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 py-1 text-xs font-medium rounded-full ${
                        node.status === 'active'
                          ? 'bg-green-100 text-green-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {node.status === 'active' ? '运行中' : '已停用'}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 flex items-center justify-between">
          <div className="text-sm text-gray-700">
            显示 {startIndex + 1} - {Math.min(endIndex, filteredNodes.length)} 条，共 {filteredNodes.length} 条
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
              disabled={currentPage === 1}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              上一页
            </button>
            <span className="px-4 py-2 text-sm font-medium text-gray-700">
              {currentPage} / {totalPages}
            </span>
            <button
              onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
              disabled={currentPage === totalPages}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              下一页
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

