'use client';

import { ProviderStat } from '@/types';

interface ProviderStatsTableProps {
  stats: ProviderStat[];
}

export default function ProviderStatsTable({ stats }: ProviderStatsTableProps) {
  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden">
      <div className="px-6 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white">
        <h2 className="text-xl font-bold">云服务商统计</h2>
        <p className="text-sm text-indigo-100 mt-1">各云服务商的节点和覆盖情况</p>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                云服务商
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                节点数
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                国家数
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                可用区总数
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {stats.map((stat, index) => (
              <tr key={stat.provider} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center gap-3">
                    <div
                      className="w-4 h-4 rounded-full"
                      style={{ backgroundColor: stat.color }}
                    />
                    <span className="font-medium text-gray-900">{stat.name}</span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-gray-700">
                  {stat.nodeCount}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-gray-700">
                  {stat.countryCount}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-gray-700 font-semibold">
                  {stat.azCount}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

