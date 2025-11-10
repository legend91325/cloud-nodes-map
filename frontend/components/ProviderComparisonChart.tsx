'use client';

import { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import { providerColors, providerNameMap, providerOrder, chartTheme } from '@/lib/chartColors';

interface ProviderComparisonChartProps {
  className?: string;
}

export default function ProviderComparisonChart({ className }: ProviderComparisonChartProps) {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;

    if (!chartInstance.current) {
      chartInstance.current = echarts.init(chartRef.current);
    }

    const chart = chartInstance.current;

    // 节点数量数据（按 providerOrder 顺序）
    const nodeCounts: Record<string, number> = {
      'google_cloud': 36,
      'azure': 34,
      'alibaba_cloud': 29,
      'aws': 28,
      'oracle_cloud': 21,
      'tencent_cloud': 18,
      'huawei_cloud': 16,
      'volcano_engine': 14,
      'ibm_cloud': 11,
      'digitalocean': 10,
      'ovh_cloud': 9,
    };

    const option: echarts.EChartsOption = {
      backgroundColor: chartTheme.backgroundColor,
      title: {
        text: '各云服务商节点数量对比',
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
      grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        containLabel: true,
        borderColor: chartTheme.gridLineColor,
      },
      xAxis: {
        type: 'category',
        data: providerOrder.map(id => providerNameMap[id]),
        axisLabel: {
          rotate: 45,
          interval: 0,
          color: chartTheme.axisTextColor,
        },
        axisLine: {
          lineStyle: {
            color: chartTheme.gridLineColor,
          },
        },
      },
      yAxis: {
        type: 'value',
        name: '节点数',
        max: 40,
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
      series: [
        {
          name: '节点数',
          type: 'bar',
          data: providerOrder.map(id => ({
            value: nodeCounts[id] || 0,
            itemStyle: { color: providerColors[id] },
          })),
          label: {
            show: true,
            position: 'top',
            formatter: '{c}',
            color: chartTheme.axisTextColor,
          },
        },
      ],
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

