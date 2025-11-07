'use client';

import { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

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

    const option: echarts.EChartsOption = {
      title: {
        text: '各云服务商节点数量对比',
        left: 'center',
        textStyle: {
          fontSize: 20,
          fontWeight: 'bold',
        },
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow',
        },
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        containLabel: true,
      },
      xAxis: {
        type: 'category',
        data: [
          'Google Cloud',
          'Azure',
          '阿里云',
          'AWS',
          '甲骨文云',
          '腾讯云',
          '华为云',
          '火山引擎',
          'IBM 云',
          'DigitalOcean',
          'OVH 云',
        ],
        axisLabel: {
          rotate: 45,
          interval: 0,
        },
      },
      yAxis: {
        type: 'value',
        name: '节点数',
        max: 40,
      },
      series: [
        {
          name: '节点数',
          type: 'bar',
          data: [
            { value: 36, itemStyle: { color: '#34A853' } },
            { value: 34, itemStyle: { color: '#0078D4' } },
            { value: 29, itemStyle: { color: '#FF6A00' } },
            { value: 28, itemStyle: { color: '#FF9900' } },
            { value: 21, itemStyle: { color: '#C74634' } },
            { value: 18, itemStyle: { color: '#9C27B0' } },
            { value: 16, itemStyle: { color: '#D0021B' } },
            { value: 14, itemStyle: { color: '#00BCD4' } },
            { value: 11, itemStyle: { color: '#FFC107' } },
            { value: 10, itemStyle: { color: '#E91E63' } },
            { value: 9, itemStyle: { color: '#607D8B' } },
          ],
          label: {
            show: true,
            position: 'top',
            formatter: '{c}',
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

