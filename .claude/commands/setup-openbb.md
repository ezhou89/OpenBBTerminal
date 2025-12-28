# OpenBB Setup Helper

Help me set up OpenBB with: **$ARGUMENTS**

## Instructions

Based on the arguments, help with:
- `install` - Full installation guide
- `keys` or `credentials` - API key setup
- `providers` - List available data providers
- `test` - Test the installation
- `mcp` - Set up MCP server for Claude Code
- `cli` - CLI installation and usage

## Installation Guide

### Basic Installation
```bash
# Core platform (Python SDK)
pip install openbb

# With CLI
pip install openbb-cli

# With charting
pip install openbb-charting

# All providers
pip install openbb[all]
```

### Verify Installation
```python
from openbb import obb
print(obb.equity.price.quote("AAPL"))
```

## API Key Setup

### Free API Keys (Recommended)
1. **FRED** (Economic Data): https://fred.stlouisfed.org/docs/api/api_key.html
2. **FMP** (Extensive Data): https://site.financialmodelingprep.com/developer
3. **Polygon** (Market Data): https://polygon.io/

### Configure Credentials
```python
from openbb import obb

# Method 1: Runtime
obb.user.credentials.fred_api_key = "YOUR_KEY"
obb.user.credentials.fmp_api_key = "YOUR_KEY"

# Method 2: File (~/.openbb_platform/user_settings.json)
{
  "credentials": {
    "fred_api_key": "YOUR_FRED_KEY",
    "fmp_api_key": "YOUR_FMP_KEY",
    "polygon_api_key": "YOUR_POLYGON_KEY"
  }
}
```

## Free Data Sources (No API Key Required)
- **Yahoo Finance** - Stocks, options, fundamentals
- **SEC** - Company filings, insider trading
- **CBOE** - Options chains
- **Finviz** - Stock screener
- **Federal Reserve** - Economic data
- **ECB** - European data
- **FINRA** - Short interest

## MCP Server Setup for Claude Code

### Start MCP Server
```bash
pip install openbb-mcp-server
openbb-mcp --transport sse
```

### Configure VS Code
Add to your MCP settings:
```json
{
  "mcpServers": {
    "openbb": {
      "url": "http://localhost:8001/mcp/"
    }
  }
}
```

## Test Commands
```python
from openbb import obb

# Test free data (no key needed)
print(obb.equity.price.quote("AAPL", provider="yfinance"))
print(obb.equity.fundamental.metrics("AAPL", provider="yfinance"))

# Test SEC data
print(obb.equity.ownership.insider_trading("AAPL"))

# Test FRED (needs key)
print(obb.economy.cpi())
```

## Common Issues

### Import Error
```bash
# Rebuild the package
python -c "import openbb; openbb.build()"
```

### Provider Not Found
```bash
# Install specific provider
pip install openbb-yfinance
pip install openbb-fred
```

### Credential Error
```python
# Check credentials
print(obb.user.credentials)
```

## Quick Start for Traders
```python
from openbb import obb

# Stock quote
obb.equity.price.quote("AAPL")

# Historical prices
obb.equity.price.historical("AAPL", start_date="2024-01-01")

# Technical analysis
data = obb.equity.price.historical("AAPL")
obb.technical.rsi(data=data)

# Options chain
obb.derivatives.options.chains("AAPL")

# News
obb.news.company("AAPL", limit=10)
```
