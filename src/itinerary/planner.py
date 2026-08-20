import pandas as pd


DEFAULT_DAILY_ACTIVITY_HOURS = 8.0


def generate_itinerary(
    routed_destinations: pd.DataFrame,
    trip_days: int,
    daily_activity_hours: float = DEFAULT_DAILY_ACTIVITY_HOURS,
) -> pd.DataFrame:
    """
    Allocate route-ordered destinations across trip days.

    Destinations remain in optimized route order.

    Each day can contain up to the configured number
    of activity hours. If a destination no longer fits
    on the current day, it is moved to the next day.

    Destinations that cannot fit within the available
    trip duration are retained and marked unscheduled.
    """

    if trip_days < 1:
        raise ValueError(
            "Trip duration must be at least 1 day."
        )

    if daily_activity_hours <= 0:
        raise ValueError(
            "Daily activity hours must be greater than 0."
        )

    required_columns = {
        "name",
        "route_order",
        "recommended_duration_hours",
    }

    missing_columns = (
        required_columns
        - set(routed_destinations.columns)
    )

    if missing_columns:
        raise ValueError(
            "Route data is missing itinerary columns: "
            + ", ".join(sorted(missing_columns))
        )

    if routed_destinations.empty:
        result = routed_destinations.copy()

        result["itinerary_day"] = pd.Series(
            dtype="Int64"
        )

        result["visit_order_in_day"] = pd.Series(
            dtype="Int64"
        )

        result["scheduled"] = pd.Series(
            dtype=bool
        )

        result["day_activity_hours"] = pd.Series(
            dtype=float
        )

        return result

    itinerary = (
        routed_destinations
        .sort_values("route_order")
        .copy()
        .reset_index(drop=True)
    )

    durations = (
        itinerary["recommended_duration_hours"]
        .astype(float)
    )

    if (durations <= 0).any():
        raise ValueError(
            "Recommended destination duration must "
            "be greater than 0."
        )

    if (
        durations
        > daily_activity_hours
    ).any():
        raise ValueError(
            "A destination requires more activity "
            "time than the daily itinerary limit."
        )

    itinerary_days: list[int | None] = []
    visit_orders: list[int | None] = []
    scheduled_flags: list[bool] = []

    current_day = 1
    used_hours = 0.0
    visit_order = 0

    for duration in durations:
        if (
            used_hours > 0
            and used_hours + duration
            > daily_activity_hours
        ):
            current_day += 1
            used_hours = 0.0
            visit_order = 0

        if current_day > trip_days:
            itinerary_days.append(None)
            visit_orders.append(None)
            scheduled_flags.append(False)
            continue

        visit_order += 1
        used_hours += duration

        itinerary_days.append(current_day)
        visit_orders.append(visit_order)
        scheduled_flags.append(True)

    itinerary["itinerary_day"] = pd.Series(
        itinerary_days,
        dtype="Int64",
    )

    itinerary["visit_order_in_day"] = pd.Series(
        visit_orders,
        dtype="Int64",
    )

    itinerary["scheduled"] = scheduled_flags

    day_totals = (
        itinerary[
            itinerary["scheduled"]
        ]
        .groupby("itinerary_day")[
            "recommended_duration_hours"
        ]
        .sum()
        .to_dict()
    )

    itinerary["day_activity_hours"] = (
        itinerary["itinerary_day"]
        .map(day_totals)
        .astype(float)
    )

    return itinerary


def itinerary_summary(
    itinerary: pd.DataFrame,
) -> dict:
    """
    Return high-level itinerary scheduling statistics.
    """

    if itinerary.empty:
        return {
            "scheduled_destinations": 0,
            "unscheduled_destinations": 0,
            "days_used": 0,
            "total_activity_hours": 0.0,
        }

    scheduled = itinerary[
        itinerary["scheduled"]
    ]

    return {
        "scheduled_destinations": int(
            itinerary["scheduled"].sum()
        ),
        "unscheduled_destinations": int(
            (~itinerary["scheduled"]).sum()
        ),
        "days_used": int(
            scheduled["itinerary_day"].nunique()
        ),
        "total_activity_hours": float(
            scheduled[
                "recommended_duration_hours"
            ].sum()
        ),
    }