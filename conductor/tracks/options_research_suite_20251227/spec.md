# Spec: Options Research Suite for Catalyst Trading

## Overview

A comprehensive options research toolkit designed for trading around expected catalysts like earnings calls, FDA approvals, and clinical trial readouts. This suite provides options chain data, Greeks calculations, screening capabilities, and analytics tools to help traders identify and evaluate options opportunities ahead of known market-moving events.

## Core Requirements

### 1. Options Chain Data
- Fetch complete options chains from multiple free providers (CBOE, Yahoo Finance, Polygon.io)
- Standardize chain data across providers using TET pattern
- Support filtering by expiration date, strike range, and option type (calls/puts)
- Include essential fields: strike, expiration, bid, ask, last, volume, open interest, IV

### 2. Options Greeks Calculation
- Calculate core Greeks: Delta, Gamma, Theta, Vega, Rho
- Support multiple pricing models (Black-Scholes, Binomial)
- Handle American vs European style options appropriately
- Provide Greeks at individual option and portfolio level

### 3. Catalyst Calendar Integration
- Integrate earnings calendar API (free providers)
- Integrate FDA calendar / biotech catalyst API
- Track clinical trial readout dates (ClinicalTrials.gov or similar)
- Allow user-defined catalyst events
- Link catalysts to relevant ticker symbols

### 4. Options Screener
- Screen options by:
  - Implied volatility (absolute and percentile)
  - Volume and open interest thresholds
  - Bid-ask spread (liquidity filter)
  - Days to expiration
  - Moneyness (ITM, ATM, OTM)
  - Upcoming catalyst proximity
- Support multi-criteria screening with AND/OR logic

### 5. Options Analytics
- Calculate expected move based on IV
- Compare IV to historical volatility (IV rank, IV percentile)
- P&L scenario analysis (price at expiration)
- Basic strategy analysis (spreads, straddles, strangles)
- Risk/reward visualization data

## Technical Considerations

- **Provider Pattern**: All fetchers follow TET (Transform-Extract-Transform)
- **Standard Models**: Create/extend standard models in `core/openbb_core/provider/standard_models/`
- **Async Support**: Use `aextract_data` for API calls (httpx/aiohttp)
- **Rate Limiting**: Respect provider rate limits, implement backoff
- **Caching**: Consider caching chain data with appropriate TTL
- **Error Handling**: Graceful degradation when providers fail
- **Testing**: VCR-style cassettes for reliable unit tests

## Acceptance Criteria

### Options Chains
- [ ] Can fetch options chain for any US equity symbol
- [ ] Data includes all standard fields (strike, expiration, bid/ask, volume, OI, IV)
- [ ] At least 2 providers implemented (Yahoo Finance, one other)
- [ ] Chain data is properly standardized across providers

### Greeks
- [ ] Delta, Gamma, Theta, Vega calculated for all options in chain
- [ ] Greeks values validated against known benchmarks
- [ ] Black-Scholes model implemented correctly
- [ ] Unit tests cover edge cases (deep ITM/OTM, near expiration)

### Catalyst Calendar
- [ ] Earnings dates fetchable for any US equity
- [ ] FDA calendar accessible for biotech tickers
- [ ] User can add custom catalyst events
- [ ] Catalysts linked to ticker symbols

### Screener
- [ ] Filter by IV percentile works correctly
- [ ] Volume/OI filters return expected results
- [ ] Expiration date range filtering works
- [ ] Combined filters produce accurate results

### Analytics
- [ ] Expected move calculation matches industry standard
- [ ] IV rank/percentile calculated correctly
- [ ] Basic P&L scenarios generated accurately

## Out of Scope

- Real-time streaming quotes (focus on snapshot data)
- Paid data provider integrations (premium providers)
- Automated trade execution
- Complex multi-leg strategy builders (beyond basic spreads)
- Backtesting framework
- Portfolio management / position tracking

## Dependencies

- **Existing OpenBB options infrastructure (CONFIRMED):**
  - Standard models: `OptionsChainsData`, `OptionsSnapshotsData`, `OptionsUnusualData`
  - Providers: YFinance, CBOE, Intrinio, Tradier (all implemented)
  - Greeks: Already included in chain data fields
  - Strategy analysis: Built into `OptionsChainsProperties` mixin
  - Router: `/derivatives/options/chains`, `/derivatives/options/surface`
- Earnings/catalyst calendar APIs (to be implemented)
- Python scientific libraries (for IV calculations)

## Data Providers to Integrate

| Provider | Data Type | Priority | Notes |
|----------|-----------|----------|-------|
| Yahoo Finance | Chains, Earnings | High | Free, reliable |
| CBOE | Chains | High | Official exchange |
| Polygon.io | Chains | Medium | Free tier available |
| Financial Modeling Prep | Earnings | Medium | Free tier |
| FDA.gov | FDA Calendar | Medium | Official source |
| ClinicalTrials.gov | Trials | Low | API available |
