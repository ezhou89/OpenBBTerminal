import { motion } from "framer-motion";

type StrategyFilterType = "all" | "buy" | "sell";

interface StrategyFilterProps {
  value: StrategyFilterType;
  onChange: (value: StrategyFilterType) => void;
}

const options: { id: StrategyFilterType; label: string; icon: string }[] = [
  { id: "all", label: "All Strategies", icon: "🎯" },
  { id: "buy", label: "Buy Premium", icon: "📈" },
  { id: "sell", label: "Sell Premium", icon: "📉" },
];

export default function StrategyFilter({ value, onChange }: StrategyFilterProps) {
  return (
    <div className="mb-4">
      <label className="text-sm font-medium text-grey-300 mb-3 block">
        Strategy Type
      </label>
      <div className="flex gap-2">
        {options.map((option) => (
          <motion.button
            key={option.id}
            onClick={() => onChange(option.id)}
            className={`flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-all ${
              value === option.id
                ? "bg-burgundy-600 text-white"
                : "bg-grey-800 text-grey-400 hover:bg-grey-700"
            }`}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <span className="mr-1">{option.icon}</span>
            {option.label}
          </motion.button>
        ))}
      </div>
    </div>
  );
}
