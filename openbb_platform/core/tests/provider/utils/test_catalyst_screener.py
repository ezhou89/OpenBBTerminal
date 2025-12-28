"""Tests for Catalyst Screener Utilities."""

from datetime import date

import pytest

from openbb_core.provider.utils.catalyst_screener import (
    calculate_earnings_iv_premium,
    combine_catalysts_with_options,
    filter_by_catalyst_proximity,
    find_nearest_post_catalyst_expiration,
    score_catalyst_play,
    screen_options_before_earnings,
)


class TestFilterByCatalystProximity:
    """Tests for filter_by_catalyst_proximity function."""

    def test_finds_expiration_after_catalyst(self):
        """Find expiration right after catalyst."""
        expirations = ["2024-01-19", "2024-01-26", "2024-02-02"]
        catalyst = date(2024, 1, 25)
        result = filter_by_catalyst_proximity(expirations, catalyst)
        assert "2024-01-26" in result
        assert "2024-02-02" not in result  # Too far after

    def test_includes_expiration_before_catalyst(self):
        """Include expirations slightly before catalyst."""
        expirations = ["2024-01-19", "2024-01-26", "2024-02-02"]
        catalyst = date(2024, 1, 25)
        result = filter_by_catalyst_proximity(expirations, catalyst, days_before=7)
        assert "2024-01-19" in result
        assert "2024-01-26" in result

    def test_custom_window(self):
        """Custom window parameters."""
        expirations = ["2024-01-19", "2024-01-26", "2024-02-02", "2024-02-09"]
        catalyst = date(2024, 1, 25)
        result = filter_by_catalyst_proximity(
            expirations, catalyst, days_before=10, days_after=14
        )
        assert len(result) == 3
        assert "2024-02-09" not in result  # 15 days after

    def test_empty_list(self):
        """Empty expirations list."""
        result = filter_by_catalyst_proximity([], date(2024, 1, 25))
        assert result == []

    def test_no_matching_expirations(self):
        """No expirations match window."""
        expirations = ["2024-03-15", "2024-06-21"]
        catalyst = date(2024, 1, 25)
        result = filter_by_catalyst_proximity(expirations, catalyst)
        assert result == []


class TestFindNearestPostCatalystExpiration:
    """Tests for find_nearest_post_catalyst_expiration function."""

    def test_finds_nearest_after(self):
        """Find the nearest expiration after catalyst."""
        expirations = ["2024-01-19", "2024-01-26", "2024-02-02"]
        catalyst = date(2024, 1, 25)
        result = find_nearest_post_catalyst_expiration(expirations, catalyst)
        assert result == "2024-01-26"

    def test_respects_min_days(self):
        """Respects minimum days after catalyst."""
        expirations = ["2024-01-26", "2024-02-02"]
        catalyst = date(2024, 1, 25)
        # Jan 26 is only 1 day after, min is 2
        result = find_nearest_post_catalyst_expiration(
            expirations, catalyst, min_days_after=2
        )
        assert result == "2024-02-02"

    def test_respects_max_days(self):
        """Respects maximum days after catalyst."""
        expirations = ["2024-02-02", "2024-02-09"]
        catalyst = date(2024, 1, 25)
        # Feb 2 is 8 days after, max is 5
        result = find_nearest_post_catalyst_expiration(
            expirations, catalyst, max_days_after=5
        )
        assert result is None

    def test_none_if_no_match(self):
        """Returns None if no matching expiration."""
        expirations = ["2024-01-19", "2024-01-20"]
        catalyst = date(2024, 1, 25)
        result = find_nearest_post_catalyst_expiration(expirations, catalyst)
        assert result is None

    def test_empty_list(self):
        """Empty expirations returns None."""
        result = find_nearest_post_catalyst_expiration([], date(2024, 1, 25))
        assert result is None


class TestScreenOptionsBeforeEarnings:
    """Tests for screen_options_before_earnings function."""

    @pytest.fixture
    def sample_options_df(self):
        """Create sample options DataFrame."""
        import pandas as pd

        return pd.DataFrame({
            "strike": [95, 100, 105, 95, 100, 105],
            "option_type": ["call", "call", "call", "put", "put", "put"],
            "implied_volatility": [0.35, 0.32, 0.30, 0.36, 0.33, 0.31],
            "expiration": ["2024-01-26"] * 6,
        })

    @pytest.fixture
    def multi_exp_options_df(self):
        """Create options DataFrame with multiple expirations."""
        import pandas as pd

        return pd.DataFrame({
            "strike": [100, 100, 100, 100],
            "option_type": ["call", "call", "put", "put"],
            "implied_volatility": [0.35, 0.25, 0.36, 0.26],
            "expiration": ["2024-01-26", "2024-02-02", "2024-01-26", "2024-02-02"],
        })

    def test_filters_post_earnings(self, multi_exp_options_df):
        """Filters to first expiration after earnings."""
        earnings = date(2024, 1, 25)
        result = screen_options_before_earnings(
            multi_exp_options_df, earnings, underlying_price=100.0
        )
        assert len(result) == 2
        assert all(result["expiration"] == "2024-01-26")

    def test_filters_by_strike_distance(self, sample_options_df):
        """Filters by strike distance from ATM."""
        earnings = date(2024, 1, 25)
        result = screen_options_before_earnings(
            sample_options_df, earnings, underlying_price=100.0, max_strike_distance_pct=3.0
        )
        # Only 100 strike within 3%
        assert all(result["strike"] == 100)

    def test_filters_by_min_iv(self, sample_options_df):
        """Filters by minimum IV."""
        earnings = date(2024, 1, 25)
        result = screen_options_before_earnings(
            sample_options_df, earnings, underlying_price=100.0, min_iv=0.33
        )
        assert len(result) > 0
        assert all(result["implied_volatility"] >= 0.33)

    def test_filters_by_option_type(self, sample_options_df):
        """Filters by option type."""
        earnings = date(2024, 1, 25)
        result = screen_options_before_earnings(
            sample_options_df, earnings, underlying_price=100.0, option_type="call"
        )
        assert all(result["option_type"] == "call")

    def test_empty_df(self):
        """Empty DataFrame returns empty."""
        import pandas as pd

        result = screen_options_before_earnings(
            pd.DataFrame(), date(2024, 1, 25), underlying_price=100.0
        )
        assert result.empty


class TestCalculateEarningsIVPremium:
    """Tests for calculate_earnings_iv_premium function."""

    def test_basic_crush(self):
        """Basic IV crush calculation."""
        result = calculate_earnings_iv_premium(0.50, 0.30)
        assert result["iv_crush"] == 0.20
        assert result["iv_crush_pct"] == 40.0

    def test_no_crush(self):
        """No IV crush (IV unchanged)."""
        result = calculate_earnings_iv_premium(0.30, 0.30)
        assert result["iv_crush"] == 0.0
        assert result["iv_crush_pct"] == 0.0

    def test_negative_crush(self):
        """Negative crush (IV increased after earnings)."""
        result = calculate_earnings_iv_premium(0.30, 0.40)
        assert result["iv_crush"] == -0.10
        assert result["iv_crush_pct"] == pytest.approx(-33.33, abs=0.1)

    def test_zero_pre_iv(self):
        """Zero pre-earnings IV."""
        result = calculate_earnings_iv_premium(0.0, 0.30)
        assert result["iv_crush_pct"] == 0.0


class TestScoreCatalystPlay:
    """Tests for score_catalyst_play function."""

    def test_high_score_setup(self):
        """High IV rank, good timing = high score."""
        result = score_catalyst_play(
            expected_move_pct=8.0,
            iv_rank=85.0,
            days_to_catalyst=5,
            days_to_expiration=7,  # 2 days after catalyst
        )
        assert result["composite_score"] >= 80
        assert "sell premium" in result["recommendation"].lower()

    def test_low_score_setup(self):
        """Low IV rank, poor timing = low score."""
        result = score_catalyst_play(
            expected_move_pct=2.0,
            iv_rank=15.0,
            days_to_catalyst=5,
            days_to_expiration=30,  # 25 days after
        )
        assert result["composite_score"] < 40

    def test_expiration_before_catalyst(self):
        """Expiration before catalyst penalized."""
        result = score_catalyst_play(
            expected_move_pct=8.0,
            iv_rank=80.0,
            days_to_catalyst=10,
            days_to_expiration=5,  # 5 days before catalyst
        )
        assert result["time_alignment_score"] < 50

    def test_component_scores(self):
        """All component scores returned."""
        result = score_catalyst_play(
            expected_move_pct=5.0,
            iv_rank=50.0,
            days_to_catalyst=7,
            days_to_expiration=10,
        )
        assert "composite_score" in result
        assert "iv_rank_score" in result
        assert "time_alignment_score" in result
        assert "expected_move_score" in result
        assert "recommendation" in result


class TestCombineCatalystsWithOptions:
    """Tests for combine_catalysts_with_options function."""

    def test_combines_correctly(self):
        """Combines catalysts with relevant expirations."""
        expirations = ["2024-01-26", "2024-02-02", "2024-02-09", "2024-02-16"]
        catalysts = [
            {"date": "2024-01-25", "name": "Q4 Earnings"},
            {"date": "2024-02-10", "name": "Product Launch"},
        ]
        result = combine_catalysts_with_options(expirations, catalysts)

        assert len(result) == 2
        assert result[0]["catalyst_name"] == "Q4 Earnings"
        assert "2024-01-26" in result[0]["relevant_expirations"]
        assert result[0]["nearest_post_catalyst_expiration"] == "2024-01-26"

    def test_custom_field_names(self):
        """Supports custom field names for catalysts."""
        expirations = ["2024-01-26", "2024-02-02"]
        catalysts = [
            {"event_date": "2024-01-25", "event_name": "Earnings"},
        ]
        result = combine_catalysts_with_options(
            expirations,
            catalysts,
            catalyst_date_field="event_date",
            catalyst_name_field="event_name",
        )
        assert len(result) == 1
        assert result[0]["catalyst_name"] == "Earnings"

    def test_empty_catalysts(self):
        """Empty catalysts list returns empty."""
        result = combine_catalysts_with_options(
            ["2024-01-26", "2024-02-02"], []
        )
        assert result == []

    def test_no_relevant_expirations(self):
        """Catalyst with no nearby expirations excluded."""
        expirations = ["2024-06-21", "2024-09-20"]
        catalysts = [{"date": "2024-01-25", "name": "Earnings"}]
        result = combine_catalysts_with_options(expirations, catalysts)
        assert len(result) == 0

    def test_sorts_by_days_to_catalyst(self):
        """Results sorted by days to catalyst."""
        expirations = ["2024-01-26", "2024-02-09", "2024-02-16"]
        catalysts = [
            {"date": "2024-02-10", "name": "Later Event"},
            {"date": "2024-01-25", "name": "Earlier Event"},
        ]
        result = combine_catalysts_with_options(expirations, catalysts)

        # Earlier event should come first
        assert result[0]["catalyst_name"] == "Earlier Event"
