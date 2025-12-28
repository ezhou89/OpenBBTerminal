"""Unified Options Research Utilities.

This module provides a unified interface for options research combining
options chain data, catalyst calendars, IV analytics, and expected move calculations.
"""

from datetime import date as dateType
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from pandas import DataFrame


def build_research_summary(
    symbol: str,
    underlying_price: float,
    options_expirations: List[str],
    earnings_date: Optional[dateType] = None,
    clinical_trials: Optional[List[Dict[str, Any]]] = None,
    atm_iv: Optional[float] = None,
    iv_rank: Optional[float] = None,
    iv_percentile: Optional[float] = None,
) -> Dict[str, Any]:
    """Build a comprehensive options research summary for a symbol.

    Combines multiple data sources into a unified research view.

    Parameters
    ----------
    symbol : str
        The ticker symbol.
    underlying_price : float
        Current price of the underlying.
    options_expirations : List[str]
        Available option expiration dates (YYYY-MM-DD format).
    earnings_date : Optional[date]
        Next earnings announcement date.
    clinical_trials : Optional[List[Dict]]
        List of relevant clinical trial records.
    atm_iv : Optional[float]
        Current ATM implied volatility.
    iv_rank : Optional[float]
        Current IV rank (0-100).
    iv_percentile : Optional[float]
        Current IV percentile (0-100).

    Returns
    -------
    Dict[str, Any]
        Comprehensive research summary with sections for:
        - overview: symbol, price, IV metrics
        - catalysts: upcoming events with dates
        - strategy_ideas: suggested strategies based on conditions
        - expirations: organized by catalyst proximity
    """
    # pylint: disable=import-outside-toplevel
    from openbb_core.provider.utils.catalyst_screener import (
        filter_by_catalyst_proximity,
        find_nearest_post_catalyst_expiration,
    )
    from openbb_core.provider.utils.iv_analytics import calculate_expected_move

    summary: Dict[str, Any] = {
        "symbol": symbol,
        "underlying_price": underlying_price,
        "overview": {},
        "catalysts": [],
        "strategy_ideas": [],
        "expirations_by_catalyst": {},
    }

    # Overview section
    summary["overview"] = {
        "atm_iv": atm_iv,
        "iv_rank": iv_rank,
        "iv_percentile": iv_percentile,
        "iv_environment": _classify_iv_environment(iv_rank, iv_percentile),
    }

    # Calculate expected moves for different time horizons
    if atm_iv:
        normalized_iv = atm_iv if atm_iv < 10 else atm_iv / 100
        for days in [7, 14, 30, 45]:
            move, pct, (low, high) = calculate_expected_move(
                underlying_price, normalized_iv, days
            )
            summary["overview"][f"expected_move_{days}d"] = {
                "dollars": move,
                "percent": pct,
                "range": (low, high),
            }

    # Catalysts section
    today = dateType.today()

    if earnings_date:
        days_to_earnings = (earnings_date - today).days
        earnings_info = {
            "type": "earnings",
            "date": earnings_date.strftime("%Y-%m-%d"),
            "days_until": days_to_earnings,
            "relevant_expirations": filter_by_catalyst_proximity(
                options_expirations, earnings_date, days_before=5, days_after=7
            ),
            "nearest_post_expiration": find_nearest_post_catalyst_expiration(
                options_expirations, earnings_date
            ),
        }
        summary["catalysts"].append(earnings_info)

        # Add expirations organized by earnings
        summary["expirations_by_catalyst"]["earnings"] = earnings_info["relevant_expirations"]

    if clinical_trials:
        for trial in clinical_trials[:5]:  # Limit to top 5 trials
            trial_date = trial.get("primary_completion_date")
            if trial_date:
                if isinstance(trial_date, str):
                    try:
                        from datetime import datetime
                        trial_date = datetime.strptime(trial_date[:10], "%Y-%m-%d").date()
                    except (ValueError, TypeError):
                        continue

                days_to_trial = (trial_date - today).days
                if days_to_trial > 0:  # Only future trials
                    trial_info = {
                        "type": "clinical_trial",
                        "name": trial.get("brief_title", trial.get("title", "Unknown")),
                        "phase": trial.get("phase"),
                        "date": trial_date.strftime("%Y-%m-%d"),
                        "days_until": days_to_trial,
                        "nct_id": trial.get("nct_id"),
                        "relevant_expirations": filter_by_catalyst_proximity(
                            options_expirations, trial_date, days_before=5, days_after=14
                        ),
                    }
                    summary["catalysts"].append(trial_info)

    # Sort catalysts by days until
    summary["catalysts"].sort(key=lambda x: x.get("days_until", 999))

    # Strategy ideas based on conditions
    summary["strategy_ideas"] = _generate_strategy_ideas(
        iv_rank=iv_rank,
        iv_percentile=iv_percentile,
        has_near_catalyst=any(
            c.get("days_until", 999) <= 14 for c in summary["catalysts"]
        ),
        options_expirations=options_expirations,
    )

    return summary


def _classify_iv_environment(
    iv_rank: Optional[float],
    iv_percentile: Optional[float],
) -> str:
    """Classify the current IV environment."""
    if iv_rank is None and iv_percentile is None:
        return "unknown"

    # Use IV rank as primary, percentile as fallback
    iv_metric = iv_rank if iv_rank is not None else iv_percentile

    if iv_metric >= 80:
        return "very_high"
    if iv_metric >= 60:
        return "elevated"
    if iv_metric >= 40:
        return "neutral"
    if iv_metric >= 20:
        return "low"
    return "very_low"


def _generate_strategy_ideas(
    iv_rank: Optional[float],
    iv_percentile: Optional[float],
    has_near_catalyst: bool,
    options_expirations: List[str],
) -> List[Dict[str, Any]]:
    """Generate strategy ideas based on current conditions."""
    ideas = []
    iv_metric = iv_rank if iv_rank is not None else iv_percentile

    if iv_metric is not None:
        if iv_metric >= 70:
            # High IV - favor selling premium
            ideas.append({
                "strategy": "iron_condor",
                "rationale": f"IV Rank at {iv_metric:.0f}% suggests elevated premium levels",
                "bias": "neutral",
                "risk_profile": "defined_risk",
            })
            ideas.append({
                "strategy": "short_strangle",
                "rationale": "Sell premium when IV is rich",
                "bias": "neutral",
                "risk_profile": "undefined_risk",
            })
            if has_near_catalyst:
                ideas.append({
                    "strategy": "short_straddle_pre_earnings",
                    "rationale": "Capture IV crush post-catalyst, but manage gamma risk",
                    "bias": "neutral",
                    "risk_profile": "high_risk",
                    "timing_note": "Enter 1-2 days before, exit immediately after",
                })

        elif iv_metric <= 30:
            # Low IV - favor buying premium
            ideas.append({
                "strategy": "long_straddle",
                "rationale": f"IV Rank at {iv_metric:.0f}% suggests cheap premium",
                "bias": "neutral",
                "risk_profile": "defined_risk",
            })
            ideas.append({
                "strategy": "calendar_spread",
                "rationale": "Buy cheap front-month IV, sell back-month",
                "bias": "directional",
                "risk_profile": "defined_risk",
            })
            if has_near_catalyst:
                ideas.append({
                    "strategy": "long_straddle_pre_catalyst",
                    "rationale": "Buy cheap premium before catalyst-driven IV expansion",
                    "bias": "neutral",
                    "risk_profile": "defined_risk",
                    "timing_note": "Enter 5-10 days before, exit before or right after",
                })

        else:
            # Neutral IV
            ideas.append({
                "strategy": "vertical_spread",
                "rationale": "Neutral IV environment favors directional plays with defined risk",
                "bias": "directional",
                "risk_profile": "defined_risk",
            })

    if has_near_catalyst and len(options_expirations) > 2:
        ideas.append({
            "strategy": "post_catalyst_expiration",
            "rationale": "Target first expiration after catalyst for maximum theta capture",
            "bias": "neutral",
            "risk_profile": "varies",
        })

    return ideas


def format_research_report(summary: Dict[str, Any]) -> str:
    """Format the research summary as a readable text report.

    Parameters
    ----------
    summary : Dict[str, Any]
        Research summary from build_research_summary.

    Returns
    -------
    str
        Formatted text report.
    """
    lines = []
    lines.append(f"═══ OPTIONS RESEARCH: {summary['symbol']} ═══")
    lines.append(f"Underlying Price: ${summary['underlying_price']:.2f}")
    lines.append("")

    # Overview
    overview = summary.get("overview", {})
    lines.append("── IV METRICS ──")
    if overview.get("atm_iv"):
        atm_iv = overview["atm_iv"]
        if atm_iv > 10:
            atm_iv = atm_iv / 100
        lines.append(f"ATM IV: {atm_iv:.1%}")
    if overview.get("iv_rank") is not None:
        lines.append(f"IV Rank: {overview['iv_rank']:.0f}%")
    if overview.get("iv_percentile") is not None:
        lines.append(f"IV Percentile: {overview['iv_percentile']:.0f}%")
    lines.append(f"Environment: {overview.get('iv_environment', 'unknown').replace('_', ' ').title()}")
    lines.append("")

    # Expected moves
    for key in ["expected_move_7d", "expected_move_14d", "expected_move_30d"]:
        if key in overview:
            em = overview[key]
            period = key.replace("expected_move_", "").replace("d", "-day")
            lines.append(f"{period} Expected Move: ±${em['dollars']:.2f} ({em['percent']:.1f}%)")
    lines.append("")

    # Catalysts
    catalysts = summary.get("catalysts", [])
    if catalysts:
        lines.append("── UPCOMING CATALYSTS ──")
        for cat in catalysts[:5]:
            cat_type = cat.get("type", "event").replace("_", " ").title()
            lines.append(f"• {cat_type}: {cat.get('date')} ({cat.get('days_until')} days)")
            if cat.get("name"):
                lines.append(f"  {cat['name'][:50]}...")
            if cat.get("nearest_post_expiration"):
                lines.append(f"  → Nearest post-event expiration: {cat['nearest_post_expiration']}")
        lines.append("")

    # Strategy ideas
    ideas = summary.get("strategy_ideas", [])
    if ideas:
        lines.append("── STRATEGY IDEAS ──")
        for idea in ideas[:4]:
            strategy = idea.get("strategy", "").replace("_", " ").title()
            lines.append(f"• {strategy}")
            lines.append(f"  {idea.get('rationale', '')}")
            if idea.get("timing_note"):
                lines.append(f"  Timing: {idea['timing_note']}")
        lines.append("")

    return "\n".join(lines)
