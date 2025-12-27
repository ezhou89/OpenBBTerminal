# Python Style Guide

## Formatting

- **Line Length**: 122 characters
- **Formatter**: Black (run via pre-commit)
- **Quotes**: Double quotes preferred

## Linting (Ruff)

Enabled rule sets: E, W, F, Q, S, UP, I, PLC, PLE, PLR, PLW, SIM, T20

Key rules:
- No unused imports
- No undefined names
- Security checks enabled
- Simplification suggestions enforced

## Type Hints

- All public functions must have type hints
- Use `from __future__ import annotations` for forward references
- Prefer specific types over `Any`
- Use mypy for static type checking

```python
def get_data(symbol: str, start_date: date | None = None) -> list[dict]:
    ...
```

## Imports

Order (enforced by isort via Ruff):
1. Standard library
2. Third-party packages
3. Local imports

Standard aliases:
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

## Docstrings

NumPy convention:

```python
def fetch_options_chain(symbol: str, expiration: date | None = None) -> OBBject:
    """Fetch options chain data for a symbol.

    Parameters
    ----------
    symbol : str
        The ticker symbol to fetch options for.
    expiration : date, optional
        Specific expiration date to filter by.

    Returns
    -------
    OBBject
        Container with options chain data.

    Examples
    --------
    >>> from openbb import obb
    >>> data = obb.derivatives.options.chains("AAPL")
    """
```

## Classes

### Data Models (Pydantic)

```python
from pydantic import Field
from openbb_core.provider.abstract.data import Data

class OptionsChainData(Data):
    """Options chain data model."""

    contract_symbol: str = Field(description="The option contract symbol.")
    strike: float = Field(description="Strike price.")
    expiration: date = Field(description="Expiration date.")
    option_type: Literal["call", "put"] = Field(description="Option type.")
```

### Fetchers (TET Pattern)

```python
class MyFetcher(Fetcher[QueryParams, list[Data]]):
    """Fetcher for my data."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> QueryParams:
        """Transform input parameters."""
        return QueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: QueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict:
        """Extract raw data from provider."""
        ...

    @staticmethod
    def transform_data(
        query: QueryParams,
        data: dict,
        **kwargs: Any,
    ) -> list[Data]:
        """Transform raw data to standardized models."""
        ...
```

## Error Handling

- Use specific exception types
- Provide actionable error messages
- Never silently swallow exceptions

```python
from openbb_core.provider.utils.errors import OpenBBError

if not data:
    raise OpenBBError(f"No data found for symbol: {symbol}")
```

## Testing

- Test files mirror source structure in `tests/` directory
- Use descriptive test names: `test_fetch_options_chain_returns_valid_data`
- Use fixtures for common setup
- Mock external API calls in unit tests
