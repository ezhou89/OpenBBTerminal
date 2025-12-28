# News & Sentiment Command

Get news and sentiment for: **$ARGUMENTS**

## Instructions

Parse arguments for symbol or topic:
- `AAPL` - Company-specific news
- `sector:technology` - Sector news
- `market` - General market news
- `crypto` or `BTC` - Cryptocurrency news

### 1. Get Company News
```python
from openbb import obb

query = "$ARGUMENTS".strip()

# Company news (works with benzinga, fmp, polygon, tiingo, yfinance)
if query.upper() in ["MARKET", "GENERAL"]:
    news = obb.news.world(limit=20)
else:
    # Assume it's a symbol
    symbol = query.upper()
    news = obb.news.company(symbol, limit=15, provider="yfinance")
```

### 2. Get Analyst Ratings (for stocks)
```python
# Recent analyst actions
targets = obb.equity.estimates.price_target(symbol, limit=5)
```

### 3. Insider Activity
```python
# Recent insider transactions
insider = obb.equity.ownership.insider_trading(symbol, limit=10)
```

## Output Format

### Latest News for [SYMBOL/TOPIC]

#### Top Headlines
For each article (up to 10):
| Time | Source | Headline | Sentiment |
|------|--------|----------|-----------|
| 2h ago | Reuters | "..." | Bullish/Bearish/Neutral |

### Sentiment Analysis
Based on headlines and content:
- **Overall Sentiment**: Bullish / Neutral / Bearish
- **Sentiment Score**: X/10
- **Key Themes**: List recurring topics

### Analyst Activity (if stock)
| Date | Analyst | Action | Target | Rating |
|------|---------|--------|--------|--------|
| ... | Goldman | Upgrade | $200 | Buy |

### Insider Activity (if stock)
| Date | Insider | Title | Action | Shares | Value |
|------|---------|-------|--------|--------|-------|
| ... | CEO | ... | Buy | 10,000 | $1.5M |

### Key Takeaways
1. Most impactful news item and why
2. Trend in sentiment (improving/declining)
3. Any red flags or catalysts to watch

### Social Sentiment (if available)
- Trending mentions
- Retail sentiment indicators
