"""Tests for Unified Options Research Utilities."""

from datetime import date, timedelta

import pytest

from openbb_core.provider.utils.options_research import (
    build_research_summary,
    format_research_report,
)


class TestBuildResearchSummary:
    """Tests for build_research_summary function."""

    @pytest.fixture
    def sample_expirations(self):
        """Generate sample expiration dates."""
        today = date.today()
        return [
            (today + timedelta(days=7)).strftime("%Y-%m-%d"),
            (today + timedelta(days=14)).strftime("%Y-%m-%d"),
            (today + timedelta(days=21)).strftime("%Y-%m-%d"),
            (today + timedelta(days=35)).strftime("%Y-%m-%d"),
            (today + timedelta(days=49)).strftime("%Y-%m-%d"),
        ]

    def test_basic_summary(self, sample_expirations):
        """Build basic summary without catalysts."""
        result = build_research_summary(
            symbol="AAPL",
            underlying_price=175.50,
            options_expirations=sample_expirations,
        )

        assert result["symbol"] == "AAPL"
        assert result["underlying_price"] == 175.50
        assert "overview" in result
        assert "catalysts" in result
        assert "strategy_ideas" in result

    def test_with_iv_metrics(self, sample_expirations):
        """Summary with IV metrics included."""
        result = build_research_summary(
            symbol="AAPL",
            underlying_price=175.50,
            options_expirations=sample_expirations,
            atm_iv=0.28,
            iv_rank=65.0,
            iv_percentile=70.0,
        )

        assert result["overview"]["atm_iv"] == 0.28
        assert result["overview"]["iv_rank"] == 65.0
        assert result["overview"]["iv_percentile"] == 70.0
        assert result["overview"]["iv_environment"] == "elevated"

    def test_with_earnings_date(self, sample_expirations):
        """Summary with earnings date."""
        earnings = date.today() + timedelta(days=10)
        result = build_research_summary(
            symbol="AAPL",
            underlying_price=175.50,
            options_expirations=sample_expirations,
            earnings_date=earnings,
        )

        assert len(result["catalysts"]) >= 1
        earnings_catalyst = result["catalysts"][0]
        assert earnings_catalyst["type"] == "earnings"
        assert earnings_catalyst["days_until"] == 10

    def test_with_clinical_trials(self, sample_expirations):
        """Summary with clinical trials data."""
        trials = [
            {
                "nct_id": "NCT12345678",
                "brief_title": "Phase 3 Study of Drug X",
                "phase": "PHASE3",
                "primary_completion_date": (date.today() + timedelta(days=30)).strftime("%Y-%m-%d"),
            }
        ]
        result = build_research_summary(
            symbol="MRNA",
            underlying_price=120.00,
            options_expirations=sample_expirations,
            clinical_trials=trials,
        )

        assert len(result["catalysts"]) >= 1
        trial_catalyst = [c for c in result["catalysts"] if c["type"] == "clinical_trial"]
        assert len(trial_catalyst) > 0

    def test_expected_moves_calculated(self, sample_expirations):
        """Expected moves calculated when IV provided."""
        result = build_research_summary(
            symbol="AAPL",
            underlying_price=175.50,
            options_expirations=sample_expirations,
            atm_iv=0.30,
        )

        assert "expected_move_7d" in result["overview"]
        assert "expected_move_30d" in result["overview"]
        assert result["overview"]["expected_move_30d"]["dollars"] > 0

    def test_high_iv_strategy_ideas(self, sample_expirations):
        """High IV generates sell premium strategies."""
        result = build_research_summary(
            symbol="AAPL",
            underlying_price=175.50,
            options_expirations=sample_expirations,
            iv_rank=85.0,
        )

        strategies = [idea["strategy"] for idea in result["strategy_ideas"]]
        assert "iron_condor" in strategies or "short_strangle" in strategies

    def test_low_iv_strategy_ideas(self, sample_expirations):
        """Low IV generates buy premium strategies."""
        result = build_research_summary(
            symbol="AAPL",
            underlying_price=175.50,
            options_expirations=sample_expirations,
            iv_rank=15.0,
        )

        strategies = [idea["strategy"] for idea in result["strategy_ideas"]]
        assert "long_straddle" in strategies or "calendar_spread" in strategies

    def test_iv_environment_classification(self, sample_expirations):
        """IV environment correctly classified."""
        # Very high IV
        result = build_research_summary(
            symbol="AAPL",
            underlying_price=175.50,
            options_expirations=sample_expirations,
            iv_rank=90.0,
        )
        assert result["overview"]["iv_environment"] == "very_high"

        # Very low IV
        result = build_research_summary(
            symbol="AAPL",
            underlying_price=175.50,
            options_expirations=sample_expirations,
            iv_rank=10.0,
        )
        assert result["overview"]["iv_environment"] == "very_low"

    def test_catalysts_sorted_by_date(self, sample_expirations):
        """Catalysts sorted by days until event."""
        earnings = date.today() + timedelta(days=20)
        trials = [
            {
                "brief_title": "Trial 1",
                "primary_completion_date": (date.today() + timedelta(days=10)).strftime("%Y-%m-%d"),
            }
        ]
        result = build_research_summary(
            symbol="MRNA",
            underlying_price=120.00,
            options_expirations=sample_expirations,
            earnings_date=earnings,
            clinical_trials=trials,
        )

        if len(result["catalysts"]) >= 2:
            days = [c["days_until"] for c in result["catalysts"]]
            assert days == sorted(days)


class TestFormatResearchReport:
    """Tests for format_research_report function."""

    def test_basic_format(self):
        """Format basic summary."""
        summary = {
            "symbol": "AAPL",
            "underlying_price": 175.50,
            "overview": {
                "atm_iv": 0.28,
                "iv_rank": 65.0,
                "iv_environment": "elevated",
            },
            "catalysts": [],
            "strategy_ideas": [],
        }

        report = format_research_report(summary)
        assert "AAPL" in report
        assert "$175.50" in report
        assert "28.0%" in report
        assert "65%" in report

    def test_format_with_catalysts(self):
        """Format report with catalysts."""
        summary = {
            "symbol": "AAPL",
            "underlying_price": 175.50,
            "overview": {"iv_environment": "neutral"},
            "catalysts": [
                {
                    "type": "earnings",
                    "date": "2024-02-01",
                    "days_until": 10,
                    "nearest_post_expiration": "2024-02-02",
                }
            ],
            "strategy_ideas": [],
        }

        report = format_research_report(summary)
        assert "CATALYSTS" in report
        assert "Earnings" in report
        assert "10 days" in report

    def test_format_with_strategies(self):
        """Format report with strategy ideas."""
        summary = {
            "symbol": "AAPL",
            "underlying_price": 175.50,
            "overview": {"iv_environment": "elevated"},
            "catalysts": [],
            "strategy_ideas": [
                {
                    "strategy": "iron_condor",
                    "rationale": "High IV environment",
                }
            ],
        }

        report = format_research_report(summary)
        assert "STRATEGY IDEAS" in report
        assert "Iron Condor" in report

    def test_format_with_expected_moves(self):
        """Format report with expected moves."""
        summary = {
            "symbol": "AAPL",
            "underlying_price": 175.50,
            "overview": {
                "iv_environment": "neutral",
                "expected_move_7d": {
                    "dollars": 5.25,
                    "percent": 3.0,
                    "range": (170.25, 180.75),
                },
            },
            "catalysts": [],
            "strategy_ideas": [],
        }

        report = format_research_report(summary)
        assert "7-day" in report
        assert "$5.25" in report

    def test_report_is_string(self):
        """Report is a string."""
        summary = {
            "symbol": "AAPL",
            "underlying_price": 175.50,
            "overview": {},
            "catalysts": [],
            "strategy_ideas": [],
        }

        report = format_research_report(summary)
        assert isinstance(report, str)
        assert len(report) > 0
