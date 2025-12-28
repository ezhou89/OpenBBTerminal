"""Options Router."""

from typing import Literal, Optional, Union

from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.example import APIEx, PythonEx
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import (
    ExtraParams,
    ProviderChoices,
    StandardParams,
)
from openbb_core.app.query import Query
from openbb_core.app.router import Router
from openbb_core.provider.abstract.data import Data
from openbb_core.provider.standard_models.options_chains import OptionsChainsData

router = Router(prefix="/options")

# pylint: disable=unused-argument


@router.command(
    model="OptionsChains",
    examples=[
        APIEx(parameters={"symbol": "AAPL", "provider": "intrinio"}),
        APIEx(
            description='Use the "date" parameter to get the end-of-day-data for a specific date, where supported.',
            parameters={"symbol": "AAPL", "date": "2023-01-25", "provider": "intrinio"},
        ),
    ],
)
async def chains(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Get the complete options chain for a ticker."""
    return await OBBject.from_query(Query(**locals()))


@router.command(
    methods=["POST"],
    examples=[
        PythonEx(
            description="Filter and process options chains data for volatility.",
            code=[
                "data = obb.derivatives.options.chains('AAPL', provider='cboe')",
                "surface = "
                + "obb.derivatives.options.surface(data=data.results, moneyness=20, dte_min=10, dte_max=60, chart=True)",
                "surface.show()",
            ],
        ),
    ],
)
async def surface(  # pylint: disable=R0913, R0917
    data: Union[list[Data], Data],
    target: str = "implied_volatility",
    underlying_price: Optional[float] = None,
    option_type: Optional[Literal["otm", "itm", "calls", "puts"]] = "otm",
    dte_min: Optional[int] = None,
    dte_max: Optional[int] = None,
    moneyness: Optional[float] = None,
    strike_min: Optional[float] = None,
    strike_max: Optional[float] = None,
    oi: bool = False,
    volume: bool = False,
    theme: Literal["dark", "light"] = "dark",
    chart_params: Optional[dict] = None,
) -> OBBject:
    """Filter and process the options chains data for volatility.

    Data posted can be an instance of OptionsChainsData,
    a pandas DataFrame, or a list of dictionaries.
    Data should contain the fields:

    - `expiration`: The expiration date of the option.
    - `strike`: The strike price of the option.
    - `option_type`: The type of the option (call or put).
    - `implied_volatility`: The implied volatility of the option. Or 'target' field.
    - `open_interest`: The open interest of the option.
    - `volume`: The trading volume of the option.
    - `dte` : Optional, days to expiration (DTE) of the option.
    - `underlying_price`: Optional, the price of the underlying asset.

    Results from the `/derivatives/options/chains` endpoint are the preferred input.

    If `underlying_price` is not supplied in the data as a field, it must be provided as a parameter.

    Parameters
    -----------
    data: Union[list[Data], Data]
    target: str
        The field to use as the z-axis. Default is "implied_volatility".
    underlying_price: Optional[float]
        The price of the underlying asset.
    option_type: Optional[str] = "otm"
        The type of df to display. Default is "otm".
        Choices are: ["otm", "itm", "puts", "calls"]
    dte_min: Optional[int] = None
        Minimum days to expiration (DTE) to filter options.
    dte_max: Optional[int] = None
        Maximum days to expiration (DTE) to filter options.
    moneyness: Optional[float] = None
        Specify a % moneyness to target for display,
        entered as a value between 0 and 100.
    strike_min: Optional[float] = None
        Minimum strike price to filter options.
    strike_max: Optional[float] = None
        Maximum strike price to filter options.
    oi: bool = False
        Filter for only options that have open interest. Default is False.
    volume: bool = False
        Filter for only options that have trading volume. Default is False.
    chart: bool = False
        Whether to return a chart or not. Default is False.
        Only valid if `openbb-charting` is installed.
    theme: Literal["dark", "light"] = "dark"
        The theme to use for the chart. Default is "dark".
        Only valid if `openbb-charting` is installed.
    chart_params: Optional[dict] = None
        Additional parameters to pass to the charting library.
        Only valid if `openbb-charting` is installed.
        Valid keys are:
        - `title`: The title of the chart.
        - `xtitle`: Title for the x-axis.
        - `ytitle`: Title for the y-axis.
        - `ztitle`: Title for the z-axis.
        - `colorscale`: The colorscale to use for the chart.
        - `layout_kwargs`: Additional dictionary to be passed to `fig.update_layout` before output.

    Returns
    -------
    OBBject[list]
        An OBBject containing the processed options data.
        Results are a list of dictionaries.
    """
    # pylint: disable=import-outside-toplevel
    from datetime import datetime  # noqa
    from pandas import concat, DataFrame

    df = DataFrame()

    if not data:
        raise OpenBBError("No data to process!")

    if isinstance(data, OptionsChainsData):
        df = data.dataframe
    elif isinstance(data, DataFrame):
        df = data
    elif isinstance(data, dict) and all(isinstance(v, list) for v in data.values()):
        df = DataFrame(data)
    elif isinstance(data, list):
        if all(isinstance(d, dict) for d in data):
            df = DataFrame(data)
        elif all(isinstance(d, Data) for d in data):
            df = DataFrame(
                [d.model_dump(exclude_none=True, exclude_unset=True) for d in data]  # type: ignore
            )

    options = DataFrame(df.copy())

    last_price = underlying_price or options.underlying_price.iloc[0]  # type: ignore

    if last_price is None:
        raise OpenBBError(
            ValueError(
                "Last price must be provided for options filtering, and was not found in the data."
            )
        )

    if target not in options.columns:  # type: ignore
        raise OpenBBError(f"Error: No {target} field found.")
    if "dte" not in options.columns:  # type: ignore
        options.dte = (options.expiration - datetime.today().date()).days  # type: ignore

    calls = options.query(f"`option_type` == 'call' and `dte` >= 0 and `{target}` > 0")  # type: ignore
    puts = options.query(f"`option_type` == 'put' and `dte` >= 0 and `{target}` > 0")  # type: ignore

    if oi:
        calls = calls[calls["open_interest"] > 0]
        puts = puts[puts["open_interest"] > 0]

    if volume:
        calls = calls[calls["volume"] > 0]
        puts = puts[puts["volume"] > 0]

    if dte_min is not None:
        calls = calls.query("dte >= @dte_min")  # type: ignore
        puts = puts.query("dte >= @dte_min")  # type: ignore

    if dte_max is not None:
        calls = calls.query("dte <= @dte_max")  # type: ignore
        puts = puts.query("dte <= @dte_max")  # type: ignore

    if moneyness is not None and moneyness > 0:
        moneyness = float(moneyness)
        high = (  # noqa:F841 pylint: disable=unused-variable  # type: ignore
            1 + (moneyness / 100)
        ) * last_price
        low = (  # noqa:F841 pylint: disable=unused-variable  # type: ignore
            1 - (moneyness / 100)
        ) * last_price
        calls = calls.query("@low <= `strike` <= @high")  # type: ignore
        puts = puts.query("@low <= `strike` <= @high")  # type: ignore

    if strike_min is not None:
        calls = calls.query("strike >= @strike_min")  # type: ignore
        puts = puts.query("strike >= @strike_min")  # type: ignore

    if strike_max is not None:
        calls = calls.query("strike <= @strike_max")  # type: ignore
        puts = puts.query("strike <= @strike_max")  # type: ignore

    if option_type in ["otm", "itm"] and last_price is None:
        raise RuntimeError(
            "Last price must be provided for OTM/ITM options filtering,"
            " and was not found in the data."
        )

    if option_type is not None and option_type == "otm":
        otm_calls = calls.query("strike > @last_price").set_index(  # type: ignore
            ["expiration", "strike", "option_type"]
        )
        otm_puts = puts.query("strike < @last_price").set_index(  # type: ignore
            ["expiration", "strike", "option_type"]
        )
        df = concat([otm_calls, otm_puts]).sort_index().reset_index()
    elif option_type is not None and option_type == "itm":
        itm_calls = calls.query("strike < @last_price").set_index(  # type: ignore
            ["expiration", "strike", "option_type"]
        )
        itm_puts = puts.query("strike > @last_price").set_index(  # type: ignore
            ["expiration", "strike", "option_type"]
        )
        df = concat([itm_calls, itm_puts]).sort_index().reset_index()
    elif option_type is not None and option_type == "calls":
        df = calls
    elif option_type is not None and option_type == "puts":
        df = puts

    df = DataFrame(
        df[  # type: ignore
            [
                "expiration",
                "strike",
                "option_type",
                "dte",
                target,
                "open_interest",
                "volume",
            ]
        ]
    )

    return OBBject(results=df.to_dict(orient="records"))


@router.command(
    model="OptionsUnusual",
    examples=[
        APIEx(parameters={"symbol": "TSLA", "provider": "intrinio"}),
        APIEx(
            description="Use the 'symbol' parameter to get the most recent activity for a specific symbol.",
            parameters={"symbol": "TSLA", "provider": "intrinio"},
        ),
    ],
)
async def unusual(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Get the complete options chain for a ticker."""
    return await OBBject.from_query(Query(**locals()))


@router.command(
    model="OptionsSnapshots",
    examples=[
        APIEx(
            parameters={"provider": "intrinio"},
        ),
    ],
)
async def snapshots(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Get a snapshot of the options market universe."""
    return await OBBject.from_query(Query(**locals()))


@router.command(
    methods=["POST"],
    examples=[
        PythonEx(
            description="Screen options for earnings plays.",
            code=[
                "import datetime",
                "data = obb.derivatives.options.chains('AAPL', provider='cboe')",
                "earnings_date = datetime.date(2024, 2, 1)",
                "screened = obb.derivatives.options.catalyst_screen(",
                "    data=data.results,",
                "    catalyst_date=earnings_date,",
                "    max_strike_distance_pct=5.0",
                ")",
            ],
        ),
    ],
)
async def catalyst_screen(  # pylint: disable=R0913, R0917
    data: Union[list[Data], Data],
    catalyst_date: str,
    underlying_price: Optional[float] = None,
    min_iv: Optional[float] = None,
    max_strike_distance_pct: float = 10.0,
    option_type: Optional[Literal["call", "put"]] = None,
    include_scoring: bool = True,
) -> OBBject:
    """Screen options for catalyst plays (earnings, FDA events, etc.).

    Finds options expiring shortly after a catalyst event, filtered by
    IV and proximity to ATM strikes.

    Parameters
    ----------
    data : Union[list[Data], Data]
        Options chain data from /derivatives/options/chains endpoint.
    catalyst_date : str
        The catalyst event date in YYYY-MM-DD format (e.g., earnings date).
    underlying_price : Optional[float]
        The current price of the underlying. If not provided, extracted from data.
    min_iv : Optional[float]
        Minimum implied volatility filter (as decimal, e.g., 0.30 for 30%).
    max_strike_distance_pct : float
        Maximum distance from ATM as percentage. Default 10%.
    option_type : Optional[Literal["call", "put"]]
        Filter by option type. None includes both.
    include_scoring : bool
        If True, includes catalyst play scoring metrics. Default True.

    Returns
    -------
    OBBject[list]
        Filtered options suitable for catalyst plays.
    """
    # pylint: disable=import-outside-toplevel
    from datetime import datetime

    from pandas import DataFrame

    from openbb_core.provider.utils.catalyst_screener import (
        score_catalyst_play,
        screen_options_before_earnings,
    )
    from openbb_core.provider.utils.iv_analytics import get_atm_iv

    df = DataFrame()

    if not data:
        raise OpenBBError("No data to process!")

    if isinstance(data, OptionsChainsData):
        df = data.dataframe
    elif isinstance(data, DataFrame):
        df = data
    elif isinstance(data, dict) and all(isinstance(v, list) for v in data.values()):
        df = DataFrame(data)
    elif isinstance(data, list):
        if all(isinstance(d, dict) for d in data):
            df = DataFrame(data)
        elif all(isinstance(d, Data) for d in data):
            df = DataFrame(
                [d.model_dump(exclude_none=True, exclude_unset=True) for d in data]
            )

    if df.empty:
        raise OpenBBError("No valid data provided!")

    # Parse catalyst date
    try:
        catalyst_dt = datetime.strptime(catalyst_date, "%Y-%m-%d").date()
    except ValueError as e:
        raise OpenBBError(f"Invalid date format. Use YYYY-MM-DD: {e}") from e

    # Get underlying price
    last_price = underlying_price
    if last_price is None and "underlying_price" in df.columns:
        last_price = df["underlying_price"].iloc[0]
    if last_price is None:
        raise OpenBBError(
            "underlying_price must be provided or present in the data."
        )

    # Screen options
    screened = screen_options_before_earnings(
        options_df=df,
        earnings_date=catalyst_dt,
        underlying_price=last_price,
        min_iv=min_iv,
        max_strike_distance_pct=max_strike_distance_pct,
        option_type=option_type,
    )

    if screened.empty:
        return OBBject(results=[])

    results = screened.to_dict(orient="records")

    # Add scoring if requested
    if include_scoring and results:
        today = datetime.today().date()
        days_to_catalyst = (catalyst_dt - today).days

        # Get ATM IV for IV rank approximation (simplified)
        atm_iv = get_atm_iv(df, last_price)
        iv_rank = 50.0  # Default if no historical data available

        for record in results:
            exp_str = str(record.get("expiration", ""))[:10]
            try:
                exp_date = datetime.strptime(exp_str, "%Y-%m-%d").date()
                dte = (exp_date - today).days
            except (ValueError, TypeError):
                dte = 30

            # Calculate expected move percent from straddle cost if available
            record_iv = record.get("implied_volatility", atm_iv or 0.3)
            if record_iv and record_iv > 10:
                record_iv = record_iv / 100
            expected_move_pct = record_iv * ((dte / 365) ** 0.5) * 100 if record_iv else 5.0

            score_info = score_catalyst_play(
                expected_move_pct=expected_move_pct,
                iv_rank=iv_rank,
                days_to_catalyst=days_to_catalyst,
                days_to_expiration=dte,
            )
            record["catalyst_score"] = score_info["composite_score"]
            record["recommendation"] = score_info["recommendation"]

    return OBBject(results=results)
