import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          950: "#070B14",
          900: "#0B1120",
          850: "#0F172A",
          800: "#131E35",
          700: "#1E293B",
          600: "#334155",
        },
        brand: {
          teal: "#0D9488",
          tealLight: "#14B8A6",
          tealDark: "#0F766E",
          emerald: "#10B981",
        },
        risk: {
          high: "#EF4444",
          medium: "#F59E0B",
          low: "#10B981",
        }
      },
    },
  },
  plugins: [],
};
export default config;
