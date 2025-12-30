import { motion } from "framer-motion";

type Provider = "cboe" | "yfinance" | "intrinio";

interface ProviderSelectProps {
  value: Provider;
  onChange: (value: Provider) => void;
}

const providers: { id: Provider; label: string; description: string }[] = [
  {
    id: "cboe",
    label: "CBOE",
    description: "Chicago Board Options Exchange - Real-time data",
  },
  {
    id: "yfinance",
    label: "Yahoo Finance",
    description: "Free delayed data - Good for research",
  },
  {
    id: "intrinio",
    label: "Intrinio",
    description: "Premium data provider - Requires API key",
  },
];

export default function ProviderSelect({ value, onChange }: ProviderSelectProps) {
  return (
    <div className="mb-4">
      <label className="text-sm font-medium text-grey-300 mb-3 block">
        Data Provider
      </label>
      <div className="space-y-2">
        {providers.map((provider) => (
          <motion.button
            key={provider.id}
            onClick={() => onChange(provider.id)}
            className={`w-full p-3 rounded-lg border text-left transition-all ${
              value === provider.id
                ? "bg-burgundy-900/30 border-burgundy-500/50 text-white"
                : "bg-grey-800/50 border-grey-700 text-grey-400 hover:border-grey-600"
            }`}
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
          >
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium">{provider.label}</div>
                <div className="text-xs text-grey-500">{provider.description}</div>
              </div>
              {value === provider.id && (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="w-5 h-5 bg-burgundy-500 rounded-full flex items-center justify-center"
                >
                  <svg className="w-3 h-3 text-white" viewBox="0 0 20 20" fill="currentColor">
                    <path
                      fillRule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clipRule="evenodd"
                    />
                  </svg>
                </motion.div>
              )}
            </div>
          </motion.button>
        ))}
      </div>
    </div>
  );
}
