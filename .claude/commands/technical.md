# Technical Analysis Command

Perform technical analysis for: **$ARGUMENTS**

## Instructions

Use OpenBB to calculate and analyze technical indicators for the given symbol:

### 1. Get Price Data
```python
from openbb import obb
symbol = "$ARGUMENTS".upper().strip()

# Get historical data (6 months for good indicator calculation)
data = obb.equity.price.historical(symbol, start_date="2024-06-01")
df = data.to_df()
```

### 2. Calculate Key Indicators
```python
# Trend Indicators
sma_20 = obb.technical.sma(data=data, length=20)
sma_50 = obb.technical.sma(data=data, length=50)
sma_200 = obb.technical.sma(data=data, length=200)
ema_12 = obb.technical.ema(data=data, length=12)
macd = obb.technical.macd(data=data)

# Momentum Indicators
rsi = obb.technical.rsi(data=data, length=14)
stoch = obb.technical.stoch(data=data)

# Volatility Indicators
bbands = obb.technical.bbands(data=data)
atr = obb.technical.atr(data=data)

# Volume Indicators
obv = obb.technical.obv(data=data)
```

## Output Format

Provide analysis including:

### Trend Analysis
- **Moving Averages** - Current position vs SMA 20/50/200
- **MACD** - Signal line crossovers, histogram direction
- **Trend Direction** - Bullish/Bearish/Neutral

### Momentum Analysis
- **RSI (14)** - Overbought (>70) / Oversold (<30) / Neutral
- **Stochastic** - %K and %D readings

### Volatility Analysis
- **Bollinger Bands** - Position within bands, squeeze detection
- **ATR** - Current volatility level

### Volume Analysis
- **OBV Trend** - Confirming or diverging from price

### Support & Resistance
- Identify key levels based on recent price action

### Trading Signals
- List any buy/sell signals from the indicators
- Overall technical outlook (Bullish/Neutral/Bearish)

### Risk Levels
- Suggested stop-loss based on ATR
- Key support levels for risk management
