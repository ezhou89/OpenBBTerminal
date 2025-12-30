import { motion } from "framer-motion";
import type { ResearchData } from "../../App";
import IVGauge from "./IVGauge";
import ExpectedMoveBar from "./ExpectedMoveBar";
import CatalystBadge from "./CatalystBadge";
import QualityStars from "../TradePanel/QualityStars";

interface AnalysisPanelProps {
  data: ResearchData;
  onContinue: () => void;
}

export default function AnalysisPanel({ data, onContinue }: AnalysisPanelProps) {
  return (
    <div className="h-full p-6 overflow-auto">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="flex items-start justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold">
              {data.symbol}{" "}
              <span className="text-grey-400 font-normal">
                ${data.price.toFixed(2)}
              </span>
            </h2>
            <p className="text-grey-500 text-sm mt-1">
              Analysis as of {new Date(data.timestamp).toLocaleString()}
            </p>
          </div>
          <button onClick={onContinue} className="btn-primary">
            View Trade Ideas
          </button>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* IV Gauge */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="panel-card"
          >
            <h3 className="text-sm font-medium text-grey-400 mb-4">
              Options Price Level
            </h3>
            <IVGauge
              value={data.iv_metrics.rank ?? data.iv_metrics.percentile ?? 50}
              environment={data.iv_metrics.environment}
              atm_iv={data.iv_metrics.atm_iv}
            />
          </motion.div>

          {/* Expected Move */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="panel-card"
          >
            <h3 className="text-sm font-medium text-grey-400 mb-4">
              Expected Move
            </h3>
            <ExpectedMoveBar
              currentPrice={data.price}
              expectedMoveDollars={data.expected_move.dollars}
              expectedMovePercent={data.expected_move.percent}
              range={data.expected_move.range}
            />
          </motion.div>

          {/* Catalyst */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="panel-card"
          >
            <h3 className="text-sm font-medium text-grey-400 mb-4">
              Upcoming Catalyst
            </h3>
            <CatalystBadge
              type={data.catalyst.type}
              date={data.catalyst.date}
              daysUntil={data.catalyst.days_until}
              timing={data.catalyst.timing}
            />
          </motion.div>
        </div>

        {/* Quality Score */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="panel-card mb-8"
        >
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-medium text-grey-400 mb-2">
                Trade Quality
              </h3>
              <QualityStars stars={data.quality.stars} />
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-burgundy-400">
                {data.quality.score.toFixed(0)}
              </div>
              <div className="text-sm text-grey-500">/ 100</div>
            </div>
          </div>
          <p className="text-grey-300 mt-4">{data.quality.summary}</p>
        </motion.div>

        {/* Plain English Summary */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="panel-card bg-burgundy-900/30 border-burgundy-500/30"
        >
          <h3 className="text-sm font-medium text-burgundy-300 mb-3">
            Summary
          </h3>
          <p className="text-grey-200 leading-relaxed whitespace-pre-line">
            {data.plain_english}
          </p>
        </motion.div>
      </div>
    </div>
  );
}
