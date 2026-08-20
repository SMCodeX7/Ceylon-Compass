import pandas as pd


TRAVEL_STYLE_FACTORS = {
    "Budget": 0.85,
    "Balanced": 1.00,
    "Comfort": 1.25,
}


TRANSPORT_COST_PER_KM = {
    "Public Transport": 0.05,
    "Mixed Transport": 0.12,
    "Private Vehicle": 0.22,
}


def calculate_destination_cost(
    itinerary: pd.DataFrame,
    travel_style: str,
) -> float:
    """
    Estimate destination-related trip cost.

    Only scheduled destinations are included.

    estimated_daily_cost_usd is scaled according to
    the fraction of one 8-hour activity day used at
    each destination.

    A travel-style factor is then applied.
    """

    if travel_style not in TRAVEL_STYLE_FACTORS:
        raise ValueError(
            f"Unsupported travel style: {travel_style}"
        )

    required_columns = {
        "scheduled",
        "estimated_daily_cost_usd",
        "recommended_duration_hours",
    }

    missing_columns = (
        required_columns
        - set(itinerary.columns)
    )

    if missing_columns:
        raise ValueError(
            "Itinerary data is missing budget columns: "
            + ", ".join(sorted(missing_columns))
        )

    if itinerary.empty:
        return 0.0

    scheduled = itinerary[
        itinerary["scheduled"]
    ].copy()

    if scheduled.empty:
        return 0.0

    costs = (
        scheduled[
            "estimated_daily_cost_usd"
        ].astype(float)
    )

    durations = (
        scheduled[
            "recommended_duration_hours"
        ].astype(float)
    )

    if (costs < 0).any():
        raise ValueError(
            "Destination cost cannot be negative."
        )

    if (durations <= 0).any():
        raise ValueError(
            "Destination duration must be greater than 0."
        )

    activity_day_fraction = (
        durations / 8.0
    )

    base_cost = (
        costs
        * activity_day_fraction
    ).sum()

    style_factor = (
        TRAVEL_STYLE_FACTORS[
            travel_style
        ]
    )

    return round(
        float(
            base_cost
            * style_factor
        ),
        2,
    )


def calculate_transport_cost(
    itinerary: pd.DataFrame,
    transport: str,
) -> float:
    """
    Estimate route transportation cost using the
    geographic route-distance proxy.

    The per-kilometre values are transparent modelling
    assumptions used for comparison between transport
    preferences.
    """

    if transport not in TRANSPORT_COST_PER_KM:
        raise ValueError(
            f"Unsupported transport: {transport}"
        )

    if (
        "distance_from_previous_km"
        not in itinerary.columns
    ):
        raise ValueError(
            "Itinerary data is missing "
            "distance_from_previous_km."
        )

    if itinerary.empty:
        return 0.0

    scheduled = itinerary[
        itinerary["scheduled"]
    ].copy()

    if scheduled.empty:
        return 0.0

    distances = (
        scheduled[
            "distance_from_previous_km"
        ].astype(float)
    )

    if (distances < 0).any():
        raise ValueError(
            "Travel distance cannot be negative."
        )

    total_distance = float(
        distances.sum()
    )

    transport_rate = (
        TRANSPORT_COST_PER_KM[
            transport
        ]
    )

    return round(
        total_distance
        * transport_rate,
        2,
    )


def estimate_trip_budget(
    itinerary: pd.DataFrame,
    total_budget_usd: float,
    travel_style: str,
    transport: str,
) -> dict:
    """
    Estimate overall trip spending for the scheduled
    itinerary.

    Returns a transparent budget breakdown including
    estimated spending and remaining or exceeded
    budget.
    """

    if total_budget_usd <= 0:
        raise ValueError(
            "Total budget must be greater than 0."
        )

    destination_cost = (
        calculate_destination_cost(
            itinerary,
            travel_style,
        )
    )

    transport_cost = (
        calculate_transport_cost(
            itinerary,
            transport,
        )
    )

    estimated_total = round(
        destination_cost
        + transport_cost,
        2,
    )

    budget_difference = round(
        total_budget_usd
        - estimated_total,
        2,
    )

    within_budget = (
        estimated_total
        <= total_budget_usd
    )

    return {
        "total_budget_usd": round(
            float(total_budget_usd),
            2,
        ),
        "destination_cost_usd": (
            destination_cost
        ),
        "transport_cost_usd": (
            transport_cost
        ),
        "estimated_total_cost_usd": (
            estimated_total
        ),
        "budget_difference_usd": (
            budget_difference
        ),
        "within_budget": (
            within_budget
        ),
    }