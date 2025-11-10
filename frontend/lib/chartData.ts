/**
 * 图表数据配置
 * 定义各图表的数据和系列配置
 */

import { providerColors, providerNameMap, providerOrder } from './chartColors';

// 增长趋势数据
export const growthTrendData: Record<string, number[]> = {
  'aws': [1, 2, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 29],
  'azure': [0, 0, 0, 0, 1, 3, 5, 7, 10, 13, 16, 19, 22, 26, 29, 32, 34, 35, 36, 36],
  'google_cloud': [0, 0, 0, 0, 1, 2, 3, 4, 6, 8, 11, 14, 17, 20, 23, 26, 29, 32, 34, 34],
  'alibaba_cloud': [0, 0, 0, 0, 0, 1, 2, 3, 5, 7, 9, 11, 14, 17, 20, 23, 26, 28, 29, 29],
  'huawei_cloud': [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 4, 6, 9, 12, 15, 17, 18, 18, 18, 18],
  'tencent_cloud': [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 5, 7, 9, 11, 13, 15, 16, 16, 16],
  'volcano_engine': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 6, 9, 10, 10, 10],
  'oracle_cloud': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8],
  'ibm_cloud': [0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 10, 10],
  'ovh_cloud': [0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8, 8, 8],
  'digitalocean': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 6, 6, 6, 6],
};

// 创建增长趋势系列配置
export function createGrowthTrendSeries() {
  return providerOrder.map(providerId => {
    const color = providerColors[providerId];
    const name = providerNameMap[providerId];
    const data = growthTrendData[providerId] || [];
    
    return {
      name,
      type: 'line' as const,
      data,
      itemStyle: { color },
      symbol: 'circle',
      symbolSize: 6,
      label: {
        show: true,
        position: 'right' as const,
        formatter: (params: any) => {
          if (params.dataIndex === 19) {
            return params.value.toString();
          }
          return '';
        },
        color,
        fontSize: 12,
        fontWeight: 'bold' as const,
      },
    };
  });
}

