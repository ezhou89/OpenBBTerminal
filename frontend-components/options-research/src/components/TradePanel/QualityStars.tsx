import { motion } from "framer-motion";

interface QualityStarsProps {
  stars: 1 | 2 | 3 | 4 | 5;
  showLabel?: boolean;
}

const starLabels = {
  1: "Poor Setup",
  2: "Below Average",
  3: "Average Setup",
  4: "Good Setup",
  5: "Excellent Setup",
};

export default function QualityStars({ stars, showLabel = true }: QualityStarsProps) {
  return (
    <div className="flex items-center gap-2">
      <div className="flex gap-0.5">
        {[1, 2, 3, 4, 5].map((i) => (
          <motion.svg
            key={i}
            className={`w-5 h-5 ${i <= stars ? "text-yellow-400" : "text-grey-700"}`}
            fill="currentColor"
            viewBox="0 0 20 20"
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{
              delay: i * 0.1,
              type: "spring",
              stiffness: 300,
              damping: 15,
            }}
          >
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </motion.svg>
        ))}
      </div>
      {showLabel && (
        <motion.span
          className="text-grey-400 text-sm"
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
        >
          {starLabels[stars]}
        </motion.span>
      )}
    </div>
  );
}
