import { motion } from "framer-motion";

interface TradeLeg {
  action: "buy" | "sell";
  option_type: "call" | "put";
  strike: number;
  premium: number;
}

interface TradeIdea {
  strategy: string;
  legs: TradeLeg[];
  expiration: string | null;
  max_profit: number | null;
  max_risk: number | null;
  rationale: string;
}

interface TradeIdeaCardProps {
  idea: TradeIdea;
  index: number;
}

const strategyEmoji: Record<string, string> = {
  iron_condor: "🦅",
  short_strangle: "🔒",
  short_straddle: "⚖️",
  short_straddle_pre_earnings: "⚡",
  long_straddle: "📈",
  long_straddle_pre_catalyst: "🚀",
  calendar_spread: "📅",
  vertical_spread: "↕️",
  post_catalyst_expiration: "🎯",
};

const strategyDescription: Record<string, string> = {
  iron_condor: "Sell premium with defined risk on both sides",
  short_strangle: "Collect premium from out-of-money options",
  short_straddle: "Sell at-the-money options for maximum premium",
  short_straddle_pre_earnings: "Capture IV crush after announcement",
  long_straddle: "Profit from large price moves in either direction",
  long_straddle_pre_catalyst: "Buy cheap premium before volatility expansion",
  calendar_spread: "Profit from time decay differential",
  vertical_spread: "Directional bet with defined risk",
  post_catalyst_expiration: "Target expiration after event for theta",
};

function formatStrategyName(strategy: string): string {
  return strategy
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

function formatLeg(leg: TradeLeg): string {
  const action = leg.action.toUpperCase();
  const type = leg.option_type.toUpperCase();
  return `${action} $${leg.strike} ${type}`;
}

export default function TradeIdeaCard({ idea, index }: TradeIdeaCardProps) {
  const emoji = strategyEmoji[idea.strategy] || "💡";
  const description = strategyDescription[idea.strategy] || idea.rationale;
  const hasDefinedRisk = idea.max_risk !== null && idea.max_risk > 0;
  const riskRewardRatio = hasDefinedRisk && idea.max_profit
    ? (idea.max_profit / idea.max_risk!).toFixed(2)
    : null;

  return (
    <motion.div
      className="panel-card hover:border-burgundy-500/50 transition-colors"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="text-2xl">{emoji}</span>
          <div>
            <h3 className="font-bold text-lg text-white">
              {formatStrategyName(idea.strategy)}
            </h3>
            <p className="text-grey-500 text-sm">{description}</p>
          </div>
        </div>
      </div>

      {/* Legs */}
      {idea.legs.length > 0 && (
        <div className="mb-4 p-3 bg-grey-800/50 rounded-lg">
          <div className="text-xs text-grey-500 uppercase mb-2">Trade Structure</div>
          <div className="space-y-1">
            {idea.legs.map((leg, i) => (
              <div
                key={i}
                className={`flex justify-between items-center text-sm ${
                  leg.action === "buy" ? "text-green-400" : "text-red-400"
                }`}
              >
                <span>{formatLeg(leg)}</span>
                <span className="text-grey-400">${leg.premium.toFixed(2)}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Expiration */}
      {idea.expiration && (
        <div className="flex items-center gap-2 mb-4 text-sm">
          <svg
            className="w-4 h-4 text-grey-500"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
            />
          </svg>
          <span className="text-grey-400">Exp: {idea.expiration}</span>
        </div>
      )}

      {/* P/L Stats */}
      <div className="grid grid-cols-3 gap-4 pt-4 border-t border-grey-700">
        <div>
          <div className="text-xs text-grey-500 uppercase">Max Profit</div>
          <div className="text-green-400 font-bold">
            {idea.max_profit !== null ? `$${idea.max_profit.toFixed(0)}` : "Unlimited"}
          </div>
        </div>
        <div>
          <div className="text-xs text-grey-500 uppercase">Max Risk</div>
          <div className="text-red-400 font-bold">
            {idea.max_risk !== null ? `$${idea.max_risk.toFixed(0)}` : "Undefined"}
          </div>
        </div>
        <div>
          <div className="text-xs text-grey-500 uppercase">Risk/Reward</div>
          <div
            className={`font-bold ${
              riskRewardRatio && parseFloat(riskRewardRatio) >= 1
                ? "text-green-400"
                : riskRewardRatio
                ? "text-yellow-400"
                : "text-grey-500"
            }`}
          >
            {riskRewardRatio ? `${riskRewardRatio}:1` : "N/A"}
          </div>
        </div>
      </div>

      {/* Rationale */}
      <div className="mt-4 pt-4 border-t border-grey-700">
        <div className="text-sm text-grey-300">{idea.rationale}</div>
      </div>
    </motion.div>
  );
}
