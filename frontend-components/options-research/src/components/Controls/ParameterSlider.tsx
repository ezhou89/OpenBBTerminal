import { motion } from "framer-motion";

interface ParameterSliderProps {
  label: string;
  value: number;
  min: number;
  max: number;
  step?: number;
  unit?: string;
  description?: string;
  onChange: (value: number) => void;
}

export default function ParameterSlider({
  label,
  value,
  min,
  max,
  step = 1,
  unit = "",
  description,
  onChange,
}: ParameterSliderProps) {
  const percentage = ((value - min) / (max - min)) * 100;

  return (
    <div className="mb-4">
      <div className="flex justify-between items-center mb-2">
        <label className="text-sm font-medium text-grey-300">{label}</label>
        <span className="text-sm font-mono text-burgundy-400">
          {value}
          {unit}
        </span>
      </div>

      <div className="relative">
        {/* Track background */}
        <div className="absolute inset-0 h-2 bg-grey-700 rounded-full top-1/2 -translate-y-1/2" />

        {/* Filled track */}
        <motion.div
          className="absolute h-2 bg-gradient-to-r from-burgundy-600 to-burgundy-400 rounded-full top-1/2 -translate-y-1/2"
          style={{ width: `${percentage}%` }}
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.2 }}
        />

        {/* Input */}
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="relative w-full h-6 appearance-none bg-transparent cursor-pointer z-10
            [&::-webkit-slider-thumb]:appearance-none
            [&::-webkit-slider-thumb]:w-4
            [&::-webkit-slider-thumb]:h-4
            [&::-webkit-slider-thumb]:rounded-full
            [&::-webkit-slider-thumb]:bg-white
            [&::-webkit-slider-thumb]:border-2
            [&::-webkit-slider-thumb]:border-burgundy-500
            [&::-webkit-slider-thumb]:shadow-lg
            [&::-webkit-slider-thumb]:cursor-pointer
            [&::-webkit-slider-thumb]:transition-transform
            [&::-webkit-slider-thumb]:hover:scale-110
            [&::-moz-range-thumb]:w-4
            [&::-moz-range-thumb]:h-4
            [&::-moz-range-thumb]:rounded-full
            [&::-moz-range-thumb]:bg-white
            [&::-moz-range-thumb]:border-2
            [&::-moz-range-thumb]:border-burgundy-500
            [&::-moz-range-thumb]:cursor-pointer"
        />
      </div>

      {/* Range labels */}
      <div className="flex justify-between text-xs text-grey-500 mt-1">
        <span>
          {min}
          {unit}
        </span>
        <span>
          {max}
          {unit}
        </span>
      </div>

      {description && (
        <p className="text-xs text-grey-500 mt-2">{description}</p>
      )}
    </div>
  );
}
