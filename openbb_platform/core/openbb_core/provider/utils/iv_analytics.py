"""Implied Volatility Analytics Utilities.

This module provides utilities for calculating IV-based analytics for options trading,
including IV rank, IV percentile, and expected move calculations.
"""

from typing import TYPE_CHECKING, List, Optional, Tuple, Union

if TYPE_CHECKING:
    from pandas import DataFrame, Series


def calculate_iv_rank(
    current_iv: float,
    iv_low: float,
    iv_high: float,
) -> float:
    """Calculate IV Rank (Implied Volatility Rank).

    IV Rank shows where current IV stands relative to its historical range.
    A rank of 0 means IV is at its lowest point, 100 means at its highest.

    Parameters
    ----------
    current_iv : float
        The current implied volatility (as a decimal, e.g., 0.30 for 30%).
    iv_low : float
        The lowest IV in the lookback period.
    iv_high : float
        The highest IV in the lookback period.

    Returns
    -------
    float
        IV Rank as a percentage (0-100).

    Examples
    --------
    >>> calculate_iv_rank(0.35, 0.20, 0.50)
    50.0
    """
    if iv_high == iv_low:
        return 50.0  # If no range, return middle value

    iv_rank = ((current_iv - iv_low) / (iv_high - iv_low)) * 100
    return round(max(0.0, min(100.0, iv_rank)), 2)


def calculate_iv_percentile(
    current_iv: float,
    historical_ivs: List[float],
) -> float:
    """Calculate IV Percentile (Implied Volatility Percentile).

    IV Percentile shows the percentage of days in the lookback period
    that had IV lower than the current IV.

    Parameters
    ----------
    current_iv : float
        The current implied volatility.
    historical_ivs : List[float]
        A list of historical IV values for the lookback period.

    Returns
    -------
    float
        IV Percentile as a percentage (0-100).

    Examples
    --------
    >>> historical = [0.20, 0.25, 0.30, 0.35, 0.40]
    >>> calculate_iv_percentile(0.32, historical)
    60.0
    """
    if not historical_ivs:
        return 50.0

    days_lower = sum(1 for iv in historical_ivs if iv < current_iv)
    percentile = (days_lower / len(historical_ivs)) * 100
    return round(percentile, 2)


def calculate_expected_move(
    underlying_price: float,
    iv: float,
    days_to_expiration: int,
    annualization_factor: int = 365,
) -> Tuple[float, float, float]:
    """Calculate the expected move based on implied volatility.

    The expected move represents a one standard deviation price movement,
    which statistically encompasses about 68% of possible outcomes.

    Parameters
    ----------
    underlying_price : float
        The current price of the underlying asset.
    iv : float
        The implied volatility (as a decimal, e.g., 0.30 for 30%).
    days_to_expiration : int
        The number of days until expiration.
    annualization_factor : int
        The number of days used for annualization. Default is 365.

    Returns
    -------
    Tuple[float, float, float]
        A tuple containing:
        - expected_move: The dollar amount of expected move
        - expected_move_percent: The expected move as a percentage
        - expected_range: Tuple of (lower_bound, upper_bound)

    Examples
    --------
    >>> move, pct, (low, high) = calculate_expected_move(100.0, 0.30, 30)
    >>> print(f"Expected move: ${move:.2f} ({pct:.2f}%)")
    Expected move: $8.60 (8.60%)
    """
    import math

    # Calculate time factor
    time_factor = math.sqrt(days_to_expiration / annualization_factor)

    # Calculate expected move
    expected_move = underlying_price * iv * time_factor
    expected_move_percent = iv * time_factor * 100

    # Calculate expected range
    lower_bound = underlying_price - expected_move
    upper_bound = underlying_price + expected_move

    return (
        round(expected_move, 2),
        round(expected_move_percent, 2),
        (round(lower_bound, 2), round(upper_bound, 2)),
    )


def calculate_expected_move_from_straddle(
    straddle_price: float,
    underlying_price: float,
) -> Tuple[float, float, Tuple[float, float]]:
    """Calculate expected move from ATM straddle price.

    The ATM straddle price is a direct market-implied expected move.
    This method is often more accurate than IV-based calculation as it
    incorporates all market information including skew.

    Parameters
    ----------
    straddle_price : float
        The total cost of the ATM straddle (call + put premiums).
    underlying_price : float
        The current price of the underlying asset.

    Returns
    -------
    Tuple[float, float, Tuple[float, float]]
        A tuple containing:
        - expected_move: The dollar amount of expected move
        - expected_move_percent: The expected move as a percentage
        - expected_range: Tuple of (lower_bound, upper_bound)

    Examples
    --------
    >>> move, pct, (low, high) = calculate_expected_move_from_straddle(8.50, 100.0)
    >>> print(f"Expected move: ${move:.2f} ({pct:.2f}%)")
    Expected move: $8.50 (8.50%)
    """
    expected_move = straddle_price
    expected_move_percent = (straddle_price / underlying_price) * 100

    lower_bound = underlying_price - expected_move
    upper_bound = underlying_price + expected_move

    return (
        round(expected_move, 2),
        round(expected_move_percent, 2),
        (round(lower_bound, 2), round(upper_bound, 2)),
    )


def get_atm_iv(
    options_df: "DataFrame",
    underlying_price: float,
    expiration: Optional[str] = None,
) -> Optional[float]:
    """Extract the at-the-money implied volatility from an options chain.

    Parameters
    ----------
    options_df : DataFrame
        Options chain DataFrame with columns: strike, implied_volatility, option_type, expiration.
    underlying_price : float
        The current price of the underlying asset.
    expiration : Optional[str]
        Specific expiration date (YYYY-MM-DD format). If None, uses nearest expiration.

    Returns
    -------
    Optional[float]
        The ATM implied volatility, or None if not available.
    """
    if options_df.empty:
        return None

    if "implied_volatility" not in options_df.columns:
        return None

    df = options_df.copy()

    # Filter by expiration if specified
    if expiration and "expiration" in df.columns:
        df = df[df["expiration"].astype(str).str[:10] == expiration]
        if df.empty:
            return None

    # Find nearest strike to underlying price
    df["strike_diff"] = abs(df["strike"] - underlying_price)
    atm_strike = df.loc[df["strike_diff"].idxmin(), "strike"]

    # Get IV for ATM options (average of call and put if both available)
    atm_options = df[df["strike"] == atm_strike]

    if "option_type" in atm_options.columns:
        call_iv = atm_options[atm_options["option_type"] == "call"]["implied_volatility"]
        put_iv = atm_options[atm_options["option_type"] == "put"]["implied_volatility"]

        ivs = []
        if not call_iv.empty and call_iv.iloc[0] is not None:
            ivs.append(call_iv.iloc[0])
        if not put_iv.empty and put_iv.iloc[0] is not None:
            ivs.append(put_iv.iloc[0])

        if ivs:
            return sum(ivs) / len(ivs)

    # Fallback: just use the ATM option's IV
    iv = atm_options["implied_volatility"].iloc[0] if not atm_options.empty else None
    return iv if iv is not None else None


def iv_term_structure(
    options_df: "DataFrame",
    underlying_price: float,
) -> "DataFrame":
    """Calculate the IV term structure (IV by expiration).

    Parameters
    ----------
    options_df : DataFrame
        Options chain DataFrame.
    underlying_price : float
        The current price of the underlying asset.

    Returns
    -------
    DataFrame
        DataFrame with expiration dates and corresponding ATM IV values.
    """
    # pylint: disable=import-outside-toplevel
    from pandas import DataFrame

    if options_df.empty or "expiration" not in options_df.columns:
        return DataFrame()

    expirations = options_df["expiration"].unique()
    term_structure = []

    for exp in expirations:
        exp_str = str(exp)[:10]
        iv = get_atm_iv(options_df, underlying_price, exp_str)
        if iv is not None:
            term_structure.append({
                "expiration": exp_str,
                "atm_iv": round(iv, 4) if iv < 10 else round(iv / 100, 4),  # Normalize if needed
            })

    df = DataFrame(term_structure)
    if not df.empty:
        df = df.sort_values("expiration").reset_index(drop=True)

    return df
