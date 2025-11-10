'use client';

import { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import { chartTheme } from '@/lib/chartColors';
import { createGrowthTrendSeries } from '@/lib/chartData';

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
      backgroundColor: chartTheme.backgroundColor,
      title: {
        text: '云服务商 节点逐年增长趋势',
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
          type: 'cross',
        },
        backgroundColor: chartTheme.tooltip.backgroundColor,
        borderColor: chartTheme.tooltip.borderColor,
        textStyle: {
          color: chartTheme.tooltip.textColor,
        },
      },
      legend: {
        data: createGrowthTrendSeries().map(s => s.name),
        bottom: 10,
        type: 'scroll',
        textStyle: {
          color: chartTheme.axisTextColor,
        },
      },
      grid: {
        left: '3%',
        right: '8%', // 增加右侧空间以显示标签
        bottom: '15%',
        containLabel: true,
        borderColor: chartTheme.gridLineColor,
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
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
        min: 0,
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
      series: createGrowthTrendSeries(),
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

