"""NIH Provider module."""

from openbb_core.provider.abstract.provider import Provider
from openbb_nih.models.clinical_trials import NIHClinicalTrialsFetcher

nih_provider = Provider(
    name="nih",
    website="https://www.nih.gov",
    description="""The National Institutes of Health (NIH) is the primary agency of the
United States government responsible for biomedical and public health research.
This provider includes data from ClinicalTrials.gov, which is maintained by the
National Library of Medicine (NLM) at the NIH.""",
    fetcher_dict={
        "ClinicalTrials": NIHClinicalTrialsFetcher,
    },
    repr_name="NIH | National Institutes of Health",
)
