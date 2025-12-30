import { useState } from "react";
import { MagnifyingGlassIcon } from "@radix-ui/react-icons";

interface DiscoveryPanelProps {
  onSymbolSelect: (symbol: string) => void;
  isLoading: boolean;
}

// Mock upcoming earnings data
const upcomingEarnings = [
  { symbol: "AAPL", company: "Apple Inc.", date: "Jan 30", timing: "AMC" },
  { symbol: "MSFT", company: "Microsoft Corp.", date: "Jan 28", timing: "AMC" },
  { symbol: "GOOGL", company: "Alphabet Inc.", date: "Feb 1", timing: "AMC" },
  { symbol: "AMZN", company: "Amazon.com Inc.", date: "Feb 3", timing: "AMC" },
  { symbol: "NVDA", company: "NVIDIA Corp.", date: "Feb 21", timing: "AMC" },
  { symbol: "TSLA", company: "Tesla Inc.", date: "Jan 29", timing: "AMC" },
];

export default function DiscoveryPanel({
  onSymbolSelect,
  isLoading,
}: DiscoveryPanelProps) {
  const [searchQuery, setSearchQuery] = useState("");

  const filteredEarnings = upcomingEarnings.filter(
    (e) =>
      e.symbol.toLowerCase().includes(searchQuery.toLowerCase()) ||
      e.company.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      onSymbolSelect(searchQuery.trim().toUpperCase());
    }
  };

  return (
    <div className="h-full p-6 overflow-auto">
      {/* Search Bar */}
      <div className="max-w-2xl mx-auto mb-8">
        <form onSubmit={handleSubmit}>
          <div className="relative">
            <MagnifyingGlassIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-grey-500" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Enter ticker symbol (e.g., AAPL)"
              className="w-full pl-12 pr-4 py-4 bg-grey-800 border border-grey-700 rounded-xl text-lg placeholder-grey-500 focus:outline-none focus:border-burgundy-400 focus:ring-1 focus:ring-burgundy-400"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !searchQuery.trim()}
              className="absolute right-2 top-1/2 -translate-y-1/2 btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? "Loading..." : "Research"}
            </button>
          </div>
        </form>
        <p className="text-center text-grey-500 text-sm mt-2">
          Use the gear icon in the corner to adjust settings
        </p>
      </div>

      {/* Upcoming Earnings Grid */}
      <div className="max-w-4xl mx-auto">
        <h2 className="text-lg font-semibold text-grey-300 mb-4">
          Upcoming Earnings This Week
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredEarnings.map((earning) => (
            <button
              key={earning.symbol}
              onClick={() => onSymbolSelect(earning.symbol)}
              disabled={isLoading}
              className="panel-card text-left hover:border-burgundy-400 transition-colors disabled:opacity-50"
            >
              <div className="flex items-start justify-between">
                <div>
                  <div className="text-lg font-semibold text-white">
                    {earning.symbol}
                  </div>
                  <div className="text-sm text-grey-400 mt-1">
                    {earning.company}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-medium text-burgundy-300">
                    {earning.date}
                  </div>
                  <div className="text-xs text-grey-500">{earning.timing}</div>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
