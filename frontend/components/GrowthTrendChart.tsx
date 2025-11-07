'use client';

import { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

interface GrowthTrendChartProps {
  className?: string;
}

export default function GrowthTrendChart({ className }: GrowthTrendChartProps) {
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
        text: '云服务商 节点逐年增长趋势',
        left: 'center',
        textStyle: {
          fontSize: 20,
          fontWeight: 'bold',
        },
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
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
        right: '8%', // 增加右侧空间以显示标签
        bottom: '15%',
        containLabel: true,
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
      },
      yAxis: {
        type: 'value',
        name: '节点数',
        min: 0,
        max: 40,
      },
      series: [
        {
          name: 'AWS',
          type: 'line',
          data: [1, 2, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 29],
          itemStyle: { color: '#FF9900' },
          symbol: 'circle',
          symbolSize: 6,
          label: {
            show: true,
            position: 'right',
            formatter: (params: any) => {
              if (params.dataIndex === 19) {
                return params.value.toString();
              }
              return '';
            },
            color: '#FF9900',
            fontSize: 12,
            fontWeight: 'bold',
          },
        },
        {
          name: 'Azure',
          type: 'line',
          data: [0, 0, 0, 0, 1, 3, 5, 7, 10, 13, 16, 19, 22, 26, 29, 32, 34, 35, 36, 36],
          itemStyle: { color: '#0078D4' },
          symbol: 'circle',
          symbolSize: 6,
          label: {
            show: true,
            position: 'right',
            formatter: (params: any) => {
              if (params.dataIndex === 19) {
                return params.value.toString();
              }
              return '';
            },
            color: '#0078D4',
            fontSize: 12,
            fontWeight: 'bold',
          },
        },
        {
          name: 'Google Cloud',
          type: 'line',
          data: [0, 0, 0, 0, 1, 2, 3, 4, 6, 8, 11, 14, 17, 20, 23, 26, 29, 32, 34, 34],
          itemStyle: { color: '#34A853' },
          symbol: 'circle',
          symbolSize: 6,
          label: {
            show: true,
            position: 'right',
            formatter: (params: any) => {
              if (params.dataIndex === 19) {
                return params.value.toString();
              }
              return '';
            },
            color: '#34A853',
            fontSize: 12,
            fontWeight: 'bold',
          },
        },
        {
          name: '阿里云',
          type: 'line',
          data: [0, 0, 0, 0, 0, 1, 2, 3, 5, 7, 9, 11, 14, 17, 20, 23, 26, 28, 29, 29],
          itemStyle: { color: '#FF6A00' },
          symbol: 'circle',
          symbolSize: 6,
          label: {
            show: true,
            position: 'right',
            formatter: (params: any) => {
              if (params.dataIndex === 19) {
                return params.value.toString();
              }
              return '';
            },
            color: '#FF6A00',
            fontSize: 12,
            fontWeight: 'bold',
          },
        },
        {
          name: '华为云',
          type: 'line',
          data: [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 4, 6, 9, 12, 15, 17, 18, 18, 18, 18],
          itemStyle: { color: '#D0021B' },
          symbol: 'circle',
          symbolSize: 6,
          label: {
            show: true,
            position: 'right',
            formatter: (params: any) => {
              if (params.dataIndex === 19) {
                return params.value.toString();
              }
              return '';
            },
            color: '#D0021B',
            fontSize: 12,
            fontWeight: 'bold',
          },
        },
        {
          name: '腾讯云',
          type: 'line',
          data: [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 5, 7, 9, 11, 13, 15, 16, 16, 16],
          itemStyle: { color: '#9C27B0' },
          symbol: 'circle',
          symbolSize: 6,
          label: {
            show: true,
            position: 'right',
            formatter: (params: any) => {
              if (params.dataIndex === 19) {
                return params.value.toString();
              }
              return '';
            },
            color: '#9C27B0',
            fontSize: 12,
            fontWeight: 'bold',
          },
        },
        {
          name: '火山引擎',
          type: 'line',
          data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 6, 9, 10, 10, 10],
          itemStyle: { color: '#00BCD4' },
          symbol: 'circle',
          symbolSize: 6,
          label: {
            show: true,
            position: 'right',
            formatter: (params: any) => {
              if (params.dataIndex === 19) {
                return params.value.toString();
              }
              return '';
            },
            color: '#00BCD4',
            fontSize: 12,
            fontWeight: 'bold',
          },
        },
        {
          name: '甲骨文云',
          type: 'line',
          data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8],
          itemStyle: { color: '#C74634' },
          symbol: 'circle',
          symbolSize: 6,
          label: {
            show: true,
            position: 'right',
            formatter: (params: any) => {
              if (params.dataIndex === 19) {
                return params.value.toString();
              }
              return '';
            },
            color: '#C74634',
            fontSize: 12,
            fontWeight: 'bold',
          },
        },
        {
          name: 'IBM 云',
          type: 'line',
          data: [0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 10, 10],
          itemStyle: { color: '#FFC107' },
          symbol: 'circle',
          symbolSize: 6,
          label: {
            show: true,
            position: 'right',
            formatter: (params: any) => {
              if (params.dataIndex === 19) {
                return params.value.toString();
              }
              return '';
            },
            color: '#FFC107',
            fontSize: 12,
            fontWeight: 'bold',
          },
        },
        {
          name: 'OVH 云',
          type: 'line',
          data: [0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8, 8, 8],
          itemStyle: { color: '#607D8B' },
          symbol: 'circle',
          symbolSize: 6,
          label: {
            show: true,
            position: 'right',
            formatter: (params: any) => {
              if (params.dataIndex === 19) {
                return params.value.toString();
              }
              return '';
            },
            color: '#607D8B',
            fontSize: 12,
            fontWeight: 'bold',
          },
        },
        {
          name: 'DigitalOcean',
          type: 'line',
          data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 6, 6, 6, 6],
          itemStyle: { color: '#E91E63' },
          symbol: 'circle',
          symbolSize: 6,
          label: {
            show: true,
            position: 'right',
            formatter: (params: any) => {
              if (params.dataIndex === 19) {
                return params.value.toString();
              }
              return '';
            },
            color: '#E91E63',
            fontSize: 12,
            fontWeight: 'bold',
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

