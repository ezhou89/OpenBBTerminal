# Compare Securities Command

Compare: **$ARGUMENTS**

## Instructions

Parse multiple symbols to compare (comma or space separated):
- `AAPL, MSFT, GOOGL` - Compare stocks
- `AAPL vs MSFT` - Head-to-head comparison
- `SPY QQQ IWM` - Compare ETFs
- `sector:tech` - Compare sector leaders

### 1. Get Comparison Data
```python
from openbb import obb
import pandas as pd

# Parse symbols
symbols_str = "$ARGUMENTS"
symbols = [s.strip().upper() for s in symbols_str.replace("vs", ",").replace(" ", ",").split(",") if s.strip()]

# Get data for each symbol
data = {}
for symbol in symbols:
    data[symbol] = {
        'quote': obb.equity.price.quote(symbol),
        'metrics': obb.equity.fundamental.metrics(symbol),
        'performance': obb.equity.price.performance(symbol),
        'historical': obb.equity.price.historical(symbol, start_date="2024-01-01")
    }
```

### 2. Use Built-in Compare Function
```python
# OpenBB has peer comparison built in
peers = obb.equity.compare.peers(symbols[0])
comparison = obb.equity.compare.groups(symbols)
```

### 3. Calculate Relative Performance
```python
# Normalize prices to compare performance
# Calculate correlation between securities
# Compare key metrics side-by-side
```

## Output Format

### Comparison: [Symbol1] vs [Symbol2] vs [Symbol3]

#### Price Performance
| Metric | AAPL | MSFT | GOOGL | Best |
|--------|------|------|-------|------|
| Current Price | $XXX | $XXX | $XXX | - |
| Day Change | +X.X% | +X.X% | +X.X% | AAPL |
| Week Change | +X.X% | +X.X% | +X.X% | MSFT |
| Month Change | +X.X% | +X.X% | +X.X% | GOOGL |
| YTD Change | +X.X% | +X.X% | +X.X% | AAPL |
| 52-Week Change | +X.X% | +X.X% | +X.X% | MSFT |

#### Valuation Comparison
| Metric | AAPL | MSFT | GOOGL | Cheapest |
|--------|------|------|-------|----------|
| P/E Ratio | XX.X | XX.X | XX.X | GOOGL |
| Forward P/E | XX.X | XX.X | XX.X | GOOGL |
| P/S Ratio | X.X | X.X | X.X | AAPL |
| P/B Ratio | X.X | X.X | X.X | MSFT |
| EV/EBITDA | XX.X | XX.X | XX.X | GOOGL |

#### Profitability
| Metric | AAPL | MSFT | GOOGL | Best |
|--------|------|------|-------|------|
| Gross Margin | XX% | XX% | XX% | MSFT |
| Operating Margin | XX% | XX% | XX% | MSFT |
| Net Margin | XX% | XX% | XX% | AAPL |
| ROE | XX% | XX% | XX% | AAPL |
| ROA | XX% | XX% | XX% | MSFT |

#### Growth
| Metric | AAPL | MSFT | GOOGL | Fastest |
|--------|------|------|-------|---------|
| Revenue Growth | XX% | XX% | XX% | MSFT |
| EPS Growth | XX% | XX% | XX% | GOOGL |

#### Risk Metrics
| Metric | AAPL | MSFT | GOOGL | Lowest Risk |
|--------|------|------|-------|-------------|
| Beta | X.XX | X.XX | X.XX | MSFT |
| Volatility (30d) | XX% | XX% | XX% | AAPL |

#### Correlation Matrix
|       | AAPL | MSFT | GOOGL |
|-------|------|------|-------|
| AAPL  | 1.00 | 0.XX | 0.XX |
| MSFT  | 0.XX | 1.00 | 0.XX |
| GOOGL | 0.XX | 0.XX | 1.00 |

### Verdict
**Best Value**: [Symbol] - Reason
**Best Growth**: [Symbol] - Reason
**Lowest Risk**: [Symbol] - Reason
**Overall Pick**: [Symbol] - Summary reasoning
