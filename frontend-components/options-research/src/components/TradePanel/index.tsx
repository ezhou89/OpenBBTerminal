import { motion } from "framer-motion";
import type { ResearchData } from "../../App";
import TradeIdeaCard from "./TradeIdeaCard";
import QualityStars from "./QualityStars";

interface TradePanelProps {
  data: ResearchData;
  onBack: () => void;
}

export default function TradePanel({ data, onBack }: TradePanelProps) {
  const hasTradeIdeas = data.trade_ideas && data.trade_ideas.length > 0;

  return (
    <div className="h-full p-6 overflow-auto">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="flex items-start justify-between mb-6">
          <div>
            <button
              onClick={onBack}
              className="text-grey-400 hover:text-white text-sm flex items-center gap-1 mb-2 transition-colors"
            >
              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Analysis
            </button>
            <h2 className="text-2xl font-bold">
              Trade Ideas for {data.symbol}
            </h2>
            <p className="text-grey-500 text-sm mt-1">
              Strategies based on current IV environment and catalyst proximity
            </p>
          </div>
          <div className="text-right">
            <QualityStars stars={data.quality.stars} />
            <div className="text-grey-400 text-sm mt-1">
              Score: {data.quality.score.toFixed(0)}/100
            </div>
          </div>
        </div>

        {/* Environment Summary */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="panel-card mb-6 bg-gradient-to-r from-burgundy-900/30 to-grey-800/50"
        >
          <div className="flex flex-wrap gap-6">
            <div>
              <div className="text-xs text-grey-500 uppercase">IV Environment</div>
              <div className="text-lg font-semibold text-white capitalize">
                {data.iv_metrics.environment.replace("_", " ")}
              </div>
            </div>
            <div>
              <div className="text-xs text-grey-500 uppercase">IV Rank</div>
              <div className="text-lg font-semibold text-white">
                {data.iv_metrics.rank?.toFixed(0) ?? "N/A"}%
              </div>
            </div>
            <div>
              <div className="text-xs text-grey-500 uppercase">Expected Move</div>
              <div className="text-lg font-semibold text-white">
                ±${data.expected_move.dollars.toFixed(2)} ({data.expected_move.percent.toFixed(1)}%)
              </div>
            </div>
            {data.catalyst.days_until && (
              <div>
                <div className="text-xs text-grey-500 uppercase">Days to Catalyst</div>
                <div className="text-lg font-semibold text-white">
                  {data.catalyst.days_until} days
                </div>
              </div>
            )}
          </div>
        </motion.div>

        {/* Trade Ideas Grid */}
        {hasTradeIdeas ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {data.trade_ideas.map((idea, index) => (
              <TradeIdeaCard key={idea.strategy} idea={idea} index={index} />
            ))}
          </div>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="panel-card text-center py-12"
          >
            <div className="text-4xl mb-4">🤔</div>
            <h3 className="text-xl font-semibold text-grey-300 mb-2">
              No Trade Ideas Available
            </h3>
            <p className="text-grey-500 max-w-md mx-auto">
              The current market conditions don't suggest any high-confidence trade setups.
              Try adjusting your parameters or check back later.
            </p>
          </motion.div>
        )}

        {/* Disclaimer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-8 p-4 bg-grey-800/30 rounded-lg border border-grey-700/50"
        >
          <p className="text-grey-500 text-xs">
            <strong className="text-grey-400">Disclaimer:</strong> These trade ideas are
            generated algorithmically based on IV metrics and catalyst proximity. They are
            for educational purposes only and do not constitute financial advice. Options
            trading involves substantial risk and is not suitable for all investors.
            Always conduct your own research and consider consulting with a financial
            advisor before making trading decisions.
          </p>
        </motion.div>
      </div>
    </div>
  );
}
