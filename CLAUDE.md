# CLAUDE.md - OpenBB Platform Developer Guide

This document provides guidance for AI assistants working with the OpenBB Platform codebase.

## Project Overview

OpenBB Platform is an open-source financial data platform that provides unified access to equity, options, crypto, forex, macro economy, fixed income, and more from multiple data providers. It consists of:

- **Core**: The main infrastructure package (`openbb_platform/core/`)
- **Extensions**: Feature modules like equity, crypto, currency (`openbb_platform/extensions/`)
- **Providers**: Data source connectors like yfinance, fmp, polygon (`openbb_platform/providers/`)
- **CLI**: Command-line interface (`cli/`)

## Directory Structure

```
OpenBBTerminal/
├── openbb_platform/           # Main platform code
│   ├── core/                  # Core infrastructure
│   │   └── openbb_core/
│   │       ├── api/           # REST API (FastAPI)
│   │       ├── app/           # Application logic
│   │       └── provider/      # Provider framework
│   │           ├── abstract/  # Base classes (Data, QueryParams, Fetcher)
│   │           └── standard_models/  # Standardized data models
│   ├── extensions/            # Feature extensions (equity, crypto, etc.)
│   ├── providers/             # Data provider implementations
│   ├── obbject_extensions/    # OBBject extensions (charting)
│   ├── dev_install.py         # Development installation script
│   └── pyproject.toml         # Main package dependencies
├── cli/                       # Command-line interface
│   ├── openbb_cli/            # CLI source code
│   └── tests/                 # CLI tests
├── .github/
│   └── workflows/             # CI/CD workflows
└── examples/                  # Usage examples
```

## Development Setup

### Prerequisites
- Python 3.9.21 - 3.13
- Poetry (`pip install poetry`)
- Git

### Installation for Development

```bash
# Clone the repository
git clone https://github.com/OpenBB-finance/OpenBB.git
cd OpenBB

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows

# Install poetry
pip install poetry

# Navigate to platform directory
cd openbb_platform

# Install in development mode (all packages)
python dev_install.py -e

# To also install CLI
python dev_install.py -e -c
```

### Rebuilding the Package

After installing new extensions:
```python
python -c "import openbb; openbb.build()"
```

## Code Style and Conventions

### Linting Tools (Pre-commit Hooks)

The project uses these linters (configured in `.pre-commit-config.yaml`):
- **Black**: Code formatting (line length: 122)
- **Ruff**: Fast Python linter
- **Pylint**: Static analysis
- **MyPy**: Type checking
- **Pydocstyle**: Docstring conventions (NumPy style)
- **Codespell**: Spell checking
- **Bandit**: Security linting

### Key Style Rules

```python
# Line length: 122 characters
# Target Python version: 3.9+

# Import conventions (from ruff.toml)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Docstring style: NumPy convention
def example_function(param1: str, param2: int) -> bool:
    """Short description.

    Parameters
    ----------
    param1 : str
        Description of param1.
    param2 : int
        Description of param2.

    Returns
    -------
    bool
        Description of return value.
    """
    pass
```

### Type Hints

Always use type hints for function signatures:
```python
from typing import Any, Dict, List, Optional, Union

def process_data(
    query: QueryParams,
    credentials: Optional[Dict[str, str]],
    **kwargs: Any,
) -> List[Data]:
    ...
```

## Architecture Patterns

### The TET Pattern (Transform, Extract, Transform)

All Fetcher classes follow the TET pattern:

```python
from openbb_core.provider.abstract.fetcher import Fetcher

class MyProviderEquityHistoricalFetcher(
    Fetcher[
        MyProviderEquityHistoricalQueryParams,
        List[MyProviderEquityHistoricalData],
    ]
):
    """Transform the query, extract and transform the data."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> MyProviderEquityHistoricalQueryParams:
        """Transform query parameters."""
        return MyProviderEquityHistoricalQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: MyProviderEquityHistoricalQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> Dict:
        """Extract raw data from API."""
        # Make API request here
        return raw_data

    @staticmethod
    def transform_data(
        query: MyProviderEquityHistoricalQueryParams,
        data: Dict,
        **kwargs: Any,
    ) -> List[MyProviderEquityHistoricalData]:
        """Transform raw data to standard format."""
        return [MyProviderEquityHistoricalData.model_validate(d) for d in data]
```

### Standard Models

Standard models are in `openbb_platform/core/openbb_core/provider/standard_models/`. Provider-specific models inherit from these:

```python
from openbb_core.provider.standard_models.equity_historical import (
    EquityHistoricalData,
    EquityHistoricalQueryParams,
)

class MyProviderEquityHistoricalQueryParams(EquityHistoricalQueryParams):
    """Provider-specific query parameters."""
    # Add provider-specific fields
    custom_field: str = Field(default="value", description="Custom field.")

class MyProviderEquityHistoricalData(EquityHistoricalData):
    """Provider-specific data model."""
    # Add provider-specific fields
    extra_field: Optional[float] = Field(default=None)
```

### Router Commands

Extension routers define API endpoints:

```python
from openbb_core.app.router import Router
from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject

router = Router(prefix="", description="My extension.")

@router.command(
    model="EquityHistorical",
    examples=[APIEx(parameters={"symbol": "AAPL", "provider": "yfinance"})],
)
async def historical(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Get historical price data."""
    return await OBBject.from_query(Query(**locals()))
```

### Provider Registration

Providers are registered in `__init__.py`:

```python
from openbb_core.provider.abstract.provider import Provider

my_provider = Provider(
    name="my_provider",
    website="https://example.com",
    description="Provider description.",
    credentials=["api_key"],  # Required credentials
    fetcher_dict={
        "EquityHistorical": MyProviderEquityHistoricalFetcher,
        # Map standard model names to fetchers
    },
)
```

Entry point in `pyproject.toml`:
```toml
[tool.poetry.plugins."openbb_provider_extension"]
my_provider = "openbb_my_provider:my_provider"
```

## Testing

### Test Structure

```
openbb_platform/
├── tests/                     # Platform-level tests
├── core/tests/                # Core tests
├── extensions/*/tests/        # Extension tests
└── providers/*/tests/         # Provider tests
    ├── test_*_fetchers.py     # Fetcher unit tests
    └── record/                # Recorded API responses
```

### Running Tests

```bash
# Run all unit tests (excludes integration tests)
pytest openbb_platform -m "not integration"

# Run integration tests only
pytest openbb_platform -m integration

# Run specific provider tests
pytest openbb_platform/providers/yfinance/tests/

# Run with coverage
pytest openbb_platform --cov=openbb_platform -m "not integration"
```

### Test Markers

- `integration`: Integration tests (require API keys/network)
- `linux`: Tests that only work on Linux

### Generating Tests

```bash
# Generate unit tests for fetchers
python openbb_platform/providers/tests/utils/unit_tests_generator.py

# Record test fixtures
pytest path/to/test_file.py --record=all
```

## Git Workflow

### Branch Naming

- `feature/feature-name` - New features
- `hotfix/hotfix-name` - Bug fixes

PRs should target the `develop` branch.

### Pre-commit Hooks

Install pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

### Important: Generated Files

Never commit files in `openbb_platform/core/openbb/package/` except `__init__.py`. These are auto-generated.

## CI/CD Workflows

- **general-linting.yml**: Runs on PRs - Black, MyPy, Pydocstyle, Pylint, Ruff
- **test-unit-platform.yml**: Platform unit tests (Python 3.9-3.13)
- **test-unit-cli.yml**: CLI unit tests
- **codeql.yml**: Security analysis

## Key Classes and Imports

```python
# Data models
from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.provider import Provider

# Router and commands
from openbb_core.app.router import Router
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.query import Query

# Provider interface
from openbb_core.app.provider_interface import (
    ExtraParams,
    ProviderChoices,
    StandardParams,
)

# Pydantic
from pydantic import Field, field_validator
```

## Error Handling

| Status Code | Exception | Use Case |
|-------------|-----------|----------|
| 400 | `OpenBBError` | Custom exceptions like `EmptyDataError` |
| 422 | `ValidationError` | Pydantic validation errors |
| 500 | Other exceptions | Unexpected errors |

```python
from openbb_core.provider.utils.errors import EmptyDataError

if not data:
    raise EmptyDataError("No data found for the given query.")
```

## REST API

Start the API server:
```bash
uvicorn openbb_core.api.rest_api:app --host 0.0.0.0 --port 8000 --reload
```

API docs available at `http://localhost:8000/docs`

## Common Tasks

### Adding a New Data Point to Existing Provider

1. Create query params and data models in `providers/<name>/openbb_<name>/models/`
2. Create a Fetcher class following TET pattern
3. Add Fetcher to provider's `__init__.py` `fetcher_dict`
4. Add tests in `providers/<name>/tests/`

### Adding a New Provider

1. Create directory structure: `providers/<name>/openbb_<name>/`
2. Create `__init__.py` with `Provider` definition
3. Create `pyproject.toml` with entry point
4. Implement Fetchers for desired standard models
5. Add tests

### Adding a New Extension

1. Create directory: `extensions/<name>/openbb_<name>/`
2. Create router file with `@router.command` decorators
3. Configure `pyproject.toml` with entry point
4. Add to `dev_install.py` LOCAL_DEPS if needed

## Documentation Resources

- Full documentation: https://docs.openbb.co/platform
- API Reference: https://docs.openbb.co/platform/reference
- Contributing Guide: `openbb_platform/CONTRIBUTING.md`
