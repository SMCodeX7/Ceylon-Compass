from __future__ import annotations

import pandas as pd

from src.optimization.route_baseline import (
    calculate_baseline_route_distance,
    nearest_neighbour_route,
)
from src.planning.service import TripPlan


DEFAULT_EVALUATION_TOP_N = 5
DEFAULT_DAILY_ACTIVITY_HOURS = 8.0


def mean_preference_score(
    plan: TripPlan,
    top_n: int = DEFAULT_EVALUATION_TOP_N,
) -> float:
    """
    Return the mean cosine-based preference score for
    the highest-ranked recommendations.

    This is an internal relevance indicator, not
    ground-truth recommendation accuracy.
    """

    recommendations = (
        plan.recommendations
        .head(top_n)
    )

    if recommendations.empty:
        return 0.0

    return round(
        float(
            recommendations[
                "preference_score"
            ].astype(float).mean()
        ),
        2,
    )


def mean_final_score(
    plan: TripPlan,
    top_n: int = DEFAULT_EVALUATION_TOP_N,
) -> float:
    """
    Return the mean final weighted score of the
    highest-ranked recommendations.
    """

    recommendations = (
        plan.recommendations
        .head(top_n)
    )

    if recommendations.empty:
        return 0.0

    return round(
        float(
            recommendations[
                "final_score"
            ].astype(float).mean()
        ),
        2,
    )


def recommendation_diversity(
    plan: TripPlan,
    top_n: int = DEFAULT_EVALUATION_TOP_N,
) -> dict:
    """
    Measure category diversity among top
    recommendations.

    Diversity percentage is:

        unique categories / evaluated destinations
        * 100
    """

    recommendations = (
        plan.recommendations
        .head(top_n)
    )

    evaluated_count = len(
        recommendations
    )

    if evaluated_count == 0:
        return {
            "unique_category_count": 0,
            "evaluated_destination_count": 0,
            "category_diversity_pct": 0.0,
        }

    unique_categories = int(
        recommendations[
            "category"
        ].nunique()
    )

    diversity_pct = (
        unique_categories
        / evaluated_count
        * 100.0
    )

    return {
        "unique_category_count": (
            unique_categories
        ),
        "evaluated_destination_count": (
            evaluated_count
        ),
        "category_diversity_pct": round(
            diversity_pct,
            2,
        ),
    }


def budget_compliant(
    plan: TripPlan,
) -> bool:
    """
    Return whether the estimated itinerary cost
    remains within the traveller's budget.
    """

    return bool(
        plan.budget[
            "within_budget"
        ]
    )


def itinerary_duration_compliant(
    plan: TripPlan,
    daily_activity_hours: float = (
        DEFAULT_DAILY_ACTIVITY_HOURS
    ),
) -> bool:
    """
    Verify that scheduled itinerary rows remain within
    the traveller's trip duration and the current
    daily activity-hour limit.

    Travel time is not included because the current V1
    itinerary model limits activity time only.
    """

    itinerary = (
        plan.itinerary
    )

    if itinerary.empty:
        return False

    scheduled = (
        itinerary[
            itinerary[
                "scheduled"
            ]
        ].copy()
    )

    if scheduled.empty:
        return False

    itinerary_days = (
        scheduled[
            "itinerary_day"
        ]
        .dropna()
        .astype(int)
    )

    if itinerary_days.empty:
        return False

    valid_days = (
        itinerary_days.min() >= 1
        and itinerary_days.max()
        <= plan.profile.trip_days
    )

    day_activity_totals = (
        scheduled
        .groupby(
            "itinerary_day"
        )[
            "recommended_duration_hours"
        ]
        .sum()
        .astype(float)
    )

    valid_activity_hours = bool(
        (
            day_activity_totals
            <= daily_activity_hours
            + 1e-9
        ).all()
    )

    return bool(
        valid_days
        and valid_activity_hours
    )


def scheduled_destination_coverage(
    plan: TripPlan,
) -> float:
    """
    Measure the percentage of selected route
    destinations that fit into the itinerary.
    """

    route_count = len(
        plan.optimized_route
    )

    if route_count == 0:
        return 0.0

    scheduled_count = int(
        plan.itinerary[
            "scheduled"
        ].sum()
    )

    return round(
        scheduled_count
        / route_count
        * 100.0,
        2,
    )


def itinerary_weather_metrics(
    plan: TripPlan,
) -> dict:
    """
    Summarize weather availability and suitability
    across scheduled itinerary destinations.
    """

    scheduled = (
        plan.itinerary[
            plan.itinerary[
                "scheduled"
            ]
        ].copy()
    )

    scheduled_count = len(
        scheduled
    )

    if (
        scheduled_count == 0
        or "weather_available"
        not in scheduled.columns
    ):
        return {
            "weather_available_count": 0,
            "weather_coverage_pct": 0.0,
            "mean_weather_score": None,
        }

    available = (
        scheduled[
            scheduled[
                "weather_available"
            ]
        ].copy()
    )

    available_count = len(
        available
    )

    coverage = (
        available_count
        / scheduled_count
        * 100.0
    )

    if (
        available_count == 0
        or "weather_score"
        not in available.columns
    ):
        average_score = None
    else:
        average_score = round(
            float(
                available[
                    "weather_score"
                ]
                .astype(float)
                .mean()
            ),
            2,
        )

    return {
        "weather_available_count": (
            available_count
        ),
        "weather_coverage_pct": round(
            coverage,
            2,
        ),
        "mean_weather_score": (
            average_score
        ),
    }


def route_valid(
    plan: TripPlan,
) -> bool:
    """
    Validate basic structural properties of the
    optimized route and itinerary.
    """

    route = (
        plan.optimized_route
    )

    itinerary = (
        plan.itinerary
    )

    if (
        route.empty
        or itinerary.empty
    ):
        return False

    required_columns = {
        "name",
        "route_order",
        "distance_from_previous_km",
    }

    if not required_columns.issubset(
        route.columns
    ):
        return False

    route_orders = (
        route[
            "route_order"
        ]
        .astype(int)
        .tolist()
    )

    expected_orders = list(
        range(
            1,
            len(route) + 1,
        )
    )

    if (
        route_orders
        != expected_orders
    ):
        return False

    route_names = (
        route[
            "name"
        ]
        .astype(str)
        .tolist()
    )

    if (
        len(route_names)
        != len(
            set(
                route_names
            )
        )
    ):
        return False

    itinerary_names = (
        itinerary[
            "name"
        ]
        .astype(str)
        .tolist()
    )

    if (
        itinerary_names
        != route_names
    ):
        return False

    distances = (
        route[
            "distance_from_previous_km"
        ]
        .astype(float)
    )

    if (
        distances < 0
    ).any():
        return False

    return True


def route_comparison_metrics(
    plan: TripPlan,
) -> dict:
    """
    Compare OR-Tools route distance against the
    nearest-neighbour baseline using the same
    destination set.

    Both distances are Haversine geographic proxies,
    not driving-road distances.
    """

    if plan.optimized_route.empty:
        return {
            "baseline_route_distance_km": 0.0,
            "optimized_route_distance_km": 0.0,
            "route_distance_saving_km": 0.0,
            "route_distance_saving_pct": 0.0,
            "optimized_not_worse": True,
        }

    baseline_route = (
        nearest_neighbour_route(
            plan.optimized_route,
            plan.profile.starting_point,
        )
    )

    baseline_distance = float(
        calculate_baseline_route_distance(
            baseline_route
        )
    )

    optimized_distance = float(
        plan.optimized_route_distance_km
    )

    saving_km = (
        baseline_distance
        - optimized_distance
    )

    if baseline_distance > 0:
        saving_pct = (
            saving_km
            / baseline_distance
            * 100.0
        )
    else:
        saving_pct = 0.0

    return {
        "baseline_route_distance_km": round(
            baseline_distance,
            2,
        ),
        "optimized_route_distance_km": round(
            optimized_distance,
            2,
        ),
        "route_distance_saving_km": round(
            saving_km,
            2,
        ),
        "route_distance_saving_pct": round(
            saving_pct,
            2,
        ),
        "optimized_not_worse": bool(
            optimized_distance
            <= baseline_distance
            + 0.01
        ),
    }


def evaluate_trip_plan(
    plan: TripPlan,
    top_n: int = DEFAULT_EVALUATION_TOP_N,
) -> dict:
    """
    Calculate all quantitative evaluation metrics for
    one generated TripPlan.
    """

    diversity = (
        recommendation_diversity(
            plan,
            top_n=top_n,
        )
    )

    weather = (
        itinerary_weather_metrics(
            plan
        )
    )

    route_metrics = (
        route_comparison_metrics(
            plan
        )
    )

    return {
        "mean_preference_score": (
            mean_preference_score(
                plan,
                top_n=top_n,
            )
        ),
        "mean_final_score": (
            mean_final_score(
                plan,
                top_n=top_n,
            )
        ),
        "unique_category_count": (
            diversity[
                "unique_category_count"
            ]
        ),
        "category_diversity_pct": (
            diversity[
                "category_diversity_pct"
            ]
        ),
        "budget_compliant": (
            budget_compliant(
                plan
            )
        ),
        "duration_compliant": (
            itinerary_duration_compliant(
                plan
            )
        ),
        "scheduled_coverage_pct": (
            scheduled_destination_coverage(
                plan
            )
        ),
        "weather_coverage_pct": (
            weather[
                "weather_coverage_pct"
            ]
        ),
        "mean_weather_score": (
            weather[
                "mean_weather_score"
            ]
        ),
        "route_valid": (
            route_valid(
                plan
            )
        ),
        **route_metrics,
    }