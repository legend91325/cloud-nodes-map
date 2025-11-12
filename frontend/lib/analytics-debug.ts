/**
 * Analytics 调试工具
 * 用于本地开发环境验证和调试 Analytics 功能
 */

declare global {
  interface Window {
    gtag?: (...args: any[]) => void;
    dataLayer?: any[];
    __ANALYTICS_DEBUG__?: boolean;
  }
}

/**
 * 启用 Analytics 调试模式
 * 在浏览器控制台输出所有 Analytics 事件
 */
export function enableAnalyticsDebug() {
  if (typeof window === 'undefined') return;

  window.__ANALYTICS_DEBUG__ = true;

  // 拦截 gtag 调用
  if (window.gtag) {
    const originalGtag = window.gtag;
    window.gtag = function (...args: any[]) {
      console.group('🔍 [Analytics Debug]');
      console.log('Event:', args[0]);
      console.log('Parameters:', args.slice(1));
      console.trace('Call Stack');
      console.groupEnd();
      return originalGtag.apply(window, args);
    };
  }

  // 监听 dataLayer 变化
  if (window.dataLayer) {
    const originalPush = window.dataLayer.push;
    window.dataLayer.push = function (...args: any[]) {
      console.group('📊 [DataLayer Debug]');
      console.log('Data:', args);
      console.trace('Call Stack');
      console.groupEnd();
      return originalPush.apply(window.dataLayer!, args);
    };
  }

  console.log('✅ Analytics Debug Mode Enabled');
  console.log('All Analytics events will be logged to console');
}

/**
 * 检查 Analytics 是否已加载
 */
export function checkAnalyticsStatus() {
  if (typeof window === 'undefined') {
    console.warn('⚠️ Analytics check: window is undefined (SSR)');
    return false;
  }

  const status = {
    gtag: typeof window.gtag === 'function',
    dataLayer: Array.isArray(window.dataLayer),
    gaId: process.env.NEXT_PUBLIC_GA_ID || 'Not configured',
  };

  console.group('📊 Analytics Status');
  console.log('gtag loaded:', status.gtag ? '✅' : '❌');
  console.log('dataLayer loaded:', status.dataLayer ? '✅' : '❌');
  console.log('GA ID:', status.gaId);
  console.log('Debug mode:', window.__ANALYTICS_DEBUG__ ? '✅ Enabled' : '❌ Disabled');
  console.groupEnd();

  return status.gtag && status.dataLayer;
}

/**
 * 测试发送 Analytics 事件
 */
export function testAnalyticsEvent() {
  if (typeof window === 'undefined' || !window.gtag) {
    console.error('❌ Analytics not loaded. Make sure GA ID is configured.');
    return;
  }

  const testEvent = {
    event_category: 'Test',
    event_label: 'Local Development Test',
    value: 1,
  };

  console.log('🧪 Testing Analytics event...');
  window.gtag('event', 'test_event', testEvent);
  console.log('✅ Test event sent:', testEvent);
}

/**
 * 显示 Analytics 调试面板（在控制台）
 */
export function showAnalyticsDebugPanel() {
  if (typeof window === 'undefined') return;

  console.log(`
╔═══════════════════════════════════════════════════════════════════╗
║              Analytics 调试面板                                   ║
╚═══════════════════════════════════════════════════════════════════╝

📊 当前状态:
  - GA ID: ${process.env.NEXT_PUBLIC_GA_ID || '❌ 未配置'}
  - gtag: ${typeof window.gtag === 'function' ? '✅ 已加载' : '❌ 未加载'}
  - dataLayer: ${Array.isArray(window.dataLayer) ? '✅ 已加载' : '❌ 未加载'}
  - Debug Mode: ${window.__ANALYTICS_DEBUG__ ? '✅ 已启用' : '❌ 未启用'}

🔧 可用命令:
  - window.__enableAnalyticsDebug() - 启用调试模式
  - window.__checkAnalyticsStatus() - 检查状态
  - window.__testAnalyticsEvent() - 发送测试事件

💡 提示:
  - 在本地开发时，确保设置了 NEXT_PUBLIC_GA_ID 环境变量
  - 使用 Google Analytics DebugView 查看实时事件
  - 访问: https://analytics.google.com → 管理 → DebugView

═══════════════════════════════════════════════════════════════════
  `);

  // 将函数挂载到 window 对象，方便在控制台调用
  (window as any).__enableAnalyticsDebug = enableAnalyticsDebug;
  (window as any).__checkAnalyticsStatus = checkAnalyticsStatus;
  (window as any).__testAnalyticsEvent = testAnalyticsEvent;
}

