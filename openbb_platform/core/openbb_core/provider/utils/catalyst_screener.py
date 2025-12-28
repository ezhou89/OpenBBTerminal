"""Catalyst-Aware Options Screener Utilities.

This module provides utilities for screening options based on proximity
to catalyst events like earnings releases and clinical trials.
"""

from datetime import date as dateType, timedelta
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Tuple

if TYPE_CHECKING:
    from pandas import DataFrame


def filter_by_catalyst_proximity(
    options_expirations: List[str],
    catalyst_date: dateType,
    days_before: int = 7,
    days_after: int = 3,
) -> List[str]:
    """Filter option expirations by proximity to a catalyst date.

    Useful for finding options that expire right after earnings or other events.

    Parameters
    ----------
    options_expirations : List[str]
        List of expiration dates in YYYY-MM-DD format.
    catalyst_date : date
        The catalyst event date (e.g., earnings date).
    days_before : int
        Maximum days before catalyst that expiration can occur. Default 7.
    days_after : int
        Maximum days after catalyst that expiration can occur. Default 3.

    Returns
    -------
    List[str]
        Filtered list of expiration dates near the catalyst.

    Examples
    --------
    >>> expirations = ["2024-01-19", "2024-01-26", "2024-02-02"]
    >>> catalyst = date(2024, 1, 25)  # earnings date
    >>> filter_by_catalyst_proximity(expirations, catalyst)
    ['2024-01-26']
    """
    # pylint: disable=import-outside-toplevel
    from datetime import datetime

    filtered = []
    catalyst_dt = catalyst_date if isinstance(catalyst_date, dateType) else catalyst_date

    for exp_str in options_expirations:
        try:
            exp_date = datetime.strptime(exp_str[:10], "%Y-%m-%d").date()
            days_diff = (exp_date - catalyst_dt).days

            # Expiration should be after catalyst (or just before for pre-event plays)
            # and within the specified window
            if -days_before <= days_diff <= days_after:
                filtered.append(exp_str)
        except (ValueError, TypeError):
            continue

    return filtered


def find_nearest_post_catalyst_expiration(
    options_expirations: List[str],
    catalyst_date: dateType,
    min_days_after: int = 1,
    max_days_after: int = 14,
) -> Optional[str]:
    """Find the nearest option expiration after a catalyst event.

    Parameters
    ----------
    options_expirations : List[str]
        List of expiration dates in YYYY-MM-DD format.
    catalyst_date : date
        The catalyst event date.
    min_days_after : int
        Minimum days after catalyst. Default 1 (day after).
    max_days_after : int
        Maximum days after catalyst to search. Default 14.

    Returns
    -------
    Optional[str]
        The nearest post-catalyst expiration, or None if not found.
    """
    # pylint: disable=import-outside-toplevel
    from datetime import datetime

    valid_expirations = []
    catalyst_dt = catalyst_date if isinstance(catalyst_date, dateType) else catalyst_date

    for exp_str in options_expirations:
        try:
            exp_date = datetime.strptime(exp_str[:10], "%Y-%m-%d").date()
            days_diff = (exp_date - catalyst_dt).days

            if min_days_after <= days_diff <= max_days_after:
                valid_expirations.append((exp_str, days_diff))
        except (ValueError, TypeError):
            continue

    if not valid_expirations:
        return None

    # Sort by days after and return the nearest
    valid_expirations.sort(key=lambda x: x[1])
    return valid_expirations[0][0]


def screen_options_before_earnings(
    options_df: "DataFrame",
    earnings_date: dateType,
    underlying_price: float,
    min_iv: Optional[float] = None,
    max_strike_distance_pct: float = 10.0,
    option_type: Optional[Literal["call", "put"]] = None,
) -> "DataFrame":
    """Screen options for pre-earnings plays.

    Finds options expiring after earnings with high IV and near-ATM strikes.

    Parameters
    ----------
    options_df : DataFrame
        Options chain DataFrame with columns: strike, expiration, implied_volatility, option_type.
    earnings_date : date
        The earnings announcement date.
    underlying_price : float
        Current price of the underlying.
    min_iv : Optional[float]
        Minimum implied volatility filter (as decimal, e.g., 0.30 for 30%).
    max_strike_distance_pct : float
        Maximum distance from ATM as percentage. Default 10%.
    option_type : Optional[Literal["call", "put"]]
        Filter by option type. None includes both.

    Returns
    -------
    DataFrame
        Filtered options suitable for earnings plays.
    """
    # pylint: disable=import-outside-toplevel
    from datetime import datetime

    from pandas import DataFrame

    if options_df.empty:
        return DataFrame()

    df = options_df.copy()

    # Parse expiration dates
    if "expiration" in df.columns:
        # Convert to date objects for comparison
        def parse_exp(x):
            if isinstance(x, dateType):
                return x
            try:
                return datetime.strptime(str(x)[:10], "%Y-%m-%d").date()
            except (ValueError, TypeError):
                return None

        df["_exp_date"] = df["expiration"].apply(parse_exp)

        # Filter for expirations after earnings
        df = df[df["_exp_date"] > earnings_date]

        # Find the first expiration after earnings
        if not df.empty:
            first_exp = df["_exp_date"].min()
            # Keep only options expiring on the first post-earnings date
            df = df[df["_exp_date"] == first_exp]
            df = df.drop(columns=["_exp_date"])

    if df.empty:
        return DataFrame()

    # Filter by strike distance from ATM
    if "strike" in df.columns:
        strike_distance_pct = abs(df["strike"] - underlying_price) / underlying_price * 100
        df = df[strike_distance_pct <= max_strike_distance_pct]

    if df.empty:
        return DataFrame()

    # Filter by minimum IV
    if min_iv is not None and "implied_volatility" in df.columns:
        # Normalize IV if in percentage form
        iv_col = df["implied_volatility"]
        normalized_iv = iv_col.apply(lambda x: x / 100 if x > 10 else x)
        df = df[normalized_iv >= min_iv]

    # Filter by option type
    if option_type is not None and "option_type" in df.columns:
        df = df[df["option_type"] == option_type]

    return df.reset_index(drop=True)


def calculate_earnings_iv_premium(
    pre_earnings_iv: float,
    post_earnings_iv: float,
) -> Dict[str, float]:
    """Calculate the IV crush after earnings.

    Parameters
    ----------
    pre_earnings_iv : float
        IV before earnings (as decimal).
    post_earnings_iv : float
        IV after earnings (as decimal).

    Returns
    -------
    Dict[str, float]
        Dictionary with iv_crush (absolute), iv_crush_pct (relative percentage).

    Examples
    --------
    >>> calculate_earnings_iv_premium(0.50, 0.30)
    {'iv_crush': 0.2, 'iv_crush_pct': 40.0}
    """
    iv_crush = pre_earnings_iv - post_earnings_iv
    iv_crush_pct = (iv_crush / pre_earnings_iv * 100) if pre_earnings_iv > 0 else 0

    return {
        "iv_crush": round(iv_crush, 4),
        "iv_crush_pct": round(iv_crush_pct, 2),
    }


def score_catalyst_play(
    expected_move_pct: float,
    iv_rank: float,
    days_to_catalyst: int,
    days_to_expiration: int,
) -> Dict[str, Any]:
    """Score an options catalyst play based on key metrics.

    Higher scores indicate potentially better setups for volatility plays.

    Parameters
    ----------
    expected_move_pct : float
        Expected move as percentage (from straddle price).
    iv_rank : float
        Current IV rank (0-100).
    days_to_catalyst : int
        Days until the catalyst event.
    days_to_expiration : int
        Days until option expiration.

    Returns
    -------
    Dict[str, Any]
        Dictionary with score (0-100), and individual component scores.
    """
    # IV Rank score: higher IV rank = higher score for selling premium
    iv_score = iv_rank

    # Time alignment score: expiration should be shortly after catalyst
    days_after_catalyst = days_to_expiration - days_to_catalyst
    if days_after_catalyst < 0:
        # Expiration before catalyst - not ideal
        time_score = max(0, 50 + days_after_catalyst * 10)
    elif days_after_catalyst <= 3:
        # Sweet spot: expiring 1-3 days after catalyst
        time_score = 100
    elif days_after_catalyst <= 7:
        # Good: within a week after
        time_score = 80
    else:
        # Further out - less theta capture
        time_score = max(30, 80 - (days_after_catalyst - 7) * 5)

    # Expected move score: larger expected move = more opportunity
    if expected_move_pct < 2:
        move_score = 20
    elif expected_move_pct < 5:
        move_score = 50
    elif expected_move_pct < 10:
        move_score = 80
    else:
        move_score = 100

    # Composite score (weighted average)
    composite_score = (iv_score * 0.4) + (time_score * 0.35) + (move_score * 0.25)

    return {
        "composite_score": round(composite_score, 1),
        "iv_rank_score": round(iv_score, 1),
        "time_alignment_score": round(time_score, 1),
        "expected_move_score": round(move_score, 1),
        "recommendation": _get_recommendation(composite_score, iv_rank),
    }


def _get_recommendation(score: float, iv_rank: float) -> str:
    """Get a trading recommendation based on score and IV rank."""
    if score >= 80 and iv_rank >= 70:
        return "Strong sell premium candidate (high IV, good timing)"
    if score >= 80 and iv_rank < 30:
        return "Strong buy premium candidate (low IV, good timing)"
    if score >= 60:
        return "Moderate opportunity (consider position sizing)"
    if score >= 40:
        return "Weak setup (proceed with caution)"
    return "Poor setup (consider waiting for better entry)"


def combine_catalysts_with_options(
    options_expirations: List[str],
    catalysts: List[Dict[str, Any]],
    catalyst_date_field: str = "date",
    catalyst_name_field: str = "name",
) -> List[Dict[str, Any]]:
    """Combine catalyst events with relevant option expirations.

    Parameters
    ----------
    options_expirations : List[str]
        List of option expiration dates (YYYY-MM-DD format).
    catalysts : List[Dict[str, Any]]
        List of catalyst events with date and description fields.
    catalyst_date_field : str
        Field name for the catalyst date. Default "date".
    catalyst_name_field : str
        Field name for the catalyst name/description. Default "name".

    Returns
    -------
    List[Dict[str, Any]]
        List of combined records with catalyst info and relevant expirations.
    """
    # pylint: disable=import-outside-toplevel
    from datetime import datetime

    results = []

    for catalyst in catalysts:
        catalyst_date = catalyst.get(catalyst_date_field)
        if catalyst_date is None:
            continue

        # Parse date if string
        if isinstance(catalyst_date, str):
            try:
                catalyst_date = datetime.strptime(catalyst_date[:10], "%Y-%m-%d").date()
            except (ValueError, TypeError):
                continue

        # Find relevant expirations
        relevant_exps = filter_by_catalyst_proximity(
            options_expirations, catalyst_date, days_before=5, days_after=7
        )

        nearest_post = find_nearest_post_catalyst_expiration(
            options_expirations, catalyst_date
        )

        if relevant_exps or nearest_post:
            results.append({
                "catalyst_date": catalyst_date.strftime("%Y-%m-%d"),
                "catalyst_name": catalyst.get(catalyst_name_field, "Unknown"),
                "catalyst_type": catalyst.get("type", "event"),
                "relevant_expirations": relevant_exps,
                "nearest_post_catalyst_expiration": nearest_post,
                "days_to_catalyst": (catalyst_date - dateType.today()).days,
            })

    # Sort by days to catalyst
    results.sort(key=lambda x: x["days_to_catalyst"])

    return results
