# Portfolio Analysis Command

Analyze the following portfolio: **$ARGUMENTS**

## Instructions

Parse the portfolio from the arguments. Expected format examples:
- `AAPL:30, GOOGL:25, MSFT:20, AMZN:15, TSLA:10` (percentages)
- `AAPL 100, GOOGL 50, MSFT 75` (share counts - will estimate weights)
- `AAPL, GOOGL, MSFT, AMZN` (equal weight assumed)

### 1. Get Portfolio Data
```python
from openbb import obb
import pandas as pd

# Parse holdings from arguments
holdings_str = "$ARGUMENTS"

# Get historical data for each holding
# Calculate returns, correlations, and metrics
```

### 2. Performance Analysis
```python
# For each symbol, get historical prices
# Calculate portfolio returns with weights
# Compare to benchmark (SPY)
```

### 3. Risk Analysis
```python
# Calculate portfolio metrics
from openbb import obb

# For the portfolio data, calculate:
# - Sharpe Ratio
# - Sortino Ratio
# - Max Drawdown
# - Volatility
# - Beta vs SPY
```

### 4. Correlation Matrix
```python
# Calculate correlation between holdings
# Identify concentration risk
```

## Output Format

### Portfolio Summary
| Symbol | Weight | Current Price | Day Change | Total Return |
|--------|--------|---------------|------------|--------------|

### Performance Metrics
- **Total Return (YTD)**: X%
- **Annualized Return**: X%
- **Volatility (Annualized)**: X%
- **Sharpe Ratio**: X.XX
- **Sortino Ratio**: X.XX
- **Max Drawdown**: X%
- **Beta (vs SPY)**: X.XX

### Risk Analysis
- **Correlation Matrix** - Show heatmap of correlations
- **Sector Concentration** - Breakdown by sector
- **Top Risk Contributors** - Which holdings add most volatility

### Diversification Score
- Rate diversification (1-10) based on correlation and sector exposure

### Recommendations
- Suggest rebalancing if any position is overweight
- Identify missing sectors for better diversification
- Flag any high-correlation pairs
