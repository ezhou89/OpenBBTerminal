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
- [ ] Task: Conductor - User Manual Verification 'Options Infrastructure' (Protocol in workflow.md)

## Phase 2: Catalyst Calendar Integration

- [ ] Task: Research free earnings calendar APIs (Yahoo Finance, FMP, Alpha Vantage)
- [ ] Task: Create standard models for EarningsCalendar (QueryParams and Data)
- [ ] Task: Implement earnings calendar fetcher for FMP or alternative provider
- [ ] Task: Write unit tests for earnings calendar fetcher
- [ ] Task: Research FDA calendar / ClinicalTrials.gov API
- [ ] Task: Create standard models for CatalystEvent (generic catalyst type)
- [ ] Task: Implement FDA/biotech catalyst fetcher
- [ ] Task: Write unit tests for catalyst fetcher
- [ ] Task: Create calendar router commands in appropriate extension
- [ ] Task: Conductor - User Manual Verification 'Catalyst Calendar' (Protocol in workflow.md)

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
