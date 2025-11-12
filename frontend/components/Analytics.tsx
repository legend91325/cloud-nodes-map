'use client';

import { useEffect } from 'react';
import Script from 'next/script';

declare global {
  interface Window {
    gtag?: (...args: any[]) => void;
    dataLayer?: any[];
    __ANALYTICS_DEBUG__?: boolean;
  }
}

interface AnalyticsProps {
  gaId?: string;
}

/**
 * Google Analytics 4 组件
 * 使用 Next.js Script 组件优化加载
 * 支持开发模式调试
 */
export default function Analytics({ gaId }: AnalyticsProps) {
  const isDebug = process.env.NEXT_PUBLIC_ANALYTICS_DEBUG === 'true';
  const isDev = process.env.NODE_ENV === 'development';

  // 开发模式下，如果没有 GA ID，仍然初始化调试功能
  useEffect(() => {
    if (isDev && (isDebug || !gaId)) {
      // 在开发模式下，即使没有 GA ID，也初始化调试工具
      if (typeof window !== 'undefined') {
        import('@/lib/analytics-debug').then(({ showAnalyticsDebugPanel, enableAnalyticsDebug }) => {
          showAnalyticsDebugPanel();
          if (isDebug) {
            enableAnalyticsDebug();
          }
        });
      }
    }
  }, [isDev, isDebug, gaId]);

  // 如果没有提供 GA ID，在开发模式下显示提示
  if (!gaId) {
    if (isDev) {
      return (
        <div className="fixed bottom-4 right-4 bg-warning-50 border border-warning-500 rounded-lg p-4 shadow-lg z-50 max-w-sm">
          <p className="text-sm font-medium text-warning-700 mb-1">
            ⚠️ Analytics 未配置
          </p>
          <p className="text-xs text-warning-600 mb-2">
            请在 <code className="bg-warning-100 px-1 rounded">.env.local</code> 中设置 <code className="bg-warning-100 px-1 rounded">NEXT_PUBLIC_GA_ID</code>
          </p>
          <p className="text-xs text-warning-600">
            打开控制台查看调试工具
          </p>
        </div>
      );
    }
    return null;
  }

  // 开发模式下，启用调试功能
  useEffect(() => {
    if (isDev && isDebug && typeof window !== 'undefined') {
      import('@/lib/analytics-debug').then(({ enableAnalyticsDebug }) => {
        // 等待 gtag 加载后再启用调试
        const checkGtag = setInterval(() => {
          if (window.gtag) {
            enableAnalyticsDebug();
            clearInterval(checkGtag);
          }
        }, 100);

        // 10秒后停止检查
        setTimeout(() => clearInterval(checkGtag), 10000);
      });
    }
  }, [isDev, isDebug]);

  return (
    <>
      {/* Google Analytics 4 */}
      <Script
        strategy="afterInteractive"
        src={`https://www.googletagmanager.com/gtag/js?id=${gaId}`}
      />
      <Script
        id="google-analytics"
        strategy="afterInteractive"
        dangerouslySetInnerHTML={{
          __html: `
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '${gaId}', {
              page_path: window.location.pathname,
              ${isDev ? 'debug_mode: true,' : ''}
            });
          `,
        }}
      />
    </>
  );
}

/**
 * 页面浏览追踪 Hook
 */
export function usePageView(path?: string) {
  useEffect(() => {
    if (typeof window !== 'undefined' && window.gtag) {
      window.gtag('config', process.env.NEXT_PUBLIC_GA_ID || '', {
        page_path: path || window.location.pathname,
      });
    }
  }, [path]);
}

/**
 * 自定义事件追踪
 */
export function trackEvent(
  action: string,
  category: string,
  label?: string,
  value?: number
) {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', action, {
      event_category: category,
      event_label: label,
      value: value,
    });
  }
}

/**
 * 节点查看事件
 */
export function trackNodeView(provider: string, nodeId: string) {
  trackEvent('view_node', 'Node', `${provider}-${nodeId}`);
}

/**
 * 图表交互事件
 */
export function trackChartInteraction(chartType: string, action: string) {
  trackEvent(action, 'Chart', chartType);
}

/**
 * 筛选操作事件
 */
export function trackFilter(provider?: string, continent?: string) {
  trackEvent('filter', 'Interaction', `${provider || 'all'}-${continent || 'all'}`);
}

