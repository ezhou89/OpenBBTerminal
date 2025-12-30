import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { Settings } from "../../App";
import ParameterSlider from "./ParameterSlider";
import ProviderSelect from "./ProviderSelect";
import StrategyFilter from "./StrategyFilter";

interface SettingsPanelProps {
  settings: Settings;
  onSettingsChange: (settings: Settings) => void;
}

export default function SettingsPanel({
  settings,
  onSettingsChange,
}: SettingsPanelProps) {
  const [isOpen, setIsOpen] = useState(false);

  const updateSetting = <K extends keyof Settings>(key: K, value: Settings[K]) => {
    onSettingsChange({ ...settings, [key]: value });
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      {/* Toggle Button */}
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        className="absolute bottom-0 right-0 w-12 h-12 rounded-full bg-burgundy-600 text-white
                   shadow-lg flex items-center justify-center hover:bg-burgundy-500 transition-colors"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <motion.svg
          className="w-6 h-6"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          animate={{ rotate: isOpen ? 90 : 0 }}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
          />
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
          />
        </motion.svg>
      </motion.button>

      {/* Settings Panel */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            className="absolute bottom-16 right-0 w-80 bg-grey-900 border border-grey-700
                       rounded-xl shadow-2xl overflow-hidden"
          >
            {/* Header */}
            <div className="px-4 py-3 bg-grey-800 border-b border-grey-700">
              <h3 className="font-semibold text-white">Settings</h3>
              <p className="text-xs text-grey-500">Adjust research parameters</p>
            </div>

            {/* Content */}
            <div className="p-4 max-h-96 overflow-y-auto">
              <ParameterSlider
                label="Strike Distance"
                value={settings.maxStrikeDistancePct}
                min={1}
                max={25}
                unit="%"
                description="Maximum distance from current price for option strikes"
                onChange={(v) => updateSetting("maxStrikeDistancePct", v)}
              />

              <ParameterSlider
                label="Expiration Window"
                value={settings.expirationWindowDays}
                min={7}
                max={90}
                unit=" days"
                description="Maximum days until expiration to consider"
                onChange={(v) => updateSetting("expirationWindowDays", v)}
              />

              <ParameterSlider
                label="Minimum IV Rank"
                value={settings.minIvRank}
                min={0}
                max={100}
                unit="%"
                description="Filter out stocks below this IV rank"
                onChange={(v) => updateSetting("minIvRank", v)}
              />

              <div className="my-4 border-t border-grey-700" />

              <ProviderSelect
                value={settings.provider}
                onChange={(v) => updateSetting("provider", v)}
              />

              <StrategyFilter
                value={settings.strategyFilter}
                onChange={(v) => updateSetting("strategyFilter", v)}
              />
            </div>

            {/* Footer */}
            <div className="px-4 py-3 bg-grey-800/50 border-t border-grey-700">
              <button
                onClick={() => {
                  onSettingsChange({
                    maxStrikeDistancePct: 10,
                    expirationWindowDays: 45,
                    minIvRank: 0,
                    provider: "cboe",
                    strategyFilter: "all",
                  });
                }}
                className="text-sm text-grey-400 hover:text-white transition-colors"
              >
                Reset to defaults
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
