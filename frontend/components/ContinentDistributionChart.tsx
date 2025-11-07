'use client';

import { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

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

    const option: echarts.EChartsOption = {
      title: {
        text: '各大洲节点分布',
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
      legend: {
        data: [
          '阿里云',
          'AWS',
          'Azure',
          'Google Cloud',
          '华为云',
          '腾讯云',
          '火山引擎',
          '甲骨文云',
          'IBM 云',
          'OVH 云',
          'DigitalOcean',
        ],
        bottom: 10,
        type: 'scroll',
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        containLabel: true,
      },
      xAxis: {
        type: 'category',
        data: ['亚洲', '欧洲', '北美洲', '南美洲', '非洲', '大洋洲', '其他'],
      },
      yAxis: {
        type: 'value',
        name: '节点数',
        max: 120,
      },
      series: [
        {
          name: '阿里云',
          type: 'bar',
          stack: 'total',
          data: [24, 0, 0, 0, 0, 0, 0],
          itemStyle: { color: '#FF6A00' },
          label: {
            show: true,
            position: 'inside',
          },
        },
        {
          name: 'AWS',
          type: 'bar',
          stack: 'total',
          data: [10, 5, 3, 1, 1, 1, 0],
          itemStyle: { color: '#FF9900' },
          label: {
            show: true,
            position: 'inside',
          },
        },
        {
          name: 'Azure',
          type: 'bar',
          stack: 'total',
          data: [11, 11, 9, 1, 1, 1, 0],
          itemStyle: { color: '#0078D4' },
          label: {
            show: true,
            position: 'inside',
          },
        },
        {
          name: 'Google Cloud',
          type: 'bar',
          stack: 'total',
          data: [10, 12, 7, 1, 1, 1, 0],
          itemStyle: { color: '#34A853' },
          label: {
            show: true,
            position: 'inside',
          },
        },
        {
          name: '华为云',
          type: 'bar',
          stack: 'total',
          data: [12, 4, 9, 1, 1, 1, 1],
          itemStyle: { color: '#D0021B' },
          label: {
            show: true,
            position: 'inside',
          },
        },
        {
          name: '腾讯云',
          type: 'bar',
          stack: 'total',
          data: [14, 6, 5, 1, 1, 1, 0],
          itemStyle: { color: '#9C27B0' },
          label: {
            show: true,
            position: 'inside',
          },
        },
        {
          name: '火山引擎',
          type: 'bar',
          stack: 'total',
          data: [12, 3, 3, 1, 1, 1, 0],
          itemStyle: { color: '#00BCD4' },
          label: {
            show: true,
            position: 'inside',
          },
        },
        {
          name: '甲骨文云',
          type: 'bar',
          stack: 'total',
          data: [8, 0, 4, 1, 1, 1, 0],
          itemStyle: { color: '#C74634' },
          label: {
            show: true,
            position: 'inside',
          },
        },
        {
          name: 'IBM 云',
          type: 'bar',
          stack: 'total',
          data: [0, 0, 0, 0, 0, 0, 0],
          itemStyle: { color: '#FFC107' },
          label: {
            show: true,
            position: 'inside',
          },
        },
        {
          name: 'OVH 云',
          type: 'bar',
          stack: 'total',
          data: [0, 0, 0, 0, 0, 0, 0],
          itemStyle: { color: '#607D8B' },
          label: {
            show: true,
            position: 'inside',
          },
        },
        {
          name: 'DigitalOcean',
          type: 'bar',
          stack: 'total',
          data: [3, 0, 4, 1, 1, 1, 0],
          itemStyle: { color: '#E91E63' },
          label: {
            show: true,
            position: 'inside',
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

