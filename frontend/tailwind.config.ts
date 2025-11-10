import type { Config } from "tailwindcss";

/**
 * 云服务商测评网站色系配置
 * 参考 Google Cloud 设计风格 - Material Design
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
        // ========== 主色 (Primary) - Google Cloud Blue ==========
        primary: {
          50: "#E8F0FE",
          100: "#D2E3FC",
          500: "#4285F4",  // Google Blue
          600: "#1A73E8",  // Deep Blue
          700: "#1967D2",  // Deeper Blue
        },
        // ========== 辅助色 (Secondary) - Google Material Colors ==========
        success: {
          50: "#E6F4EA",
          500: "#34A853",  // Google Green
        },
        warning: {
          50: "#FEF7E0",
          500: "#FBBC05",  // Google Yellow
        },
        error: {
          50: "#FCE8E6",
          500: "#EA4335",  // Google Red
        },
        info: {
          50: "#E8F0FE",  // Same as Primary-50
          500: "#4285F4",  // Same as Primary-500
        },
        // ========== 中性色 (Neutral) - Google Material Gray ==========
        neutral: {
          50: "#F8F9FA",
          100: "#F1F3F4",
          200: "#E8EAED",
          300: "#DADCE0",
          500: "#5F6368",
          700: "#3C4043",
          900: "#202124",
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

