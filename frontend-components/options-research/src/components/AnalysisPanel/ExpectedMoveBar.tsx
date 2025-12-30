import { motion } from "framer-motion";

interface ExpectedMoveBarProps {
  currentPrice: number;
  expectedMoveDollars: number;
  expectedMovePercent: number;
  range: [number, number];
}

export default function ExpectedMoveBar({
  currentPrice,
  expectedMoveDollars,
  expectedMovePercent,
  range,
}: ExpectedMoveBarProps) {
  const [lowPrice, highPrice] = range;
  const totalRange = highPrice - lowPrice;

  // Calculate current price position as percentage of range
  const currentPosition = ((currentPrice - lowPrice) / totalRange) * 100;

  return (
    <div className="w-full">
      {/* Label */}
      <div className="flex justify-between items-center mb-3">
        <span className="text-grey-400 text-sm">Expected Move</span>
        <span className="text-white font-medium">
          ±${expectedMoveDollars.toFixed(2)} ({expectedMovePercent.toFixed(1)}%)
        </span>
      </div>

      {/* Price Range Bar */}
      <div className="relative h-12 mb-2">
        {/* Background bar */}
        <div className="absolute inset-x-0 top-1/2 -translate-y-1/2 h-3 bg-grey-800 rounded-full overflow-hidden">
          {/* Gradient fill representing range */}
          <motion.div
            className="absolute inset-0 opacity-60"
            style={{
              background: "linear-gradient(90deg, #ef4444 0%, #22c55e 50%, #ef4444 100%)",
            }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.6 }}
            transition={{ duration: 0.5 }}
          />
        </div>

        {/* Low price marker */}
        <motion.div
          className="absolute top-1/2 -translate-y-1/2 flex flex-col items-center"
          style={{ left: "0%" }}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <div className="w-0.5 h-5 bg-red-500" />
          <span className="text-xs text-grey-400 mt-1">${lowPrice.toFixed(2)}</span>
        </motion.div>

        {/* Current price marker */}
        <motion.div
          className="absolute top-1/2 -translate-y-1/2 flex flex-col items-center z-10"
          style={{ left: `${currentPosition}%` }}
          initial={{ opacity: 0, scale: 0 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4, type: "spring", stiffness: 200 }}
        >
          <div className="w-4 h-4 bg-white rounded-full shadow-lg border-2 border-grey-900" />
          <div className="absolute top-6 whitespace-nowrap">
            <span className="text-sm font-bold text-white">${currentPrice.toFixed(2)}</span>
          </div>
        </motion.div>

        {/* High price marker */}
        <motion.div
          className="absolute top-1/2 -translate-y-1/2 flex flex-col items-center"
          style={{ left: "100%" }}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <div className="w-0.5 h-5 bg-red-500" />
          <span className="text-xs text-grey-400 mt-1">${highPrice.toFixed(2)}</span>
        </motion.div>

        {/* Range arrows */}
        <motion.div
          className="absolute top-1/2 -translate-y-1/2 w-full flex justify-between px-4 pointer-events-none"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
        >
          <svg className="w-4 h-4 text-grey-500" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          <svg className="w-4 h-4 text-grey-500" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </motion.div>
      </div>

      {/* Percentage labels */}
      <div className="flex justify-between text-xs text-grey-500">
        <span>-{expectedMovePercent.toFixed(1)}%</span>
        <span className="text-grey-400">1 Std Dev Range</span>
        <span>+{expectedMovePercent.toFixed(1)}%</span>
      </div>
    </div>
  );
}
