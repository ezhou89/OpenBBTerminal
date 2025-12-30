/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      screens: {
        smh: { raw: "(max-height: 450px)" },
        mdl: { raw: "(min-width: 890px)" },
      },
      colors: {
        // OpenBB greys (nested for theme() function)
        grey: {
          50: "#f6f6f6ff",
          100: "#eaeaeaff",
          200: "#dcdcdcff",
          300: "#c8c8c8ff",
          400: "#a2a2a2ff",
          500: "#808080ff",
          600: "#5a5a5aff",
          700: "#474747ff",
          800: "#2a2a2aff",
          850: "#131313ff",
          900: "#070707ff",
        },
        // OpenBB burgundy
        burgundy: {
          300: "#B47DA0",
          400: "#9B5181",
          500: "#822661",
          900: "#340F27",
        },
        // Options Research colors
        iv: {
          cheap: "#22c55e",
          neutral: "#eab308",
          expensive: "#ef4444",
        },
        catalyst: {
          far: "#22c55e",
          near: "#f97316",
          imminent: "#ef4444",
        },
        // Accent
        accent: {
          cyan: "#06b6d4",
          purple: "#a855f7",
        },
      },
      fontFamily: {
        mono: ["JetBrains Mono", "SF Mono", "Monaco", "monospace"],
        display: ["Inter", "system-ui", "sans-serif"],
      },
      animation: {
        "gauge-fill": "gauge-fill 1s ease-out forwards",
        "slide-up": "slide-up 0.3s ease-out",
        "fade-in": "fade-in 0.3s ease-out",
      },
      keyframes: {
        "gauge-fill": {
          "0%": { strokeDashoffset: "100" },
          "100%": { strokeDashoffset: "var(--gauge-value)" },
        },
        "slide-up": {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "fade-in": {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
      },
    },
  },
  plugins: [],
};
