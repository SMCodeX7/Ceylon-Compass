from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.budget.estimator import (
    estimate_trip_budget,
)
from src.itinerary.planner import (
    generate_itinerary,
    itinerary_summary,
)
from src.optimization.route_optimizer import (
    calculate_optimized_route_distance,
    optimize_route,
)
from src.recommendation.recommender import (
    DATA_PATH,
    rank_destinations,
)
from src.recommendation.traveller_profile import (
    TravellerProfile,
)


DEFAULT_RECOMMENDATION_COUNT = 10
DEFAULT_ROUTE_CANDIDATE_COUNT = 7


@dataclass
class TripPlan:
    """
    Complete result produced by the CeylonCompass
    planning pipeline.

    Each field keeps the output from an individual
    planning stage available for the UI, evaluation,
    and later system integration.
    """

    profile: TravellerProfile

    recommendations: pd.DataFrame

    optimized_route: pd.DataFrame

    itinerary: pd.DataFrame

    itinerary_summary: dict

    budget: dict

    optimized_route_distance_km: float


def _validate_pipeline_counts(
    recommendation_count: int,
    route_candidate_count: int,
) -> None:
    """
    Validate recommendation and route-candidate
    limits before running the planning pipeline.
    """

    if recommendation_count < 1:
        raise ValueError(
            "Recommendation count must be at least 1."
        )

    if route_candidate_count < 1:
        raise ValueError(
            "Route candidate count must be at least 1."
        )

    if (
        route_candidate_count
        > recommendation_count
    ):
        raise ValueError(
            "Route candidate count cannot exceed "
            "recommendation count."
        )


def generate_trip_plan(
    profile: TravellerProfile,
    recommendation_count: int = (
        DEFAULT_RECOMMENDATION_COUNT
    ),
    route_candidate_count: int = (
        DEFAULT_ROUTE_CANDIDATE_COUNT
    ),
    data_path: Path = DATA_PATH,
) -> TripPlan:
    """
    Run the current CeylonCompass planning pipeline.

    Pipeline stages:

    1. Rank destinations from traveller preferences.
    2. Select the strongest route candidates.
    3. Optimize their visit sequence using OR-Tools.
    4. Allocate destinations across available days.
    5. Estimate trip spending.
    6. Return one structured TripPlan object.

    Weather-aware final recommendation scoring is
    intentionally added in the next integration stage.
    """

    if not isinstance(
        profile,
        TravellerProfile,
    ):
        raise TypeError(
            "profile must be a TravellerProfile."
        )

    _validate_pipeline_counts(
        recommendation_count,
        route_candidate_count,
    )

    recommendations = (
        rank_destinations(
            profile=profile,
            top_n=recommendation_count,
            data_path=data_path,
        )
    )

    if recommendations.empty:
        raise RuntimeError(
            "No destination recommendations "
            "were generated."
        )

    route_candidates = (
        recommendations
        .head(
            route_candidate_count
        )
        .copy()
    )

    optimized_route = (
        optimize_route(
            route_candidates,
            profile.starting_point,
        )
    )

    optimized_route_distance = (
        calculate_optimized_route_distance(
            optimized_route
        )
    )

    itinerary = (
        generate_itinerary(
            optimized_route,
            profile.trip_days,
        )
    )

    summary = (
        itinerary_summary(
            itinerary
        )
    )

    budget = (
        estimate_trip_budget(
            itinerary=itinerary,
            total_budget_usd=profile.budget_usd,
            travel_style=profile.travel_style,
            transport=profile.transport,
        )
    )

    return TripPlan(
        profile=profile,
        recommendations=(
            recommendations
        ),
        optimized_route=(
            optimized_route
        ),
        itinerary=(
            itinerary
        ),
        itinerary_summary=(
            summary
        ),
        budget=budget,
        optimized_route_distance_km=round(
            float(
                optimized_route_distance
            ),
            2,
        ),
    )