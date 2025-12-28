# OpenBB NIH Provider

This extension adds support for data from the National Institutes of Health (NIH).

## Data Sources

- **ClinicalTrials.gov** - Clinical trial information from the U.S. National Library of Medicine

## Installation

```bash
pip install openbb-nih
```

## Usage

```python
from openbb import obb

# Search for clinical trials by sponsor/company
trials = obb.equity.calendar.clinical_trials(
    sponsor="Pfizer",
    phase="phase3",
    provider="nih"
)

# Search by condition
trials = obb.equity.calendar.clinical_trials(
    condition="breast cancer",
    status="recruiting",
    provider="nih"
)
```

## API Reference

- [ClinicalTrials.gov API](https://clinicaltrials.gov/data-api/api)
