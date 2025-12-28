"""Tests for NIH Provider Fetchers."""

import pytest
from openbb_core.app.service.user_service import UserService
from openbb_nih.models.clinical_trials import (
    NIHClinicalTrialsFetcher,
    NIHClinicalTrialsQueryParams,
)

test_credentials = UserService().default_user_settings.credentials.model_dump(
    mode="json"
)


@pytest.fixture(scope="module")
def vcr_config():
    """VCR configuration for recording API responses."""
    return {
        "filter_headers": [("User-Agent", None)],
        "filter_query_parameters": [],
    }


@pytest.mark.record_http
def test_nih_clinical_trials_fetcher(credentials=test_credentials):
    """Test NIH Clinical Trials Fetcher with sponsor search."""
    params = NIHClinicalTrialsQueryParams(
        sponsor="Pfizer",
        phase="phase3",
        status="recruiting",
        limit=10,
    )

    fetcher = NIHClinicalTrialsFetcher()
    result = fetcher.test(params, credentials)

    assert result is not None
    assert len(result) > 0
    # Verify expected fields are present
    first_result = result[0]
    assert first_result.nct_id is not None
    assert first_result.title is not None


@pytest.mark.record_http
def test_nih_clinical_trials_by_condition(credentials=test_credentials):
    """Test NIH Clinical Trials Fetcher with condition search."""
    params = NIHClinicalTrialsQueryParams(
        condition="breast cancer",
        phase="phase3",
        limit=5,
    )

    fetcher = NIHClinicalTrialsFetcher()
    result = fetcher.test(params, credentials)

    assert result is not None
    assert len(result) > 0


@pytest.mark.record_http
def test_nih_clinical_trials_by_intervention(credentials=test_credentials):
    """Test NIH Clinical Trials Fetcher with intervention search."""
    params = NIHClinicalTrialsQueryParams(
        intervention="pembrolizumab",
        limit=5,
    )

    fetcher = NIHClinicalTrialsFetcher()
    result = fetcher.test(params, credentials)

    assert result is not None
