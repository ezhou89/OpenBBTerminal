"""Clinical Trials Standard Model."""

from datetime import date as dateType
from typing import Literal, Optional

from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.descriptions import (
    QUERY_DESCRIPTIONS,
)
from pydantic import Field


class ClinicalTrialsQueryParams(QueryParams):
    """Clinical Trials Query.

    Search for clinical trials from ClinicalTrials.gov.
    Useful for biotech catalyst tracking around trial readouts.
    """

    symbol: Optional[str] = Field(
        default=None,
        description=QUERY_DESCRIPTIONS.get("symbol", "")
        + " Maps to sponsor/company search.",
    )
    condition: Optional[str] = Field(
        default=None,
        description="Condition or disease being studied (e.g., 'breast cancer', 'diabetes').",
    )
    intervention: Optional[str] = Field(
        default=None,
        description="Drug, device, or intervention being tested.",
    )
    sponsor: Optional[str] = Field(
        default=None,
        description="Lead sponsor or company running the trial.",
    )
    phase: Optional[
        Literal[
            "early_phase1",
            "phase1",
            "phase2",
            "phase3",
            "phase4",
            "not_applicable",
        ]
    ] = Field(
        default=None,
        description="Trial phase. Phase 3 trials are typically the most significant catalysts.",
    )
    status: Optional[
        Literal[
            "not_yet_recruiting",
            "recruiting",
            "enrolling_by_invitation",
            "active_not_recruiting",
            "completed",
            "suspended",
            "terminated",
            "withdrawn",
        ]
    ] = Field(
        default=None,
        description="Overall recruitment status of the trial.",
    )
    start_date: Optional[dateType] = Field(
        default=None,
        description=QUERY_DESCRIPTIONS.get("start_date", "")
        + " Filters by primary completion date range.",
    )
    end_date: Optional[dateType] = Field(
        default=None,
        description=QUERY_DESCRIPTIONS.get("end_date", "")
        + " Filters by primary completion date range.",
    )
    limit: Optional[int] = Field(
        default=100,
        description=QUERY_DESCRIPTIONS.get("limit", ""),
    )


class ClinicalTrialsData(Data):
    """Clinical Trials Data.

    Contains information about clinical trials from ClinicalTrials.gov.
    Key fields for catalyst trading: primary_completion_date, phase, status.
    """

    nct_id: str = Field(
        description="ClinicalTrials.gov NCT identifier (e.g., 'NCT04280705').",
    )
    title: str = Field(
        description="Official title of the clinical trial.",
    )
    brief_title: Optional[str] = Field(
        default=None,
        description="Brief title of the clinical trial.",
    )
    sponsor: Optional[str] = Field(
        default=None,
        description="Lead sponsor or company running the trial.",
    )
    status: Optional[str] = Field(
        default=None,
        description="Overall recruitment status (e.g., 'Recruiting', 'Completed').",
    )
    phase: Optional[str] = Field(
        default=None,
        description="Trial phase (e.g., 'Phase 3', 'Phase 2/Phase 3').",
    )
    conditions: Optional[str] = Field(
        default=None,
        description="Conditions or diseases being studied, comma-separated.",
    )
    interventions: Optional[str] = Field(
        default=None,
        description="Interventions or treatments being tested, comma-separated.",
    )
    start_date: Optional[dateType] = Field(
        default=None,
        description="Date when the trial started or is expected to start.",
    )
    primary_completion_date: Optional[dateType] = Field(
        default=None,
        description="Expected date for primary outcome data collection completion. "
        "Key date for catalyst trading.",
    )
    completion_date: Optional[dateType] = Field(
        default=None,
        description="Expected date for study completion (last participant's last visit).",
    )
    enrollment: Optional[int] = Field(
        default=None,
        description="Number of participants enrolled or expected.",
    )
    study_type: Optional[str] = Field(
        default=None,
        description="Type of study (e.g., 'Interventional', 'Observational').",
    )
    primary_outcome: Optional[str] = Field(
        default=None,
        description="Primary outcome measure of the trial.",
    )
    url: Optional[str] = Field(
        default=None,
        description="URL to the trial page on ClinicalTrials.gov.",
    )
