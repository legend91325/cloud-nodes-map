import type { Config } from "tailwindcss";

/**
 * 云服务商测评网站色系配置
 * 基于专业、清晰、可信赖的设计理念
 */
const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // ========== 主色 (Primary) ==========
        primary: {
          50: "#EEF2FF",
          500: "#6366F1",
          600: "#4F46E5",
          700: "#4338CA",
        },
        // ========== 辅助色 (Secondary) ==========
        success: {
          50: "#ECFDF5",
          600: "#10B981",
        },
        warning: {
          50: "#FFFBEB",
          500: "#F59E0B",
        },
        error: {
          50: "#FEF2F2",
          600: "#DC2626",
        },
        info: {
          50: "#EFF6FF",
          500: "#3B82F6",
        },
        // ========== 中性色 (Neutral) ==========
        neutral: {
          50: "#F9FAFB",
          100: "#F3F4F6",
          300: "#D1D5DB",
          500: "#6B7280",
          700: "#374151",
          900: "#111827",
        },
        // ========== 云服务商配色 (Data Visualization) ==========
        provider: {
          aws: "#FF9900",
          azure: "#0078D4",
          "google-cloud": "#4285F4",
          "alibaba-cloud": "#FF6A00",
          "tencent-cloud": "#9C27B0",
          "huawei-cloud": "#D0021B",
          "volcano-engine": "#00BCD4",
          "oracle-cloud": "#C74634",
          "ibm-cloud": "#FFC107",
          "ovh-cloud": "#607D8B",
          digitalocean: "#E91E63",
        },
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;

