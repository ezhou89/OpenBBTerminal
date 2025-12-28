"""Tests for IV Analytics Utilities."""

import math
from unittest.mock import MagicMock

import pytest

from openbb_core.provider.utils.iv_analytics import (
    calculate_expected_move,
    calculate_expected_move_from_straddle,
    calculate_iv_percentile,
    calculate_iv_rank,
    get_atm_iv,
    iv_term_structure,
)


class TestCalculateIVRank:
    """Tests for calculate_iv_rank function."""

    def test_iv_rank_middle_of_range(self):
        """IV at middle of range should return 50."""
        result = calculate_iv_rank(0.35, 0.20, 0.50)
        assert result == 50.0

    def test_iv_rank_at_low(self):
        """IV at low should return 0."""
        result = calculate_iv_rank(0.20, 0.20, 0.50)
        assert result == 0.0

    def test_iv_rank_at_high(self):
        """IV at high should return 100."""
        result = calculate_iv_rank(0.50, 0.20, 0.50)
        assert result == 100.0

    def test_iv_rank_quarter_range(self):
        """IV at 25% of range."""
        result = calculate_iv_rank(0.275, 0.20, 0.50)
        assert result == 25.0

    def test_iv_rank_three_quarter_range(self):
        """IV at 75% of range."""
        result = calculate_iv_rank(0.425, 0.20, 0.50)
        assert result == 75.0

    def test_iv_rank_no_range(self):
        """Equal high and low should return 50."""
        result = calculate_iv_rank(0.30, 0.30, 0.30)
        assert result == 50.0

    def test_iv_rank_below_low(self):
        """IV below historical low should return 0."""
        result = calculate_iv_rank(0.10, 0.20, 0.50)
        assert result == 0.0

    def test_iv_rank_above_high(self):
        """IV above historical high should return 100."""
        result = calculate_iv_rank(0.60, 0.20, 0.50)
        assert result == 100.0


class TestCalculateIVPercentile:
    """Tests for calculate_iv_percentile function."""

    def test_iv_percentile_middle(self):
        """IV in middle of historical distribution."""
        historical = [0.20, 0.25, 0.30, 0.35, 0.40]
        result = calculate_iv_percentile(0.32, historical)
        assert result == 60.0  # 3 out of 5 are lower

    def test_iv_percentile_at_lowest(self):
        """IV at lowest historical value."""
        historical = [0.20, 0.25, 0.30, 0.35, 0.40]
        result = calculate_iv_percentile(0.20, historical)
        assert result == 0.0  # None are lower

    def test_iv_percentile_below_all(self):
        """IV below all historical values."""
        historical = [0.20, 0.25, 0.30, 0.35, 0.40]
        result = calculate_iv_percentile(0.15, historical)
        assert result == 0.0

    def test_iv_percentile_above_all(self):
        """IV above all historical values."""
        historical = [0.20, 0.25, 0.30, 0.35, 0.40]
        result = calculate_iv_percentile(0.50, historical)
        assert result == 100.0

    def test_iv_percentile_empty_history(self):
        """Empty historical data returns 50."""
        result = calculate_iv_percentile(0.30, [])
        assert result == 50.0

    def test_iv_percentile_single_value(self):
        """Single historical value."""
        result = calculate_iv_percentile(0.30, [0.25])
        assert result == 100.0  # 1 out of 1 is lower

    def test_iv_percentile_all_same(self):
        """All historical values same as current."""
        historical = [0.30, 0.30, 0.30, 0.30]
        result = calculate_iv_percentile(0.30, historical)
        assert result == 0.0  # None are strictly lower


class TestCalculateExpectedMove:
    """Tests for calculate_expected_move function."""

    def test_expected_move_basic(self):
        """Basic expected move calculation."""
        move, pct, (low, high) = calculate_expected_move(100.0, 0.30, 30)
        # sqrt(30/365) ≈ 0.2867
        # Expected move = 100 * 0.30 * 0.2867 ≈ 8.60
        assert move == pytest.approx(8.60, abs=0.1)
        assert pct == pytest.approx(8.60, abs=0.1)
        assert low == pytest.approx(91.40, abs=0.1)
        assert high == pytest.approx(108.60, abs=0.1)

    def test_expected_move_zero_dte(self):
        """Zero DTE should have zero expected move."""
        move, pct, (low, high) = calculate_expected_move(100.0, 0.30, 0)
        assert move == 0.0
        assert pct == 0.0
        assert low == 100.0
        assert high == 100.0

    def test_expected_move_one_year(self):
        """One year DTE should match IV."""
        move, pct, (low, high) = calculate_expected_move(100.0, 0.30, 365)
        assert move == pytest.approx(30.0, abs=0.1)
        assert pct == pytest.approx(30.0, abs=0.1)

    def test_expected_move_high_iv(self):
        """High IV stock."""
        move, pct, (low, high) = calculate_expected_move(50.0, 1.0, 30)
        # sqrt(30/365) ≈ 0.2867
        # Expected move = 50 * 1.0 * 0.2867 ≈ 14.33
        assert move == pytest.approx(14.33, abs=0.1)
        assert pct == pytest.approx(28.67, abs=0.2)

    def test_expected_move_low_iv(self):
        """Low IV stock."""
        move, pct, (low, high) = calculate_expected_move(200.0, 0.10, 7)
        # sqrt(7/365) ≈ 0.1385
        # Expected move = 200 * 0.10 * 0.1385 ≈ 2.77
        assert move == pytest.approx(2.77, abs=0.1)

    def test_expected_move_custom_annualization(self):
        """Custom annualization factor (trading days)."""
        move, pct, _ = calculate_expected_move(100.0, 0.30, 21, annualization_factor=252)
        # sqrt(21/252) ≈ 0.2887
        # Expected move = 100 * 0.30 * 0.2887 ≈ 8.66
        assert move == pytest.approx(8.66, abs=0.1)


class TestCalculateExpectedMoveFromStraddle:
    """Tests for calculate_expected_move_from_straddle function."""

    def test_straddle_expected_move_basic(self):
        """Basic straddle-implied expected move."""
        move, pct, (low, high) = calculate_expected_move_from_straddle(8.50, 100.0)
        assert move == 8.50
        assert pct == 8.50
        assert low == 91.50
        assert high == 108.50

    def test_straddle_expected_move_high_premium(self):
        """High straddle premium."""
        move, pct, (low, high) = calculate_expected_move_from_straddle(25.0, 100.0)
        assert move == 25.0
        assert pct == 25.0
        assert low == 75.0
        assert high == 125.0

    def test_straddle_expected_move_low_premium(self):
        """Low straddle premium."""
        move, pct, (low, high) = calculate_expected_move_from_straddle(2.0, 50.0)
        assert move == 2.0
        assert pct == 4.0
        assert low == 48.0
        assert high == 52.0


class TestGetAtmIV:
    """Tests for get_atm_iv function."""

    @pytest.fixture
    def sample_options_df(self):
        """Create a sample options DataFrame."""
        import pandas as pd

        return pd.DataFrame({
            "strike": [95, 95, 100, 100, 105, 105],
            "option_type": ["call", "put", "call", "put", "call", "put"],
            "implied_volatility": [0.32, 0.33, 0.30, 0.31, 0.28, 0.29],
            "expiration": ["2024-01-19"] * 6,
        })

    def test_get_atm_iv_basic(self, sample_options_df):
        """Get ATM IV for underlying at 100."""
        result = get_atm_iv(sample_options_df, 100.0)
        # Average of call (0.30) and put (0.31) at strike 100
        assert result == pytest.approx(0.305, abs=0.001)

    def test_get_atm_iv_between_strikes(self, sample_options_df):
        """Get ATM IV when underlying is between strikes."""
        result = get_atm_iv(sample_options_df, 102.0)
        # Closest strike is 100
        assert result == pytest.approx(0.305, abs=0.001)

    def test_get_atm_iv_with_expiration(self, sample_options_df):
        """Get ATM IV for specific expiration."""
        result = get_atm_iv(sample_options_df, 100.0, expiration="2024-01-19")
        assert result == pytest.approx(0.305, abs=0.001)

    def test_get_atm_iv_wrong_expiration(self, sample_options_df):
        """Get ATM IV with non-existent expiration returns None."""
        result = get_atm_iv(sample_options_df, 100.0, expiration="2024-02-16")
        assert result is None

    def test_get_atm_iv_empty_df(self):
        """Empty DataFrame returns None."""
        import pandas as pd

        result = get_atm_iv(pd.DataFrame(), 100.0)
        assert result is None

    def test_get_atm_iv_no_iv_column(self):
        """DataFrame without IV column returns None."""
        import pandas as pd

        df = pd.DataFrame({"strike": [100], "option_type": ["call"]})
        result = get_atm_iv(df, 100.0)
        assert result is None

    def test_get_atm_iv_call_only(self):
        """Get ATM IV with only calls available."""
        import pandas as pd

        df = pd.DataFrame({
            "strike": [100],
            "option_type": ["call"],
            "implied_volatility": [0.30],
        })
        result = get_atm_iv(df, 100.0)
        assert result == 0.30


class TestIVTermStructure:
    """Tests for iv_term_structure function."""

    @pytest.fixture
    def multi_expiry_df(self):
        """Create options DataFrame with multiple expirations."""
        import pandas as pd

        return pd.DataFrame({
            "strike": [100, 100, 100, 100, 100, 100],
            "option_type": ["call", "put", "call", "put", "call", "put"],
            "implied_volatility": [0.25, 0.26, 0.30, 0.31, 0.35, 0.36],
            "expiration": [
                "2024-01-19", "2024-01-19",
                "2024-02-16", "2024-02-16",
                "2024-03-15", "2024-03-15",
            ],
        })

    def test_term_structure_basic(self, multi_expiry_df):
        """Get IV term structure."""
        result = iv_term_structure(multi_expiry_df, 100.0)
        assert len(result) == 3
        assert list(result["expiration"]) == ["2024-01-19", "2024-02-16", "2024-03-15"]
        assert result["atm_iv"].iloc[0] == pytest.approx(0.255, abs=0.001)
        assert result["atm_iv"].iloc[1] == pytest.approx(0.305, abs=0.001)
        assert result["atm_iv"].iloc[2] == pytest.approx(0.355, abs=0.001)

    def test_term_structure_empty_df(self):
        """Empty DataFrame returns empty result."""
        import pandas as pd

        result = iv_term_structure(pd.DataFrame(), 100.0)
        assert result.empty

    def test_term_structure_no_expiration(self):
        """DataFrame without expiration column returns empty."""
        import pandas as pd

        df = pd.DataFrame({
            "strike": [100],
            "option_type": ["call"],
            "implied_volatility": [0.30],
        })
        result = iv_term_structure(df, 100.0)
        assert result.empty

    def test_term_structure_sorted(self, multi_expiry_df):
        """Term structure should be sorted by expiration."""
        import pandas as pd

        # Shuffle the data
        shuffled = multi_expiry_df.sample(frac=1).reset_index(drop=True)
        result = iv_term_structure(shuffled, 100.0)
        # Should still be sorted
        expirations = list(result["expiration"])
        assert expirations == sorted(expirations)
