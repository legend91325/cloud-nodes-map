'use client';

import { Analytics as VercelAnalyticsComponent } from '@vercel/analytics/react';
import { SpeedInsights } from '@vercel/speed-insights/react';

/**
 * Vercel Analytics 组件
 * 提供 Web Analytics 和 Speed Insights
 * 
 * 注意：需要在 Vercel Dashboard 中启用 Analytics
 * Settings → Analytics → Enable Web Analytics
 */
export default function VercelAnalytics() {
  return (
    <>
      <VercelAnalyticsComponent />
      <SpeedInsights />
    </>
  );
}

