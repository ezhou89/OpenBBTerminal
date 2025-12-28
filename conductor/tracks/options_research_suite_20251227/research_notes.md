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

## Greeks Verification (2025-12-27)

**Key Finding: Greeks are PROVIDER-SOURCED, not calculated by OpenBB**

| Aspect | Details |
|--------|---------|
| **Source** | Data providers return Greeks from their APIs |
| **Fields** | delta, gamma, theta, vega, rho (all optional) |
| **OpenBB calculates** | DEX, GEX from provider-supplied Greeks |
| **`has_greeks` property** | Returns True if provider returned Greeks |

**How it works:**
1. Providers fetch Greeks from their data sources (e.g., Yahoo Finance API, CBOE data)
2. Greeks are optional fields - some providers may not return them
3. OpenBB uses provider Greeks to calculate:
   - DEX (Delta Exposure) = delta * contract_size * OI * underlying_price
   - GEX (Gamma Exposure) = gamma * contract_size * OI * price² * 0.01
4. Intrinio offers `model` parameter to select pricing model (black_scholes or bjerk)

**Implications:**
- No need to implement Black-Scholes ourselves
- Greeks accuracy depends on provider implementation
- If provider doesn't supply Greeks, they'll be None

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

## Polygon.io Research (2025-12-27)

**Finding: Polygon.io not a priority for options chain implementation**

| Aspect | Details |
|--------|---------|
| **Current Status** | OpenBB has Polygon provider, but NO options support |
| **Rebrand** | Polygon.io now Massive.com |
| **Free Tier** | EOD options data, 5 API calls/minute (very limited) |
| **Paid Tiers** | $29/month+ for better access |

**Recommendation:** Low priority. YFinance and CBOE already provide free options data with better rate limits. Polygon.io options could be added later if specific features are needed.

Sources:
- [Polygon.io Pricing](https://polygon.io/pricing)
- [Massive.com Pricing](https://massive.com/pricing)

## Earnings Calendar Research (2025-12-27)

**Finding: Comprehensive earnings calendar already exists in OpenBB**

### Existing Standard Model

**Location:** `openbb_platform/core/openbb_core/provider/standard_models/calendar_earnings.py`

**Query Parameters:**
- `start_date` - Start date for calendar range
- `end_date` - End date for calendar range

**Standard Data Fields:**
- `report_date` - Date of the earnings report
- `symbol` - Ticker symbol
- `name` - Company name (optional)
- `eps_previous` - EPS from same period last year
- `eps_consensus` - Analyst consensus EPS estimate

### Provider Implementations

| Provider | Free? | Extra Fields | Notes |
|----------|-------|--------------|-------|
| **FMP** | No (API key) | eps_actual, revenue_consensus, revenue_actual, last_updated | Requires FMP API key |
| **Nasdaq** | Yes | eps_actual, surprise_percent, num_estimates, period_ending, previous_report_date, reporting_time, market_cap | Free, rich data |
| **Seeking Alpha** | Yes | market_cap, reporting_time, exchange, sector_id | Free, supports US/CA |
| **TMX** | Yes | Various (Canadian focus) | Free, Canadian markets |

### Router Command

**Endpoint:** `GET /equity/calendar/earnings`

**Example:**
```python
from openbb import obb
# Get earnings for next 3 days
earnings = obb.equity.calendar.earnings(provider="nasdaq")
# Get earnings for specific dates
earnings = obb.equity.calendar.earnings(
    start_date="2024-02-01",
    end_date="2024-02-07",
    provider="fmp"
)
```

### Other Calendar Types (Also Exist)

| Calendar | Router | Providers |
|----------|--------|-----------|
| **IPO** | `/equity/calendar/ipo` | Intrinio, Nasdaq |
| **Dividend** | `/equity/calendar/dividend` | FMP, Nasdaq |
| **Splits** | `/equity/calendar/splits` | FMP |
| **Events** | `/equity/calendar/events` | FMP (deprecated) |

### Gap Analysis for Catalyst Calendar

**Already Complete:**
- [x] Earnings calendar standard model
- [x] Earnings calendar providers (4 providers)
- [x] Earnings calendar router command
- [x] IPO, dividend, splits calendars

**Still Needed:**
- [ ] FDA approval calendar (biotech catalysts)
- [ ] Clinical trial readout calendar (ClinicalTrials.gov)
- [ ] Generic "catalyst" event type that combines multiple sources
- [ ] User-defined catalyst events

### Implications for Phase 2

Most of Phase 2 (Catalyst Calendar Integration) is already complete for earnings. The plan should be updated to:

1. ~~Research free earnings calendar APIs~~ → Already exists
2. ~~Create standard models for EarningsCalendar~~ → Already exists
3. ~~Implement earnings calendar fetcher~~ → Already exists (4 providers!)
4. Research FDA calendar / ClinicalTrials.gov API → **Still needed**
5. Create standard models for CatalystEvent → **Still needed**
6. Implement FDA/biotech catalyst fetcher → **Still needed**

## FDA Calendar / ClinicalTrials.gov Research (2025-12-27)

### ClinicalTrials.gov API (FREE, Official - Recommended)

**Status:** Excellent option for clinical trial catalyst tracking

| Aspect | Details |
|--------|---------|
| **API Version** | v2.0 (REST API with OpenAPI 3.0 spec) |
| **Base URL** | `https://clinicaltrials.gov/api/v2/studies` |
| **Auth** | No API key required (FREE) |
| **Format** | JSON response, ISO 8601 dates |

**Key Date Fields Available:**
- `primaryCompletionDate` - When data collection for primary outcomes completes
- `completionDate` (study completion) - Last participant's last visit
- `startDate` - Trial start
- `firstPostedDate`, `lastUpdatePostedDate`, `resultsFirstPostedDate`

**API Endpoints:**
1. `GET /api/v2/studies` - Search trials with filters
2. `GET /api/v2/studies/{NCT_ID}` - Get specific trial details

**Query Parameters:**
- `query.cond` - Condition/disease (e.g., "breast cancer")
- `query.intr` - Intervention/drug name
- `query.spons` - Sponsor/company name
- `filter.overallStatus` - Recruitment status
- Date range syntax: `AREA[LastUpdatePostDate]RANGE[2023-01-15,MAX]`

**Python Package:** `pytrials` available on PyPI
```python
from pytrials.client import ClinicalTrials
ct = ClinicalTrials()
# Get studies by search term
studies = ct.get_full_studies(search_expr="Pfizer", max_studies=50)
```

**Use Case for Catalyst Trading:**
- Query trials by company/drug name
- Get Primary Completion Date for upcoming readouts
- Filter by phase (Phase 3 for major catalysts)
- Track trial status changes

### openFDA API (FREE, Official - Limited Use)

**Status:** Useful for historical data, NOT for upcoming approvals

| Aspect | Details |
|--------|---------|
| **Base URL** | `https://api.fda.gov/drug/` |
| **Auth** | No API key required (FREE) |
| **Rate Limits** | 240 requests/minute without key |

**Available Endpoints:**
1. `/drug/event` - Adverse event reports
2. `/drug/label` - Drug labeling/prescribing info
3. `/drug/ndc` - NDC Directory
4. `/drug/enforcement` - Recall reports
5. `/drug/drugsfda` - Historical approvals since 1939

**Key Limitation:** No upcoming PDUFA dates or pending approvals. Only historical data.

### PDUFA Calendar Services (Commercial - Not Recommended)

**Status:** No free API available for upcoming FDA approval dates

| Service | Free Tier | API Available |
|---------|-----------|---------------|
| FDA Tracker | Limited | Unknown |
| RTTNews | Trial only | Paid |
| BiopharmIQ | Limited | Paid |
| BioPharmCatalyst | Limited | Unknown |
| Unusual Whales | Partial | Unknown |

**Why Not Recommended:**
- Most require paid subscriptions
- No documented free Python API
- Would require web scraping (ToS concerns)
- Out of scope for "free providers" requirement

### Recommendations for Phase 2

1. **Implement ClinicalTrials.gov fetcher** (HIGH PRIORITY)
   - Free, official API with rich data
   - Primary Completion Date ideal for catalyst tracking
   - Can filter by company/drug to get relevant trials
   - pytrials package simplifies implementation

2. **Skip PDUFA calendar for now** (DEFERRED)
   - No free API available
   - Could add later if paid provider integration requested

3. **Use openFDA for supplemental data** (LOW PRIORITY)
   - Historical approval context
   - Drug labeling information

### Integration with Options Research

**Workflow for catalyst-aware options trading:**
1. Query ClinicalTrials.gov for company's active trials
2. Get Primary Completion Dates for Phase 3 trials
3. Combine with existing earnings calendar
4. Screen options expiring after catalyst dates
5. Analyze IV around expected readout dates

## File References

- Standard models: `openbb_platform/core/openbb_core/provider/standard_models/`
- YFinance: `openbb_platform/providers/yfinance/openbb_yfinance/models/options_chains.py`
- CBOE: `openbb_platform/providers/cboe/openbb_cboe/models/options_chains.py`
- Intrinio: `openbb_platform/providers/intrinio/openbb_intrinio/models/options_chains.py`
- Router: `openbb_platform/extensions/derivatives/openbb_derivatives/options/options_router.py`
- Views: `openbb_platform/extensions/derivatives/openbb_derivatives/derivatives_views.py`
- Earnings Calendar: `openbb_platform/core/openbb_core/provider/standard_models/calendar_earnings.py`
- Calendar Router: `openbb_platform/extensions/equity/openbb_equity/calendar/calendar_router.py`
