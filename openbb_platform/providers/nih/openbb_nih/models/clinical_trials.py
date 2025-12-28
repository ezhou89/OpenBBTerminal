"""NIH ClinicalTrials.gov Model."""

# pylint: disable=unused-argument

from datetime import date as dateType, datetime
from typing import Any, Dict, List, Literal, Optional

from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.clinical_trials import (
    ClinicalTrialsData,
    ClinicalTrialsQueryParams,
)
from openbb_core.provider.utils.errors import EmptyDataError
from pydantic import Field, field_validator


class NIHClinicalTrialsQueryParams(ClinicalTrialsQueryParams):
    """NIH ClinicalTrials.gov Query.

    Source: https://clinicaltrials.gov/data-api/api
    """

    study_type: Optional[Literal["interventional", "observational", "expanded_access"]] = Field(
        default=None,
        description="Type of study to filter by.",
    )


class NIHClinicalTrialsData(ClinicalTrialsData):
    """NIH ClinicalTrials.gov Data."""

    acronym: Optional[str] = Field(
        default=None,
        description="Acronym for the clinical trial.",
    )
    collaborators: Optional[str] = Field(
        default=None,
        description="Collaborating organizations, comma-separated.",
    )
    locations: Optional[str] = Field(
        default=None,
        description="Geographic locations of the trial sites.",
    )
    last_update_date: Optional[dateType] = Field(
        default=None,
        description="Date when the trial record was last updated.",
    )
    first_posted_date: Optional[dateType] = Field(
        default=None,
        description="Date when the trial was first posted on ClinicalTrials.gov.",
    )
    results_first_posted_date: Optional[dateType] = Field(
        default=None,
        description="Date when results were first posted.",
    )

    @field_validator(
        "start_date",
        "primary_completion_date",
        "completion_date",
        "last_update_date",
        "first_posted_date",
        "results_first_posted_date",
        mode="before",
        check_fields=False,
    )
    @classmethod
    def validate_dates(cls, v):
        """Parse date strings from API response."""
        if v is None:
            return None
        if isinstance(v, dateType):
            return v
        if isinstance(v, dict):
            # API returns dates as {"date": "2024-01-15", "type": "ESTIMATED"}
            v = v.get("date")
        if isinstance(v, str):
            try:
                return datetime.strptime(v[:10], "%Y-%m-%d").date()
            except (ValueError, TypeError):
                return None
        return None


class NIHClinicalTrialsFetcher(
    Fetcher[
        NIHClinicalTrialsQueryParams,
        List[NIHClinicalTrialsData],
    ]
):
    """Transform the query, extract and transform the data from ClinicalTrials.gov API v2."""

    require_credentials = False

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> NIHClinicalTrialsQueryParams:
        """Transform the query params."""
        return NIHClinicalTrialsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: NIHClinicalTrialsQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Extract data from ClinicalTrials.gov API v2."""
        # pylint: disable=import-outside-toplevel
        from openbb_core.provider.utils.helpers import amake_request

        base_url = "https://clinicaltrials.gov/api/v2/studies"

        # Build query parameters
        params: Dict[str, Any] = {
            "format": "json",
            "pageSize": min(query.limit or 100, 1000),
        }

        # Build the query expression
        query_terms = []

        if query.sponsor or query.symbol:
            sponsor = query.sponsor or query.symbol
            query_terms.append(f"AREA[LeadSponsorName]{sponsor}")

        if query.condition:
            query_terms.append(f"AREA[Condition]{query.condition}")

        if query.intervention:
            query_terms.append(f"AREA[InterventionName]{query.intervention}")

        if query_terms:
            params["query.term"] = " AND ".join(query_terms)

        # Filter by phase
        phase_map = {
            "early_phase1": "EARLY_PHASE1",
            "phase1": "PHASE1",
            "phase2": "PHASE2",
            "phase3": "PHASE3",
            "phase4": "PHASE4",
            "not_applicable": "NA",
        }
        if query.phase:
            params["filter.advanced"] = f"AREA[Phase]{phase_map.get(query.phase, query.phase)}"

        # Filter by status
        status_map = {
            "not_yet_recruiting": "NOT_YET_RECRUITING",
            "recruiting": "RECRUITING",
            "enrolling_by_invitation": "ENROLLING_BY_INVITATION",
            "active_not_recruiting": "ACTIVE_NOT_RECRUITING",
            "completed": "COMPLETED",
            "suspended": "SUSPENDED",
            "terminated": "TERMINATED",
            "withdrawn": "WITHDRAWN",
        }
        if query.status:
            status_filter = f"AREA[OverallStatus]{status_map.get(query.status, query.status)}"
            if "filter.advanced" in params:
                params["filter.advanced"] += f" AND {status_filter}"
            else:
                params["filter.advanced"] = status_filter

        # Filter by study type
        if query.study_type:
            study_type_filter = f"AREA[StudyType]{query.study_type.upper()}"
            if "filter.advanced" in params:
                params["filter.advanced"] += f" AND {study_type_filter}"
            else:
                params["filter.advanced"] = study_type_filter

        # Build URL with params
        url = base_url + "?" + "&".join(f"{k}={v}" for k, v in params.items())

        # Make the request
        response = await amake_request(url, timeout=30)

        if not response or "studies" not in response:
            return []

        return response.get("studies", [])

    @staticmethod
    def transform_data(
        query: NIHClinicalTrialsQueryParams,
        data: List[Dict],
        **kwargs: Any,
    ) -> List[NIHClinicalTrialsData]:
        """Transform the data to standard format."""
        if not data:
            raise EmptyDataError("No clinical trials found for the given query.")

        results = []
        for study in data:
            protocol = study.get("protocolSection", {})
            identification = protocol.get("identificationModule", {})
            status_module = protocol.get("statusModule", {})
            sponsor_module = protocol.get("sponsorCollaboratorsModule", {})
            design_module = protocol.get("designModule", {})
            conditions_module = protocol.get("conditionsModule", {})
            arms_module = protocol.get("armsInterventionsModule", {})
            outcomes_module = protocol.get("outcomesModule", {})

            # Get lead sponsor
            lead_sponsor = sponsor_module.get("leadSponsor", {})
            sponsor_name = lead_sponsor.get("name")

            # Get collaborators
            collaborators = sponsor_module.get("collaborators", [])
            collaborator_names = ", ".join(c.get("name", "") for c in collaborators) if collaborators else None

            # Get conditions
            conditions = conditions_module.get("conditions", [])
            conditions_str = ", ".join(conditions) if conditions else None

            # Get interventions
            interventions = arms_module.get("interventions", [])
            intervention_names = ", ".join(i.get("name", "") for i in interventions) if interventions else None

            # Get phases
            phases = design_module.get("phases", [])
            phase_str = ", ".join(phases) if phases else None

            # Get primary outcome
            primary_outcomes = outcomes_module.get("primaryOutcomes", [])
            primary_outcome = primary_outcomes[0].get("measure") if primary_outcomes else None

            # Get enrollment
            enrollment_info = design_module.get("enrollmentInfo", {})
            enrollment = enrollment_info.get("count")

            # Build the trial record
            trial = {
                "nct_id": identification.get("nctId"),
                "title": identification.get("officialTitle") or identification.get("briefTitle"),
                "brief_title": identification.get("briefTitle"),
                "acronym": identification.get("acronym"),
                "sponsor": sponsor_name,
                "collaborators": collaborator_names,
                "status": status_module.get("overallStatus"),
                "phase": phase_str,
                "conditions": conditions_str,
                "interventions": intervention_names,
                "start_date": status_module.get("startDateStruct"),
                "primary_completion_date": status_module.get("primaryCompletionDateStruct"),
                "completion_date": status_module.get("completionDateStruct"),
                "enrollment": enrollment,
                "study_type": design_module.get("studyType"),
                "primary_outcome": primary_outcome,
                "last_update_date": status_module.get("lastUpdateSubmitDateStruct"),
                "first_posted_date": status_module.get("studyFirstPostDateStruct"),
                "results_first_posted_date": status_module.get("resultsFirstPostDateStruct"),
                "url": f"https://clinicaltrials.gov/study/{identification.get('nctId')}",
            }

            # Filter by date range if specified (filter by primary completion date)
            primary_date = trial.get("primary_completion_date")
            if primary_date and isinstance(primary_date, dict):
                primary_date = primary_date.get("date")
            if primary_date and isinstance(primary_date, str):
                try:
                    primary_date = datetime.strptime(primary_date[:10], "%Y-%m-%d").date()
                except (ValueError, TypeError):
                    primary_date = None

            if query.start_date and primary_date and primary_date < query.start_date:
                continue
            if query.end_date and primary_date and primary_date > query.end_date:
                continue

            results.append(NIHClinicalTrialsData.model_validate(trial))

        if not results:
            raise EmptyDataError("No clinical trials found matching the date criteria.")

        # Sort by primary completion date (most imminent first)
        results.sort(
            key=lambda x: x.primary_completion_date or dateType.max,
        )

        return results
