import { motion } from "framer-motion";

interface CatalystBadgeProps {
  type: "earnings" | "clinical_trial" | "none";
  date: string | null;
  daysUntil: number | null;
  timing?: "AMC" | "BMO" | "unknown";
}

const catalystConfig = {
  earnings: {
    icon: "📊",
    label: "Earnings",
    description: "Quarterly results announcement",
  },
  clinical_trial: {
    icon: "🧬",
    label: "Trial Data",
    description: "Clinical trial results expected",
  },
  none: {
    icon: "📅",
    label: "No Catalyst",
    description: "No upcoming catalysts found",
  },
};

const timingLabels = {
  AMC: "After Market Close",
  BMO: "Before Market Open",
  unknown: "Time TBD",
};

function getUrgencyColor(daysUntil: number | null): string {
  if (daysUntil === null) return "grey";
  if (daysUntil <= 3) return "red";
  if (daysUntil <= 7) return "orange";
  if (daysUntil <= 14) return "yellow";
  return "green";
}

function getUrgencyClasses(daysUntil: number | null): {
  bg: string;
  border: string;
  text: string;
  glow: string;
} {
  const color = getUrgencyColor(daysUntil);
  const colorMap = {
    red: {
      bg: "bg-red-500/10",
      border: "border-red-500/50",
      text: "text-red-400",
      glow: "shadow-red-500/20",
    },
    orange: {
      bg: "bg-orange-500/10",
      border: "border-orange-500/50",
      text: "text-orange-400",
      glow: "shadow-orange-500/20",
    },
    yellow: {
      bg: "bg-yellow-500/10",
      border: "border-yellow-500/50",
      text: "text-yellow-400",
      glow: "shadow-yellow-500/20",
    },
    green: {
      bg: "bg-green-500/10",
      border: "border-green-500/50",
      text: "text-green-400",
      glow: "shadow-green-500/20",
    },
    grey: {
      bg: "bg-grey-700/50",
      border: "border-grey-600",
      text: "text-grey-400",
      glow: "",
    },
  };
  return colorMap[color];
}

export default function CatalystBadge({
  type,
  date,
  daysUntil,
  timing,
}: CatalystBadgeProps) {
  const config = catalystConfig[type];
  const urgency = getUrgencyClasses(daysUntil);
  const showPulse = daysUntil !== null && daysUntil <= 7;

  if (type === "none" || !date) {
    return (
      <div className="flex items-center gap-3 p-4 rounded-xl bg-grey-800/50 border border-grey-700">
        <span className="text-2xl opacity-50">📅</span>
        <div>
          <div className="text-grey-400 font-medium">No Upcoming Catalysts</div>
          <div className="text-grey-500 text-sm">No earnings or events in next 45 days</div>
        </div>
      </div>
    );
  }

  return (
    <motion.div
      className={`relative p-4 rounded-xl border ${urgency.bg} ${urgency.border} ${urgency.glow} shadow-lg`}
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
    >
      {/* Pulse animation for urgent catalysts */}
      {showPulse && (
        <motion.div
          className={`absolute inset-0 rounded-xl border ${urgency.border}`}
          animate={{
            opacity: [0.5, 0, 0.5],
            scale: [1, 1.02, 1],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      )}

      <div className="flex items-start gap-4">
        {/* Icon */}
        <motion.div
          className="text-3xl"
          animate={showPulse ? { scale: [1, 1.1, 1] } : {}}
          transition={{ duration: 1, repeat: Infinity }}
        >
          {config.icon}
        </motion.div>

        {/* Content */}
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <span className={`font-semibold ${urgency.text}`}>{config.label}</span>
            {timing && timing !== "unknown" && (
              <span className="text-xs px-2 py-0.5 rounded-full bg-grey-700 text-grey-300">
                {timing}
              </span>
            )}
          </div>

          <div className="text-grey-400 text-sm mb-2">{config.description}</div>

          {/* Date and countdown */}
          <div className="flex items-center gap-4">
            <div className="text-white font-medium">{date}</div>
            {daysUntil !== null && (
              <motion.div
                className={`flex items-center gap-1 ${urgency.text}`}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <span className="font-bold">
                  {daysUntil === 0
                    ? "TODAY"
                    : daysUntil === 1
                    ? "Tomorrow"
                    : `${daysUntil} days`}
                </span>
              </motion.div>
            )}
          </div>

          {/* Timing detail */}
          {timing && (
            <div className="text-xs text-grey-500 mt-1">
              {timingLabels[timing]}
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}
