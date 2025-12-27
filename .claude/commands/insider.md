# Insider Trading Analysis Command

Analyze insider activity for: **$ARGUMENTS**

## Instructions

Get insider trading data for the specified symbol:
- `AAPL` - Insider trades for Apple
- `AAPL 90d` - Last 90 days of trades
- `sector:tech` - Insider activity across tech sector

### 1. Get Insider Trading Data
```python
from openbb import obb

symbol = "$ARGUMENTS".split()[0].upper()

# Insider trading data (works with fmp, intrinio)
insider = obb.equity.ownership.insider_trading(symbol, limit=50)

# Institutional ownership
institutions = obb.equity.ownership.institutional(symbol)
```

### 2. Get Form 4 Filings from SEC
```python
# SEC filings for more detail
filings = obb.regulators.sec.form_13f(symbol)
```

### 3. Analyze Patterns
```python
# Calculate buy/sell ratio
# Identify cluster buying/selling
# Track CEO/CFO transactions specifically
```

## Output Format

### Insider Activity: [SYMBOL]

#### Recent Transactions (Last 90 Days)
| Date | Insider | Title | Type | Shares | Price | Value | Holdings After |
|------|---------|-------|------|--------|-------|-------|----------------|
| 2024-01-15 | Tim Cook | CEO | Sell | 50,000 | $185 | $9.25M | 1.2M shares |
| 2024-01-10 | Luca Maestri | CFO | Buy | 10,000 | $180 | $1.8M | 250K shares |

#### Transaction Summary
| Metric | Buys | Sells |
|--------|------|-------|
| Count | X | X |
| Total Shares | XXX,XXX | XXX,XXX |
| Total Value | $X.XM | $X.XM |
| Avg Price | $XXX | $XXX |

**Buy/Sell Ratio (by value)**: X.XX
**Insider Sentiment**: Bullish / Neutral / Bearish

#### Key Insiders Activity
| Insider | Title | 12-Month Net | Last Action | Last Date |
|---------|-------|--------------|-------------|-----------|
| CEO | ... | +50,000 shares | Buy | 2024-01-10 |
| CFO | ... | -100,000 shares | Sell | 2024-01-15 |

#### Institutional Ownership
- **% Held by Institutions**: XX.X%
- **Change (QoQ)**: +/- X.X%
- **Number of Holders**: XXX
- **Top Holders**: Vanguard, BlackRock, Fidelity...

#### Pattern Analysis
- **Cluster Activity**: Any coordinated buying/selling detected?
- **Price Context**: Were trades at highs or lows?
- **Pre-Event Trades**: Any trades before earnings/announcements?

### Interpretation
1. **Bullish Signals**: (e.g., CEO buying, multiple insiders buying)
2. **Bearish Signals**: (e.g., CFO selling large position, cluster selling)
3. **Neutral Factors**: (e.g., planned 10b5-1 sales, option exercises)

### Historical Context
- Insider buying accuracy (did stock go up after previous buys?)
- Notable past transactions and outcomes

### Red Flags (if any)
- Unusual timing before announcements
- Large concentrated selling
- New executives selling immediately
