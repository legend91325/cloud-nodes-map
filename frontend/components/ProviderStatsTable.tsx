'use client';

import { ProviderStat } from '@/types';

interface ProviderStatsTableProps {
  stats: ProviderStat[];
}

export default function ProviderStatsTable({ stats }: ProviderStatsTableProps) {
  return (
    <div className="bg-white rounded-lg shadow-md border border-neutral-200 overflow-hidden">
      <div className="px-6 py-4 bg-gradient-to-r from-primary-500 to-primary-600 text-white">
        <h2 className="text-lg font-semibold">云服务商统计</h2>
        <p className="text-sm text-primary-50 mt-1 opacity-90">各云服务商的节点和覆盖情况</p>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-primary-50 border-b border-neutral-200">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-semibold text-primary-700 uppercase tracking-wider">
                云服务商
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-primary-700 uppercase tracking-wider">
                节点数
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-primary-700 uppercase tracking-wider">
                国家数
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-primary-700 uppercase tracking-wider">
                可用区总数
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-neutral-200">
            {stats.map((stat, index) => (
              <tr key={stat.provider} className="hover:bg-primary-50 transition-colors">
                <td className="px-4 py-3 whitespace-nowrap">
                  <div className="flex items-center gap-3">
                    <div
                      className="w-4 h-4 rounded-full"
                      style={{ backgroundColor: stat.color }}
                    />
                    <span className="font-medium text-neutral-900">{stat.name}</span>
                  </div>
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-neutral-900">
                  {stat.nodeCount}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-neutral-900">
                  {stat.countryCount}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-neutral-900 font-medium">
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

