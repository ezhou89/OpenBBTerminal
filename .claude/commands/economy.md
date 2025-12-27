# Economic Indicators Command

Get economic data for: **$ARGUMENTS**

## Instructions

Parse arguments for specific indicators or general overview:
- `overview` or empty - Key economic dashboard
- `gdp` - GDP data
- `inflation` or `cpi` - Inflation metrics
- `employment` or `jobs` - Labor market data
- `rates` or `fed` - Interest rates and Fed data
- `housing` - Housing market data
- `earnings` - Upcoming earnings calendar

### 1. Economic Dashboard
```python
from openbb import obb

query = "$ARGUMENTS".lower().strip() if "$ARGUMENTS" else "overview"

# Key indicators from FRED (requires free API key)
# GDP
gdp = obb.economy.gdp.nominal(provider="oecd", country="united_states")

# Inflation
cpi = obb.economy.cpi(provider="fred", country="united_states")

# Unemployment
unemployment = obb.economy.unemployment(provider="oecd", country="united_states")

# Fed Funds Rate
fed_rate = obb.fixedincome.rate.effr(provider="federal_reserve")

# Treasury Yields
yields = obb.fixedincome.government.treasury_rates(provider="federal_reserve")
```

### 2. Economic Calendar
```python
# Upcoming economic events
calendar = obb.economy.calendar(provider="fmp")
```

### 3. Yield Curve
```python
# Treasury yield curve
curve = obb.fixedincome.government.yield_curve(provider="federal_reserve")
```

## Output Format

### Economic Dashboard - [Date]

#### Key Indicators
| Indicator | Current | Previous | Change | Trend |
|-----------|---------|----------|--------|-------|
| GDP Growth (QoQ) | X.X% | X.X% | +/- | Expanding/Contracting |
| Inflation (CPI YoY) | X.X% | X.X% | +/- | Rising/Falling |
| Unemployment | X.X% | X.X% | +/- | Improving/Worsening |
| Fed Funds Rate | X.XX% | X.XX% | +/- | Hiking/Cutting/Holding |
| 10Y Treasury | X.XX% | X.XX% | +/- | Rising/Falling |

#### Yield Curve
| Maturity | Yield | Change |
|----------|-------|--------|
| 3-Month | X.XX% | +/- |
| 2-Year | X.XX% | +/- |
| 10-Year | X.XX% | +/- |
| 30-Year | X.XX% | +/- |

**Curve Status**: Normal / Inverted / Flat
**Recession Signal**: Yes/No (based on 2Y-10Y spread)

### Upcoming Economic Events
| Date | Time | Event | Forecast | Previous | Impact |
|------|------|-------|----------|----------|--------|
| ... | 8:30 AM | Non-Farm Payrolls | 200K | 180K | High |

### Market Implications
Based on current economic conditions:
1. **Equity Outlook**: Favorable/Unfavorable because...
2. **Bond Outlook**: Rates likely to...
3. **Sector Rotation**: Favor defensive/cyclical because...
4. **Risk Assessment**: Key risks to monitor

### Fed Watch
- Next FOMC meeting date
- Market-implied rate expectations
- Recent Fed commentary summary
