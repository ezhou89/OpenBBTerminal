import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import DiscoveryPanel from "./components/DiscoveryPanel";
import AnalysisPanel from "./components/AnalysisPanel";
import TradePanel from "./components/TradePanel";
import { SettingsPanel } from "./components/Controls";

// Types for the research data
export interface ResearchData {
  symbol: string;
  price: number;
  timestamp: string;
  catalyst: {
    type: "earnings" | "clinical_trial" | "none";
    date: string | null;
    days_until: number | null;
    timing: "AMC" | "BMO" | null;
  };
  iv_metrics: {
    atm_iv: number | null;
    rank: number | null;
    percentile: number | null;
    environment: "very_low" | "low" | "neutral" | "elevated" | "very_high";
  };
  expected_move: {
    dollars: number;
    percent: number;
    range: [number, number];
  };
  trade_ideas: Array<{
    strategy: string;
    legs: Array<{
      action: "buy" | "sell";
      option_type: "call" | "put";
      strike: number;
      premium: number;
    }>;
    expiration: string | null;
    max_profit: number | null;
    max_risk: number | null;
    rationale: string;
  }>;
  quality: {
    score: number;
    stars: number;
    summary: string;
  };
  plain_english: string;
}

export interface Settings {
  maxStrikeDistancePct: number;
  expirationWindowDays: number;
  minIvRank: number;
  provider: "cboe" | "yfinance" | "intrinio";
  strategyFilter: "all" | "buy" | "sell";
}

declare global {
  interface Window {
    json_data: string;
    title: string;
    pywry: unknown;
  }
}

type Step = "discover" | "analyze" | "trade";

const stepOrder: Step[] = ["discover", "analyze", "trade"];

function App() {
  const [currentStep, setCurrentStep] = useState<Step>("discover");
  const [selectedSymbol, setSelectedSymbol] = useState<string | null>(null);
  const [researchData, setResearchData] = useState<ResearchData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [settings, setSettings] = useState<Settings>({
    maxStrikeDistancePct: 10,
    expirationWindowDays: 45,
    minIvRank: 0,
    provider: "cboe",
    strategyFilter: "all",
  });

  // Handle production data injection
  useEffect(() => {
    if (process.env.NODE_ENV === "production") {
      const interval = setInterval(() => {
        if (window.json_data) {
          try {
            const data = JSON.parse(window.json_data);
            setResearchData(data);
            setSelectedSymbol(data.symbol);
            setCurrentStep("analyze");
          } catch (e) {
            console.error("Failed to parse json_data:", e);
          }
          clearInterval(interval);
        }
      }, 100);
      return () => clearInterval(interval);
    }
  }, []);

  const handleSymbolSelect = async (symbol: string) => {
    setSelectedSymbol(symbol);
    setIsLoading(true);

    // In development, use mock data
    if (process.env.NODE_ENV !== "production") {
      // Simulate API call with mock data
      setTimeout(() => {
        setResearchData(getMockData(symbol));
        setCurrentStep("analyze");
        setIsLoading(false);
      }, 800);
    } else {
      // In production, data comes from window.json_data
      setCurrentStep("analyze");
      setIsLoading(false);
    }
  };

  const goToStep = (step: Step) => {
    setCurrentStep(step);
  };

  const canNavigateTo = (step: Step): boolean => {
    const currentIndex = stepOrder.indexOf(currentStep);
    const targetIndex = stepOrder.indexOf(step);

    // Can always go back
    if (targetIndex < currentIndex) return true;

    // Can only go forward if we have data
    if (step === "analyze" || step === "trade") {
      return researchData !== null;
    }

    return true;
  };

  return (
    <div className="h-full bg-grey-900 text-white font-display">
      {/* Header with Step Navigation */}
      <header className="border-b border-grey-800 px-6 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-semibold">
            Options Research
            {selectedSymbol && (
              <span className="ml-2 text-burgundy-400">{selectedSymbol}</span>
            )}
          </h1>

          {/* Step Indicators */}
          <nav className="flex items-center gap-2">
            {stepOrder.map((step, index) => {
              const isActive = currentStep === step;
              const isClickable = canNavigateTo(step);
              const stepNumber = index + 1;
              const stepLabels: Record<Step, string> = {
                discover: "Discover",
                analyze: "Analyze",
                trade: "Trade",
              };

              return (
                <button
                  key={step}
                  onClick={() => isClickable && goToStep(step)}
                  disabled={!isClickable}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
                    isActive
                      ? "bg-burgundy-500 text-white"
                      : isClickable
                      ? "bg-grey-800 text-grey-300 hover:bg-grey-700"
                      : "bg-grey-850 text-grey-600 cursor-not-allowed"
                  }`}
                >
                  <span
                    className={`w-6 h-6 rounded-full flex items-center justify-center text-sm font-medium ${
                      isActive
                        ? "bg-white/20"
                        : isClickable
                        ? "bg-grey-700"
                        : "bg-grey-800"
                    }`}
                  >
                    {stepNumber}
                  </span>
                  <span className="hidden sm:inline">{stepLabels[step]}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="h-[calc(100%-73px)] overflow-hidden">
        <AnimatePresence mode="wait">
          {currentStep === "discover" && (
            <motion.div
              key="discover"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="h-full"
            >
              <DiscoveryPanel
                onSymbolSelect={handleSymbolSelect}
                isLoading={isLoading}
              />
            </motion.div>
          )}

          {currentStep === "analyze" && researchData && (
            <motion.div
              key="analyze"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="h-full"
            >
              <AnalysisPanel
                data={researchData}
                onContinue={() => goToStep("trade")}
              />
            </motion.div>
          )}

          {currentStep === "trade" && researchData && (
            <motion.div
              key="trade"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="h-full"
            >
              <TradePanel
                data={researchData}
                onBack={() => goToStep("analyze")}
              />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Settings Panel (floating) */}
        <SettingsPanel settings={settings} onSettingsChange={setSettings} />
      </main>
    </div>
  );
}

// Mock data for development
function getMockData(symbol: string): ResearchData {
  return {
    symbol,
    price: 175.5,
    timestamp: new Date().toISOString(),
    catalyst: {
      type: "earnings",
      date: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000)
        .toISOString()
        .slice(0, 10),
      days_until: 5,
      timing: "AMC",
    },
    iv_metrics: {
      atm_iv: 0.35,
      rank: 78,
      percentile: 82,
      environment: "elevated",
    },
    expected_move: {
      dollars: 8.5,
      percent: 4.9,
      range: [167.0, 184.0],
    },
    trade_ideas: [
      {
        strategy: "iron_condor",
        legs: [
          { action: "sell", option_type: "put", strike: 170, premium: 2.5 },
          { action: "buy", option_type: "put", strike: 165, premium: 1.2 },
          { action: "sell", option_type: "call", strike: 185, premium: 2.3 },
          { action: "buy", option_type: "call", strike: 190, premium: 1.1 },
        ],
        expiration: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
          .toISOString()
          .slice(0, 10),
        max_profit: 250,
        max_risk: 250,
        rationale: "High IV environment suggests selling premium",
      },
      {
        strategy: "short_strangle",
        legs: [
          { action: "sell", option_type: "put", strike: 170, premium: 2.5 },
          { action: "sell", option_type: "call", strike: 185, premium: 2.3 },
        ],
        expiration: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
          .toISOString()
          .slice(0, 10),
        max_profit: 480,
        max_risk: null,
        rationale: "Collect maximum premium with undefined risk",
      },
    ],
    quality: {
      score: 82.5,
      stars: 4,
      summary: "Strong sell premium candidate (high IV, good timing)",
    },
    plain_english:
      "AAPL options are expensive right now (IV Rank: 78%). The market expects a move of about $8.50 after earnings on Jan 25. Options expiring Jan 26 capture this event perfectly.",
  };
}

export default App;
