'use client';

import { useEffect, useRef, useState } from 'react';
import * as echarts from 'echarts';
import { CloudNode, ProviderMetadata } from '@/types';
import { getAvailabilityZoneCount } from '@/lib/data';
import { chartTheme } from '@/lib/chartColors';

interface MapChartProps {
  nodes: CloudNode[];
  providers: ProviderMetadata['providers'];
  selectedProviders?: string[];
}

// 加载世界地图数据
async function loadWorldMap() {
  // 检查是否已经注册
  if (echarts.getMap('world')) {
    return true;
  }

  try {
    // 使用 ECharts 4.x 的地图数据（兼容性好）
    const response = await fetch('https://cdn.jsdelivr.net/npm/echarts@4.9.0/map/json/world.json', {
      mode: 'cors',
    });
    
    if (response.ok) {
      const mapData = await response.json();
      if (mapData && (mapData.type === 'FeatureCollection' || mapData.features || mapData.geoJSON)) {
        echarts.registerMap('world', mapData);
        return true;
      }
    }
  } catch (error) {
    console.warn('Primary map source failed, trying alternatives:', error);
  }

  // 备用方案：使用 GitHub 上的地图数据
  try {
    const response = await fetch('https://raw.githubusercontent.com/apache/echarts/master/map/json/world.json', {
      mode: 'cors',
    });
    
    if (response.ok) {
      const mapData = await response.json();
      if (mapData && (mapData.type === 'FeatureCollection' || mapData.features)) {
        echarts.registerMap('world', mapData);
        return true;
      }
    }
  } catch (error) {
    console.warn('GitHub source also failed:', error);
  }

  // 如果都失败，返回 false，但图表仍可使用地理坐标系显示散点
  return false;
}

export default function MapChart({ nodes, providers, selectedProviders }: MapChartProps) {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);
  const [mapLoaded, setMapLoaded] = useState(false);
  const [loading, setLoading] = useState(true);
  
  // 初始地图状态
  const initialZoom = 1.2;
  const initialCenter: [number, number] = [0, 20];

  useEffect(() => {
    // 加载世界地图
    loadWorldMap().then((success) => {
      setMapLoaded(success);
      setLoading(false);
    });
  }, []);

  useEffect(() => {
    if (!chartRef.current || loading) return;

    // 初始化图表
    if (!chartInstance.current) {
      chartInstance.current = echarts.init(chartRef.current);
    }

    const chart = chartInstance.current;

    // 过滤节点
    const filteredNodes = selectedProviders && selectedProviders.length > 0
      ? nodes.filter(node => selectedProviders.includes(node.provider))
      : nodes;

    // 按提供商分组
    const providerGroups: Record<string, CloudNode[]> = {};
    filteredNodes.forEach(node => {
      if (!providerGroups[node.provider]) {
        providerGroups[node.provider] = [];
      }
      providerGroups[node.provider].push(node);
    });

    // 创建系列数据
    const series = Object.entries(providerGroups).map(([providerId, providerNodes]) => {
      const provider = providers[providerId];
      if (!provider) return null;

      const data = providerNodes.map(node => {
        const azCount = getAvailabilityZoneCount(node);
        return {
          name: node.name,
          value: [
            node.location.longitude,
            node.location.latitude,
            azCount,
            node.location.country,
            node.location.city,
            node.launch_date,
          ],
          provider: providerId,
          nodeId: node.node_id,
          status: node.status,
        };
      }).filter(Boolean);

      return {
        name: provider.name,
        type: 'scatter',
        coordinateSystem: 'geo',
        data,
        symbolSize: (val: number[]) => Math.max(8, Math.min(20, val[2] * 2)),
        itemStyle: {
          color: provider.color,
          shadowBlur: 10,
          shadowColor: provider.color,
        },
        emphasis: {
          itemStyle: {
            borderColor: '#fff',
            borderWidth: 2,
            shadowBlur: 20,
            shadowColor: provider.color,
          },
        },
      };
    }).filter(Boolean);

    const option: echarts.EChartsOption = {
      backgroundColor: chartTheme.backgroundColor,
      geo: {
        map: 'world',
        roam: true,
        zoom: initialZoom,
        center: initialCenter,
        scaleLimit: {
          min: initialZoom, // 设置最小缩放级别，防止缩放到更小
          max: 5, // 设置最大缩放级别
        },
        itemStyle: {
          areaColor: chartTheme.neutral[100], // #F1F3F4 (Google Material Gray)
          borderColor: chartTheme.neutral[300], // #DADCE0 (Google Material Gray)
          borderWidth: 0.5,
        },
        emphasis: {
          itemStyle: {
            areaColor: chartTheme.neutral[200], // #E8EAED (Google Material Gray)
          },
        },
        silent: false,
      },
      series: series as any,
      tooltip: {
        trigger: 'item',
        backgroundColor: chartTheme.tooltip.backgroundColor,
        borderColor: chartTheme.tooltip.borderColor,
        textStyle: {
          color: chartTheme.tooltip.textColor,
        },
        formatter: (params: any) => {
          if (params.seriesType === 'scatter') {
            const data = params.data.value;
            const provider = providers[params.data.provider];
            return `
              <div style="padding: 8px;">
                <div style="font-weight: bold; margin-bottom: 4px; color: ${provider?.color}">
                  ${params.data.name}
                </div>
                <div style="font-size: 12px; line-height: 1.6;">
                  <div>提供商: ${provider?.name}</div>
                  <div>国家: ${data[3]}</div>
                  <div>城市: ${data[4]}</div>
                  <div>可用区: ${data[2]} 个</div>
                  ${data[5] ? `<div>上线时间: ${new Date(data[5]).toLocaleDateString('zh-CN')}</div>` : ''}
                </div>
              </div>
            `;
          }
          return params.name;
        },
      },
      legend: {
        show: true,
        orient: 'horizontal',
        left: 'center',
        bottom: 10,
        data: series.map((s: any) => s?.name).filter(Boolean),
        textStyle: {
          color: chartTheme.axisTextColor,
        },
      },
      animation: true,
      animationDuration: 2000,
      animationEasing: 'cubicOut',
    };

    chart.setOption(option);

    // 响应式调整
    const handleResize = () => {
      chart.resize();
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, [nodes, providers, selectedProviders, mapLoaded, loading]);

  if (loading) {
    return (
      <div className="w-full h-[600px] rounded-xl overflow-hidden shadow-lg bg-white flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mb-2"></div>
          <p className="text-neutral-500 text-sm">加载地图中...</p>
        </div>
      </div>
    );
  }

  // 重置地图视图
  const handleReset = () => {
    if (chartInstance.current) {
      // 使用 setOption 重置 geo 配置
      chartInstance.current.setOption({
        geo: {
          zoom: initialZoom,
          center: initialCenter,
        },
      }, false); // false 表示不合并，直接替换
    }
  };

  return (
    <div className="w-full h-[600px] rounded-lg overflow-hidden shadow-sm border border-neutral-200 bg-white relative">
      <div ref={chartRef} className="w-full h-full" />
      {/* 重置按钮 */}
      <button
        onClick={handleReset}
        className="absolute top-4 right-4 z-10 px-4 py-2 bg-white border border-neutral-300 rounded-md shadow-sm hover:bg-neutral-50 hover:border-primary-500 transition-colors text-sm font-medium text-neutral-700 hover:text-primary-600 flex items-center gap-2"
        aria-label="重置地图视图"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-4 w-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
          />
        </svg>
        <span>重置视图</span>
      </button>
    </div>
  );
}
