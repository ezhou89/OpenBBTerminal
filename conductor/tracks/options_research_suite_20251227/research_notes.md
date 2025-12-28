# Research Notes: Existing Options Infrastructure

## Date: 2025-12-27

## Summary

The OpenBB codebase has **comprehensive existing options infrastructure** that covers most of Phase 1 and Phase 2 requirements. This significantly reduces the scope of work needed.

## Existing Standard Models

### 1. OptionsChainsData (`options_chains.py`)

**Location:** `openbb_platform/core/openbb_core/provider/standard_models/options_chains.py`

**60+ fields including:**
- Basic: `underlying_symbol`, `underlying_price`, `contract_symbol`, `expiration`, `dte`, `strike`, `option_type`
- Volume: `open_interest`, `volume`
- Pricing: `bid`, `ask`, `last_trade_price`, `mark`, `open`, `high`, `low`, `close`
- **Greeks:** `delta`, `gamma`, `theta`, `vega`, `rho`
- Volatility: `implied_volatility`, `change`, `change_percent`

**Built-in Analytics (OptionsChainsProperties mixin):**
- `filter_data()` - Advanced filtering
- `skew()` - Volatility skew analysis
- `straddle()` - Straddle strategy construction
- `strangle()` - Strangle strategy construction
- `synthetic_long()`, `synthetic_short()` - Synthetic positions
- `vertical_call()`, `vertical_put()` - Vertical spreads
- `strategies()` - Combined strategy analysis
- Properties: `expirations`, `strikes`, `has_iv`, `has_greeks`, `total_oi`, `total_volume`, `total_dex`, `total_gex`

### 2. OptionsSnapshotsData (`options_snapshots.py`)
- Market-wide options snapshot data
- Only implemented by Intrinio provider

### 3. OptionsUnusualData (`options_unusual.py`)
- Unusual options activity detection
- Only implemented by Intrinio provider

## Existing Provider Implementations

| Provider | Options Chains | Options Snapshots | Options Unusual | Free? |
|----------|---------------|-------------------|-----------------|-------|
| YFinance | Yes | No | No | Yes |
| CBOE | Yes | No | No | Yes |
| Intrinio | Yes | Yes | Yes | No (API key) |
| Tradier | Yes | No | No | No (API key) |
| TMX | Yes (Canadian) | No | No | Yes |
| Deribit | Yes (Crypto) | No | No | Yes |

### Provider-Specific Features

**Intrinio (most feature-rich):**
- `delay` parameter: EOD, realtime, delayed
- `model` parameter: black_scholes, bjerk
- Filtering: `strike_gt/lt`, `volume_gt/lt`, `oi_gt/lt`, `moneyness`

**CBOE:**
- `use_cache` parameter for company directory caching
- Free, official exchange data

**YFinance:**
- `in_the_money` field
- Free, reliable

## Existing Router Commands

**Location:** `openbb_platform/extensions/derivatives/openbb_derivatives/options/options_router.py`

1. `GET /derivatives/options/chains` - Full options chain
2. `POST /derivatives/options/surface` - 3D volatility surface with filtering
3. `GET /derivatives/options/unusual` - Unusual activity (Intrinio only)
4. `GET /derivatives/options/snapshots` - Market snapshot (Intrinio only)

## Gap Analysis

### Already Complete (Remove from Plan)
- [x] Options chain standard models
- [x] Options chain fetchers (YFinance, CBOE, Intrinio, Tradier)
- [x] Greeks fields in chain data
- [x] Basic strategy analysis (straddle, strangle, spreads)
- [x] Router commands for chains
- [x] Volatility surface visualization

### Still Needed
- [ ] Polygon.io options chain fetcher (if free tier supports it)
- [ ] Earnings calendar integration
- [ ] FDA/biotech catalyst calendar
- [ ] IV rank/percentile calculations
- [ ] Expected move calculations
- [ ] Catalyst-proximity options screener
- [ ] Unified research command combining chain + catalyst

## Recommendations

1. **Phase 1 (Options Chain Infrastructure)**: Mostly complete. Only need to:
   - Verify Polygon.io free tier supports options
   - Test existing implementations
   - Document capabilities

2. **Phase 2 (Greeks)**: Already complete in existing implementation

3. **Phase 3 (Catalyst Calendar)**: Full implementation needed - this is the main gap

4. **Phase 4 (Screener)**: Partial - filter_data() exists, need catalyst proximity

5. **Phase 5 (Analytics)**: Need IV rank/percentile, expected move

6. **Phase 6 (Integration)**: Create unified research workflow

## File References

- Standard models: `openbb_platform/core/openbb_core/provider/standard_models/`
- YFinance: `openbb_platform/providers/yfinance/openbb_yfinance/models/options_chains.py`
- CBOE: `openbb_platform/providers/cboe/openbb_cboe/models/options_chains.py`
- Intrinio: `openbb_platform/providers/intrinio/openbb_intrinio/models/options_chains.py`
- Router: `openbb_platform/extensions/derivatives/openbb_derivatives/options/options_router.py`
- Views: `openbb_platform/extensions/derivatives/openbb_derivatives/derivatives_views.py`
