# Earnings Calendar & Analysis Command

Get earnings data for: **$ARGUMENTS**

## Instructions

Parse arguments for different earnings views:
- `calendar` or `upcoming` - This week's earnings calendar
- `AAPL` - Specific company earnings history and upcoming
- `today` - Today's earnings releases
- `tomorrow` - Tomorrow's releases
- `week` - Full week calendar

### 1. Get Earnings Calendar
```python
from openbb import obb
from datetime import datetime, timedelta

query = "$ARGUMENTS".lower().strip()

# Upcoming earnings calendar (works with fmp, nasdaq)
calendar = obb.equity.calendar.earnings(
    start_date=datetime.now().strftime("%Y-%m-%d"),
    end_date=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
    provider="fmp"
)
```

### 2. Company-Specific Earnings
```python
# If a symbol is provided
symbol = "$ARGUMENTS".upper()

# Historical earnings
earnings_history = obb.equity.fundamental.earnings(symbol)

# Earnings estimates
estimates = obb.equity.estimates.consensus(symbol)

# Earnings transcripts (if available)
transcripts = obb.equity.fundamental.transcript(symbol)
```

### 3. Earnings Surprises
```python
# Get historical beat/miss data
historical = obb.equity.fundamental.earnings(symbol)
# Calculate beat rate, average surprise
```

## Output Format

### Earnings Calendar: [Date Range]

#### Today's Releases
| Time | Symbol | Company | EPS Est | Rev Est | Market Cap |
|------|--------|---------|---------|---------|------------|
| BMO | AAPL | Apple Inc | $1.45 | $89.5B | $3.0T |
| AMC | MSFT | Microsoft | $2.78 | $56.2B | $2.8T |

*BMO = Before Market Open, AMC = After Market Close*

#### Tomorrow's Releases
| Time | Symbol | Company | EPS Est | Rev Est |
|------|--------|---------|---------|---------|

#### Rest of Week
[Table format by day]

---

### Company Earnings: [SYMBOL] (if specific stock requested)

#### Upcoming Earnings
- **Date**: YYYY-MM-DD
- **Time**: Before/After Market
- **EPS Estimate**: $X.XX
- **Revenue Estimate**: $XX.XB

#### Historical Performance
| Quarter | Date | EPS Est | EPS Actual | Surprise | Rev Est | Rev Actual |
|---------|------|---------|------------|----------|---------|------------|
| Q4 2024 | ... | $1.40 | $1.52 | +8.6% | $88B | $90B |
| Q3 2024 | ... | $1.35 | $1.42 | +5.2% | $85B | $86B |

#### Track Record
- **Beat Rate (EPS)**: X/X quarters (XX%)
- **Average EPS Surprise**: +X.X%
- **Beat Rate (Revenue)**: X/X quarters (XX%)

#### Stock Reaction to Earnings
| Quarter | Surprise | Next-Day Move |
|---------|----------|---------------|
| Q4 2024 | +8.6% | +3.2% |
| Q3 2024 | +5.2% | -1.5% |

#### Analyst Expectations
- **Current EPS Estimates**: FY24 $X.XX, FY25 $X.XX
- **Revision Trend**: Up/Down over last 30 days
- **Number of Analysts**: XX

### Trading Considerations
1. **Expected Move**: Based on options IV, ±X.X%
2. **Historical Volatility**: Average post-earnings move ±X.X%
3. **Key Metrics to Watch**: List important metrics for this company
4. **Risk Factors**: Guidance, margins, growth rates to monitor
