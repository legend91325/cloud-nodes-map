'use client';

import { useEffect, useRef, useState } from 'react';
import * as echarts from 'echarts';
import { CloudNode, ProviderMetadata } from '@/types';
import { getAvailabilityZoneCount } from '@/lib/data';

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
            node.network_info.latency,
            node.network_info.uptime,
            node.location.country,
            node.location.city,
            node.data_center,
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
      backgroundColor: 'transparent',
      geo: {
        map: 'world',
        roam: true,
        zoom: 1.2,
        center: [0, 20],
        itemStyle: {
          areaColor: '#f0f2f5',
          borderColor: '#d0d7de',
          borderWidth: 0.5,
        },
        emphasis: {
          itemStyle: {
            areaColor: '#e0e4e8',
          },
        },
        silent: false,
      },
      series: series as any,
      tooltip: {
        trigger: 'item',
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        borderColor: 'transparent',
        textStyle: {
          color: '#fff',
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
                  <div>国家: ${data[5]}</div>
                  <div>城市: ${data[6]}</div>
                  <div>可用区: ${data[2]} 个</div>
                  <div>延迟: ${data[3]}ms</div>
                  <div>可用性: ${data[4]}%</div>
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
          color: '#666',
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
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mb-2"></div>
          <p className="text-gray-600 text-sm">加载地图中...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full h-[600px] rounded-xl overflow-hidden shadow-lg bg-white">
      <div ref={chartRef} className="w-full h-full" />
    </div>
  );
}
