# Stock Analysis Command

Perform a comprehensive stock analysis for: **$ARGUMENTS**

## Instructions

Use OpenBB to gather and analyze the following data for the given stock symbol(s):

### 1. Price & Quote Data
```python
from openbb import obb
symbol = "$ARGUMENTS".upper().strip()

# Current quote and recent performance
quote = obb.equity.price.quote(symbol)
performance = obb.equity.price.performance(symbol)
historical = obb.equity.price.historical(symbol, start_date="2024-01-01")
```

### 2. Fundamental Data
```python
# Key metrics and ratios
metrics = obb.equity.fundamental.metrics(symbol)
ratios = obb.equity.fundamental.ratios(symbol)
```

### 3. Analyst Estimates
```python
# Price targets and recommendations
targets = obb.equity.estimates.price_target(symbol)
```

### 4. Recent News
```python
news = obb.news.company(symbol, limit=5)
```

## Output Format

Provide a structured analysis including:
1. **Current Price & Performance** - Price, change, 52-week range, volume
2. **Valuation Metrics** - P/E, P/B, P/S, EV/EBITDA
3. **Financial Health** - Debt/Equity, Current Ratio, ROE, ROA
4. **Growth Metrics** - Revenue growth, EPS growth
5. **Analyst Sentiment** - Price targets, buy/hold/sell ratings
6. **Recent News Summary** - Key headlines affecting the stock
7. **Quick Take** - Brief bullish/bearish assessment

If any data provider fails, try alternative providers (yfinance, fmp, polygon, intrinio).
