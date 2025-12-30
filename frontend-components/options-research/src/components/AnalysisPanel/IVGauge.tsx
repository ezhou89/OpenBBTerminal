import { useEffect, useState } from "react";
import { motion } from "framer-motion";

interface IVGaugeProps {
  value: number; // 0-100
  environment: "very_low" | "low" | "neutral" | "elevated" | "very_high";
  atm_iv: number | null;
}

const environmentLabels = {
  very_low: "Very Cheap",
  low: "Cheap",
  neutral: "Average",
  elevated: "Expensive",
  very_high: "Very Expensive",
};

const environmentColors = {
  very_low: "#22c55e",
  low: "#84cc16",
  neutral: "#eab308",
  elevated: "#f97316",
  very_high: "#ef4444",
};

export default function IVGauge({ value, environment, atm_iv }: IVGaugeProps) {
  const [animatedValue, setAnimatedValue] = useState(0);

  useEffect(() => {
    // Animate the value on mount
    const timer = setTimeout(() => setAnimatedValue(value), 100);
    return () => clearTimeout(timer);
  }, [value]);

  // SVG arc calculations
  const radius = 60;
  const strokeWidth = 10;
  const circumference = Math.PI * radius; // Half circle
  const progress = (animatedValue / 100) * circumference;

  return (
    <div className="flex flex-col items-center">
      {/* Gauge SVG */}
      <svg width="160" height="100" viewBox="0 0 160 100" className="mb-2">
        {/* Background arc */}
        <path
          d="M 20 90 A 60 60 0 0 1 140 90"
          fill="none"
          stroke="currentColor"
          strokeWidth={strokeWidth}
          className="text-grey-700"
        />

        {/* Gradient definition */}
        <defs>
          <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#22c55e" />
            <stop offset="50%" stopColor="#eab308" />
            <stop offset="100%" stopColor="#ef4444" />
          </linearGradient>
        </defs>

        {/* Progress arc */}
        <motion.path
          d="M 20 90 A 60 60 0 0 1 140 90"
          fill="none"
          stroke="url(#gaugeGradient)"
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: circumference - progress }}
          transition={{ duration: 1, ease: "easeOut" }}
        />

        {/* Needle */}
        <motion.g
          initial={{ rotate: -90 }}
          animate={{ rotate: -90 + (animatedValue / 100) * 180 }}
          transition={{ duration: 1, ease: "easeOut" }}
          style={{ transformOrigin: "80px 90px" }}
        >
          <line
            x1="80"
            y1="90"
            x2="80"
            y2="40"
            stroke="white"
            strokeWidth="2"
          />
          <circle cx="80" cy="90" r="6" fill="white" />
        </motion.g>

        {/* Labels */}
        <text x="15" y="98" className="fill-grey-500 text-[10px]">
          0
        </text>
        <text x="76" y="20" className="fill-grey-400 text-[10px]">
          50
        </text>
        <text x="135" y="98" className="fill-grey-500 text-[10px]">
          100
        </text>
      </svg>

      {/* Value and Label */}
      <div className="text-center">
        <div
          className="text-2xl font-bold"
          style={{ color: environmentColors[environment] }}
        >
          {value.toFixed(0)}%
        </div>
        <div
          className="text-sm font-medium"
          style={{ color: environmentColors[environment] }}
        >
          {environmentLabels[environment]}
        </div>
        {atm_iv !== null && (
          <div className="text-xs text-grey-500 mt-1">
            ATM IV: {(atm_iv * 100).toFixed(1)}%
          </div>
        )}
      </div>
    </div>
  );
}
