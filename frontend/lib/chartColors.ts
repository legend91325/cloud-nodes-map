/**
 * 图表颜色配置
 * 基于设计规范中的色系系统
 */

// 云服务商配色（与设计规范中的 color_scheme.palette 保持一致）
export const providerColors: Record<string, string> = {
  'alibaba_cloud': '#FF6A00',      // 阿里云 - 橙红
  'aws': '#FF9900',                 // AWS - 橙色
  'azure': '#0078D4',               // Azure - 蓝色
  'google_cloud': '#34A853',        // Google Cloud - 绿色（图表专用，区别于品牌色）
  'tencent_cloud': '#9C27B0',       // 腾讯云 - 紫色
  'huawei_cloud': '#D0021B',        // 华为云 - 红色
  'volcano_engine': '#00BCD4',      // 火山引擎 - 青色
  'oracle_cloud': '#C74634',        // Oracle Cloud - 红棕
  'ibm_cloud': '#FFC107',           // IBM Cloud - 金色
  'ovh_cloud': '#607D8B',           // OVH Cloud - 蓝灰
  'digitalocean': '#E91E63',        // DigitalOcean - 粉红
};

// 云服务商中文名称映射
export const providerNameMap: Record<string, string> = {
  'alibaba_cloud': '阿里云',
  'aws': 'AWS',
  'azure': 'Azure',
  'google_cloud': 'Google Cloud',
  'tencent_cloud': '腾讯云',
  'huawei_cloud': '华为云',
  'volcano_engine': '火山引擎',
  'oracle_cloud': '甲骨文云',
  'ibm_cloud': 'IBM 云',
  'ovh_cloud': 'OVH 云',
  'digitalocean': 'DigitalOcean',
};

// 图表通用样式配置（基于设计规范）
export const chartTheme = {
  // 主色系 (Google Cloud Blue)
  primary: {
    50: '#E8F0FE',
    100: '#D2E3FC',
    500: '#4285F4',
    600: '#1A73E8',
    700: '#1967D2',
  },
  // 中性色 (Google Material Gray)
  neutral: {
    50: '#F8F9FA',
    100: '#F1F3F4',
    200: '#E8EAED',
    300: '#DADCE0',
    500: '#5F6368',
    700: '#3C4043',
    900: '#202124',
  },
  // 图表背景
  backgroundColor: 'transparent',
  // 网格线颜色
  gridLineColor: '#DADCE0', // neutral-300 (Google Material Gray)
  // 坐标轴文字颜色
  axisTextColor: '#3C4043', // neutral-700 (Google Material Gray)
  // 标题文字颜色
  titleTextColor: '#202124', // neutral-900 (Google Material Gray)
  // Tooltip 样式
  tooltip: {
    backgroundColor: 'rgba(32, 33, 36, 0.9)', // neutral-900 with opacity (Google Material Gray)
    borderColor: 'transparent',
    textColor: '#FFFFFF',
  },
};

// 获取云服务商颜色
export function getProviderColor(providerId: string): string {
  return providerColors[providerId] || chartTheme.primary[600];
}

// 获取云服务商中文名称
export function getProviderName(providerId: string): string {
  return providerNameMap[providerId] || providerId;
}

// 图表系列顺序（按节点数量排序）
export const providerOrder = [
  'google_cloud',
  'azure',
  'alibaba_cloud',
  'aws',
  'oracle_cloud',
  'tencent_cloud',
  'huawei_cloud',
  'volcano_engine',
  'ibm_cloud',
  'digitalocean',
  'ovh_cloud',
];

