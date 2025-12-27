# Options Analysis Command

Analyze options for: **$ARGUMENTS**

## Instructions

Parse the symbol and optional parameters:
- `AAPL` - Full options chain analysis
- `AAPL 2024-01-19` - Specific expiration
- `AAPL calls` or `AAPL puts` - Filter by type
- `AAPL ATM` - Focus on at-the-money options

### 1. Get Options Chain
```python
from openbb import obb

symbol = "$ARGUMENTS".split()[0].upper()

# Get options chain (works with yfinance, cboe, intrinio, tradier)
chain = obb.derivatives.options.chains(symbol, provider="yfinance")
```

### 2. Analyze the Chain
```python
# Get current stock price for reference
quote = obb.equity.price.quote(symbol)
current_price = quote.results[0].last_price

# Filter for relevant strikes (within 20% of current price)
# Group by expiration
# Calculate Greeks if available
```

### 3. Unusual Activity (if available)
```python
# Check for unusual options activity
unusual = obb.derivatives.options.unusual(symbol)
```

## Output Format

### Current Stock Price: $XXX.XX

### Options Chain Summary
**Next Expiration: YYYY-MM-DD (X days)**

#### Calls
| Strike | Bid | Ask | Last | Volume | OI | IV | Delta |
|--------|-----|-----|------|--------|----|----|-------|

#### Puts
| Strike | Bid | Ask | Last | Volume | OI | IV | Delta |
|--------|-----|-----|------|--------|----|----|-------|

### Key Metrics
- **Implied Volatility (ATM)**: X%
- **Put/Call Ratio (Volume)**: X.XX
- **Put/Call Ratio (OI)**: X.XX
- **Max Pain**: $XXX

### Notable Activity
- Highest volume strikes
- Unusual open interest changes
- Large block trades if detected

### Trading Ideas
Based on the options data, suggest:
1. **Bullish Play**: (e.g., buy calls, bull spread)
2. **Bearish Play**: (e.g., buy puts, bear spread)
3. **Neutral Play**: (e.g., iron condor, straddle)

Include strike prices, expirations, and estimated costs.

### Risk Warning
- IV percentile (is IV high or low historically?)
- Upcoming events (earnings, dividends)
- Liquidity concerns for wide bid-ask spreads
