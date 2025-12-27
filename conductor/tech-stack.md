# Tech Stack

## Core Technology

### Language: Python 3.9-3.13
**Rationale**: Dominant language in financial/data science ecosystem, strong typing support, excellent library ecosystem for financial analysis.

### Package Manager: Poetry
**Rationale**: Modern dependency management with lock files, better reproducibility than pip, supports complex multi-package monorepo structure.

## Backend

### API Framework: FastAPI
**Rationale**: High performance async support, automatic OpenAPI documentation, native Pydantic integration for data validation.

### Data Validation: Pydantic
**Rationale**: Type-safe data models, automatic serialization/deserialization, integrates seamlessly with FastAPI.

### HTTP Client: httpx / aiohttp
**Rationale**: Async support for parallel provider requests, connection pooling for performance.

## Architecture Patterns

### Provider Pattern (TET)
All data fetchers follow Transform-Extract-Transform:
1. `transform_query()` - Input params to provider-specific QueryParams
2. `extract_data()` - API request returning raw data
3. `transform_data()` - Raw data to standardized Data models

### Standardization Framework
- Standard models define shared schemas in `core/openbb_core/provider/standard_models/`
- Provider models inherit from standard models
- Enables cross-provider compatibility

## Testing

### Framework: pytest
**Rationale**: Industry standard, excellent fixture system, plugin ecosystem.

### Test Recording: VCR-style cassettes
**Rationale**: Record API responses for reliable, fast unit tests without hitting live APIs.

## Code Quality

### Formatter: Black
**Rationale**: Opinionated, deterministic formatting eliminates style debates.

### Linter: Ruff
**Rationale**: Fast, comprehensive linting covering E, W, F, Q, S, UP, I, PLC, PLE, PLR, PLW, SIM, T20 rules.

### Type Checker: mypy
**Rationale**: Static type checking for catching errors early.

### Pre-commit: Hooks
**Rationale**: Consistent quality gates before commits reach the repository.

## Deployment

### API Server: Uvicorn
**Rationale**: ASGI server with excellent async performance, hot reloading for development.

### Default Port: 6900 (via openbb-api) or 8000 (via uvicorn)
