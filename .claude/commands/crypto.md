# Cryptocurrency Analysis Command

Analyze cryptocurrency: **$ARGUMENTS**

## Instructions

Parse arguments for crypto analysis:
- `BTC` or `bitcoin` - Bitcoin analysis
- `ETH` or `ethereum` - Ethereum analysis
- `market` - Overall crypto market overview
- `BTC,ETH,SOL` - Compare multiple cryptos
- `defi` - DeFi sector overview

### 1. Get Crypto Price Data
```python
from openbb import obb

symbol = "$ARGUMENTS".upper().strip()

# Map common names to symbols
symbol_map = {
    "BITCOIN": "BTC", "ETHEREUM": "ETH",
    "SOLANA": "SOL", "CARDANO": "ADA"
}
symbol = symbol_map.get(symbol, symbol)

# Price data (works with yfinance, polygon, tiingo, fmp)
# For yfinance, use format like "BTC-USD"
quote = obb.crypto.price.historical(
    symbol=f"{symbol}USD",  # or "BTC-USD" for yfinance
    provider="yfinance"
)
```

### 2. Get Market Overview
```python
# If "market" requested
# Get top cryptos by market cap
# Get total market cap
# Get BTC dominance
```

### 3. Technical Analysis
```python
# Apply technical indicators
data = obb.crypto.price.historical(f"{symbol}USD")
rsi = obb.technical.rsi(data=data)
macd = obb.technical.macd(data=data)
bbands = obb.technical.bbands(data=data)
```

### 4. Derivatives Data (for major cryptos)
```python
# Futures data from Deribit
futures = obb.derivatives.futures.curve(symbol="BTC", provider="deribit")

# Options data
options = obb.derivatives.options.chains(symbol="BTC", provider="deribit")
```

## Output Format

### Crypto Analysis: [SYMBOL]

#### Current Price & Performance
| Metric | Value | Change |
|--------|-------|--------|
| Price | $XX,XXX | +X.X% (24h) |
| 24h High | $XX,XXX | |
| 24h Low | $XX,XXX | |
| 24h Volume | $X.XB | |
| Market Cap | $X.XT | |
| Rank | #X | |

#### Performance
| Timeframe | Return |
|-----------|--------|
| 24 Hours | +X.X% |
| 7 Days | +X.X% |
| 30 Days | +X.X% |
| 90 Days | +X.X% |
| YTD | +X.X% |
| 1 Year | +X.X% |

#### Technical Analysis
| Indicator | Value | Signal |
|-----------|-------|--------|
| RSI (14) | XX | Overbought/Neutral/Oversold |
| MACD | XX | Bullish/Bearish |
| 50 SMA | $XX,XXX | Above/Below |
| 200 SMA | $XX,XXX | Above/Below |

**Trend**: Bullish / Neutral / Bearish
**Support Levels**: $XX,XXX, $XX,XXX
**Resistance Levels**: $XX,XXX, $XX,XXX

#### On-Chain Metrics (if available)
- Active Addresses (24h)
- Transaction Volume
- Exchange Inflows/Outflows
- Whale Activity

#### Derivatives (Major Cryptos)
- Funding Rate: X.XX%
- Open Interest: $X.XB
- Long/Short Ratio: X.XX
- Options Put/Call: X.XX

### Market Overview (if requested)

#### Top 10 by Market Cap
| Rank | Symbol | Price | 24h | 7d | Market Cap |
|------|--------|-------|-----|----|-----------|
| 1 | BTC | $XX,XXX | +X% | +X% | $X.XT |
| 2 | ETH | $X,XXX | +X% | +X% | $XXXB |

#### Market Metrics
- **Total Market Cap**: $X.XT
- **24h Volume**: $XXXB
- **BTC Dominance**: XX.X%
- **ETH Dominance**: XX.X%
- **Fear & Greed Index**: XX (Fear/Neutral/Greed)

### Risk Factors
- Volatility level (compared to historical)
- Correlation with BTC
- Liquidity assessment
- Key levels to watch

### Trading Considerations
- Key support/resistance levels
- Volume analysis
- Momentum assessment
- Risk/reward setup
