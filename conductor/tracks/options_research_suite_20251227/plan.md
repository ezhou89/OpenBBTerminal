# Plan: Options Research Suite for Catalyst Trading

> **Note:** Research completed 2025-12-27 revealed extensive existing options infrastructure.
> Plan updated to focus on gaps: catalyst calendars, IV analytics, and unified research workflow.
> See [research_notes.md](research_notes.md) for full findings.

## Phase 1: Validate & Extend Options Infrastructure

- [x] Task: Research existing options chain implementations in OpenBB codebase (e0ae643)
- [x] Task: Test existing YFinance options chain fetcher with sample symbols
- [x] Task: Test existing CBOE options chain fetcher with sample symbols
- [x] Task: Verify Greeks are calculated correctly in existing implementation (provider-sourced)
- [x] Task: Research Polygon.io free tier options API availability (low priority, limited free tier)
- [x] Task: Conductor - User Manual Verification 'Options Infrastructure' (Protocol in workflow.md)

## Phase 1 Checkpoint [a6abe68]
> Options infrastructure validated. YFinance, CBOE functional. Greeks provider-sourced. Polygon.io low priority.

## Phase 2: Catalyst Calendar Integration

> **Note:** Research completed 2025-12-27 revealed earnings calendar already fully implemented.
> 4 providers exist: FMP, Nasdaq, Seeking Alpha, TMX. See [research_notes.md](research_notes.md).

- [x] Task: Research free earnings calendar APIs (Yahoo Finance, FMP, Alpha Vantage) - ALREADY EXISTS
- [x] Task: Create standard models for EarningsCalendar (QueryParams and Data) - ALREADY EXISTS at calendar_earnings.py
- [x] Task: Implement earnings calendar fetcher for FMP or alternative provider - ALREADY EXISTS (4 providers!)
- [x] Task: Write unit tests for earnings calendar fetcher - Tests exist for all 4 providers
- [x] Task: Research FDA calendar / ClinicalTrials.gov API - ClinicalTrials.gov API v2 recommended (free, official)
- [x] Task: Create standard models for ClinicalTrials (QueryParams and Data)
- [x] Task: Implement ClinicalTrials.gov fetcher using API v2 - NIH provider created
- [x] Task: Write unit tests for ClinicalTrials fetcher
- [x] Task: Create calendar router command for clinical trials (added to equity calendar)
- [ ] Task: Conductor - User Manual Verification 'Catalyst Calendar' (Protocol in workflow.md)

> **Note:** PDUFA calendar deferred - no free API available. See research_notes.md.

## Phase 2 Checkpoint [7655589]
> Catalyst calendar integration complete:
> - Earnings calendar: 4 existing providers (FMP, Nasdaq, Seeking Alpha, TMX)
> - Clinical trials: New NIH provider with ClinicalTrials.gov API v2
> - PDUFA calendar: Deferred (no free API)

## Phase 3: IV Analytics & Expected Move

- [ ] Task: Implement IV rank calculation (current IV vs 52-week range)
- [ ] Task: Write unit tests for IV rank calculation
- [ ] Task: Implement IV percentile calculation (% of days IV was lower)
- [ ] Task: Write unit tests for IV percentile calculation
- [ ] Task: Implement expected move calculation from ATM straddle IV
- [ ] Task: Write unit tests for expected move calculation
- [ ] Task: Add IV analytics to options chain data or separate utility
- [ ] Task: Conductor - User Manual Verification 'IV Analytics' (Protocol in workflow.md)

## Phase 4: Catalyst-Aware Options Screener

- [ ] Task: Design catalyst proximity filter interface
- [ ] Task: Implement options screener that combines chain data with catalyst dates
- [ ] Task: Write unit tests for catalyst proximity screening
- [ ] Task: Implement "options before earnings" screen
- [ ] Task: Write unit tests for earnings screen
- [ ] Task: Create screener router command
- [ ] Task: Conductor - User Manual Verification 'Options Screener' (Protocol in workflow.md)

## Phase 5: Unified Research Workflow

- [ ] Task: Create unified options research command combining chain + catalyst + IV analytics
- [ ] Task: Write integration tests for full research workflow
- [ ] Task: Add CLI integration for catalyst commands
- [ ] Task: Add comprehensive docstrings and examples
- [ ] Task: Run full test suite and fix any regressions
- [ ] Task: Conductor - User Manual Verification 'Integration' (Protocol in workflow.md)

---

## Task Status Legend

- `[ ]` - Not started
- `[~]` - In progress
- `[x]` - Completed (commit SHA appended, e.g., `[x] (abc1234)`)

## Phase Changes from Original Plan

**Removed (Already Exists):**
- Create standard models for OptionsChain (exists in `options_chains.py`)
- Implement Yahoo Finance/CBOE/Intrinio fetchers (all exist)
- Greeks calculation engine (Greeks already in chain data)
- Strategy analysis (straddle, strangle, spreads already in OptionsChainsProperties)

**Refocused:**
- Phase 1: Validate existing infrastructure, extend if gaps found
- Phase 2: Catalyst calendar (main new development)
- Phase 3: IV analytics (new calculations)
- Phase 4: Catalyst-aware screener (new feature)
- Phase 5: Integration (combine new with existing)

## Notes

- Each task should follow TDD: write failing test first, then implement, then refactor
- Commit after each task completion with appropriate commit message format
- Run linting (`pre-commit run --all-files`) before marking tasks complete
- Leverage existing `OptionsChainsProperties.filter_data()` for screener foundation
