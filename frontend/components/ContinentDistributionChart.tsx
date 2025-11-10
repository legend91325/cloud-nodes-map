'use client';

import { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import { providerColors, providerNameMap, providerOrder, chartTheme } from '@/lib/chartColors';

interface ContinentDistributionChartProps {
  className?: string;
}

export default function ContinentDistributionChart({ className }: ContinentDistributionChartProps) {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;

    if (!chartInstance.current) {
      chartInstance.current = echarts.init(chartRef.current);
    }

    const chart = chartInstance.current;

    // 大洲分布数据（按 providerOrder 顺序）
    const continentData: Record<string, number[]> = {
      'alibaba_cloud': [24, 0, 0, 0, 0, 0, 0],
      'aws': [10, 5, 3, 1, 1, 1, 0],
      'azure': [11, 11, 9, 1, 1, 1, 0],
      'google_cloud': [10, 12, 7, 1, 1, 1, 0],
      'huawei_cloud': [12, 4, 9, 1, 1, 1, 1],
      'tencent_cloud': [14, 6, 5, 1, 1, 1, 0],
      'volcano_engine': [12, 3, 3, 1, 1, 1, 0],
      'oracle_cloud': [8, 0, 4, 1, 1, 1, 0],
      'ibm_cloud': [0, 0, 0, 0, 0, 0, 0],
      'ovh_cloud': [0, 0, 0, 0, 0, 0, 0],
      'digitalocean': [3, 0, 4, 1, 1, 1, 0],
    };

    const option: echarts.EChartsOption = {
      backgroundColor: chartTheme.backgroundColor,
      title: {
        text: '各大洲节点分布',
        left: 'center',
        textStyle: {
          fontSize: 20,
          fontWeight: 'bold',
          color: chartTheme.titleTextColor,
        },
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow',
        },
        backgroundColor: chartTheme.tooltip.backgroundColor,
        borderColor: chartTheme.tooltip.borderColor,
        textStyle: {
          color: chartTheme.tooltip.textColor,
        },
      },
      legend: {
        data: providerOrder.map(id => providerNameMap[id]),
        bottom: 10,
        type: 'scroll',
        textStyle: {
          color: chartTheme.axisTextColor,
        },
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        containLabel: true,
        borderColor: chartTheme.gridLineColor,
      },
      xAxis: {
        type: 'category',
        data: ['亚洲', '欧洲', '北美洲', '南美洲', '非洲', '大洋洲', '其他'],
        axisLine: {
          lineStyle: {
            color: chartTheme.gridLineColor,
          },
        },
        axisLabel: {
          color: chartTheme.axisTextColor,
        },
      },
      yAxis: {
        type: 'value',
        name: '节点数',
        max: 120,
        nameTextStyle: {
          color: chartTheme.axisTextColor,
        },
        axisLine: {
          lineStyle: {
            color: chartTheme.gridLineColor,
          },
        },
        axisLabel: {
          color: chartTheme.axisTextColor,
        },
        splitLine: {
          lineStyle: {
            color: chartTheme.gridLineColor,
            type: 'dashed',
          },
        },
      },
      series: providerOrder.map(id => ({
        name: providerNameMap[id],
        type: 'bar' as const,
        stack: 'total',
        data: continentData[id] || [0, 0, 0, 0, 0, 0, 0],
        itemStyle: { color: providerColors[id] },
        label: {
          show: true,
          position: 'inside' as const,
          color: '#FFFFFF',
          fontSize: 10,
        },
      })),
    };

    chart.setOption(option);

    const handleResize = () => {
      chart.resize();
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <div className={`w-full h-[500px] ${className || ''}`}>
      <div ref={chartRef} className="w-full h-full" />
    </div>
  );
}

