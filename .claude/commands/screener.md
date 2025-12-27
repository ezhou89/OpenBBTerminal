# Stock Screener Command

Screen stocks with criteria: **$ARGUMENTS**

## Instructions

Parse the screening criteria from arguments. Common patterns:
- `undervalued` - P/E < 15, P/B < 2
- `growth` - Revenue growth > 20%, EPS growth > 15%
- `dividend` - Dividend yield > 3%, payout ratio < 60%
- `momentum` - RSI between 50-70, above 50-day SMA
- `value` - Low P/E, high ROE
- `sector:technology` - Filter by sector
- Custom: `pe<20 roe>15 marketcap>10B`

### 1. Use OpenBB Screener
```python
from openbb import obb

# Finviz screener (no API key required)
# Available presets: top_gainers, top_losers, most_active, unusual_volume
# oversold, overbought, most_volatile, undervalued_large_caps, etc.

# Example for value stocks
results = obb.equity.screener(provider="finviz", preset="undervalued_large_caps")

# Or with custom filters
results = obb.equity.screener(
    provider="finviz",
    market_cap="Large",
    pe_ratio="Under 15",
    return_on_equity="Positive (>0%)"
)
```

### 2. Available Finviz Presets
- `top_gainers` / `top_losers` / `most_active`
- `most_volatile` / `unusual_volume`
- `overbought` / `oversold`
- `undervalued_large_caps` / `undervalued_growth`
- `high_dividend` / `steady_growth`

### 3. Custom Filters Available
- Market Cap: Mega, Large, Mid, Small, Micro
- P/E Ratio: Under 5, Under 10, Under 15, Under 20, Over 50
- Dividend Yield: Over 1%, Over 2%, Over 3%, Over 5%
- ROE: Positive, Over 5%, Over 10%, Over 15%
- And many more...

## Output Format

### Screen Results: [Criteria Description]

| Rank | Symbol | Company | Price | Change | Market Cap | P/E | Div Yield |
|------|--------|---------|-------|--------|------------|-----|-----------|
| 1    | ...    | ...     | ...   | ...    | ...        | ... | ...       |

### Top Picks Analysis
For the top 5 results, provide:
- Quick fundamental summary
- Technical setup
- Risk factors
- Catalyst potential

### Screen Statistics
- Total matches: X stocks
- Average P/E of results: X
- Average dividend yield: X%
- Sector breakdown of results
