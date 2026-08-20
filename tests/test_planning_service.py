import pandas as pd
import pytest

from src.planning.service import (
    TripPlan,
    generate_trip_plan,
)
from src.recommendation.traveller_profile import (
    TravellerProfile,
)


def fake_weather_fetcher(
    latitude: float,
    longitude: float,
    forecast_days: int,
) -> pd.DataFrame:
    """
    Deterministic weather provider used instead of
    calling Open-Meteo during automated tests.
    """

    return pd.DataFrame(
        {
            "date": pd.date_range(
                "2026-08-20",
                periods=forecast_days,
                freq="D",
            ),
            "weather_code": [
                1
                for _ in range(
                    forecast_days
                )
            ],
            "temperature_max_c": [
                29.0
                for _ in range(
                    forecast_days
                )
            ],
            "temperature_min_c": [
                23.0
                for _ in range(
                    forecast_days
                )
            ],
            "precipitation_probability_max": [
                10.0
                for _ in range(
                    forecast_days
                )
            ],
            "precipitation_sum_mm": [
                0.5
                for _ in range(
                    forecast_days
                )
            ],
        }
    )


def failing_weather_fetcher(
    latitude: float,
    longitude: float,
    forecast_days: int,
) -> pd.DataFrame:
    raise RuntimeError(
        "Weather unavailable."
    )


@pytest.fixture(
    scope="module",
)
def sample_profile() -> TravellerProfile:
    return TravellerProfile(
        starting_point="Colombo",
        trip_days=6,
        budget_usd=500,
        travel_style="Budget",
        crowd_preference=(
            "Prefer Less Crowded Places"
        ),
        transport="Public Transport",
        interests=(
            "Hiking",
            "Nature",
            "Adventure",
        ),
    )


@pytest.fixture(
    scope="module",
)
def sample_plan(
    sample_profile: TravellerProfile,
) -> TripPlan:
    return generate_trip_plan(
        sample_profile,
        weather_fetcher=(
            fake_weather_fetcher
        ),
    )


@pytest.fixture(
    scope="module",
)
def failed_weather_plan(
    sample_profile: TravellerProfile,
) -> TripPlan:
    return generate_trip_plan(
        sample_profile,
        weather_fetcher=(
            failing_weather_fetcher
        ),
    )


@pytest.fixture(
    scope="module",
)
def no_crowd_preference_plan() -> TripPlan:
    profile = TravellerProfile(
        starting_point="Colombo",
        trip_days=6,
        budget_usd=500,
        travel_style="Budget",
        crowd_preference=(
            "No Preference"
        ),
        transport="Public Transport",
        interests=(
            "Hiking",
            "Nature",
            "Adventure",
        ),
    )

    return generate_trip_plan(
        profile,
        weather_fetcher=(
            fake_weather_fetcher
        ),
    )


def test_generate_trip_plan_returns_trip_plan(
    sample_plan: TripPlan,
) -> None:
    assert isinstance(
        sample_plan,
        TripPlan,
    )


def test_trip_plan_preserves_profile(
    sample_plan: TripPlan,
    sample_profile: TravellerProfile,
) -> None:
    assert (
        sample_plan.profile
        == sample_profile
    )


def test_default_recommendation_count(
    sample_plan: TripPlan,
) -> None:
    assert (
        len(
            sample_plan.recommendations
        )
        == 10
    )


def test_default_route_candidate_count(
    sample_plan: TripPlan,
) -> None:
    assert (
        len(
            sample_plan.optimized_route
        )
        == 7
    )


def test_route_order_is_continuous(
    sample_plan: TripPlan,
) -> None:
    route_orders = (
        sample_plan.optimized_route[
            "route_order"
        ]
        .astype(int)
        .tolist()
    )

    assert route_orders == list(
        range(
            1,
            len(route_orders) + 1,
        )
    )


def test_itinerary_preserves_optimized_route_order(
    sample_plan: TripPlan,
) -> None:
    route_names = (
        sample_plan.optimized_route[
            "name"
        ]
        .tolist()
    )

    itinerary_names = (
        sample_plan.itinerary[
            "name"
        ]
        .tolist()
    )

    assert (
        itinerary_names
        == route_names
    )


def test_itinerary_respects_trip_duration(
    sample_plan: TripPlan,
) -> None:
    scheduled = (
        sample_plan.itinerary[
            sample_plan.itinerary[
                "scheduled"
            ]
        ]
    )

    if not scheduled.empty:
        assert (
            int(
                scheduled[
                    "itinerary_day"
                ].max()
            )
            <= sample_plan.profile.trip_days
        )


def test_itinerary_summary_matches_flags(
    sample_plan: TripPlan,
) -> None:
    itinerary = (
        sample_plan.itinerary
    )

    summary = (
        sample_plan.itinerary_summary
    )

    assert (
        summary[
            "scheduled_destinations"
        ]
        == int(
            itinerary[
                "scheduled"
            ].sum()
        )
    )

    assert (
        summary[
            "unscheduled_destinations"
        ]
        == int(
            (
                ~itinerary[
                    "scheduled"
                ]
            ).sum()
        )
    )


def test_budget_uses_profile_budget(
    sample_plan: TripPlan,
) -> None:
    assert (
        sample_plan.budget[
            "total_budget_usd"
        ]
        == 500.0
    )

    assert (
        sample_plan.budget[
            "estimated_total_cost_usd"
        ]
        >= 0
    )


def test_budget_contains_status(
    sample_plan: TripPlan,
) -> None:
    assert (
        "within_budget"
        in sample_plan.budget
    )

    assert isinstance(
        sample_plan.budget[
            "within_budget"
        ],
        bool,
    )


def test_route_distance_matches_segments(
    sample_plan: TripPlan,
) -> None:
    expected_distance = float(
        sample_plan.optimized_route[
            "distance_from_previous_km"
        ].sum()
    )

    assert (
        sample_plan.optimized_route_distance_km
        == pytest.approx(
            expected_distance,
            abs=0.01,
        )
    )


def test_invalid_recommendation_count_is_rejected(
    sample_profile: TravellerProfile,
) -> None:
    with pytest.raises(
        ValueError,
        match="Recommendation count",
    ):
        generate_trip_plan(
            sample_profile,
            recommendation_count=0,
            weather_fetcher=(
                fake_weather_fetcher
            ),
        )


def test_invalid_route_candidate_count_is_rejected(
    sample_profile: TravellerProfile,
) -> None:
    with pytest.raises(
        ValueError,
        match="Route candidate count",
    ):
        generate_trip_plan(
            sample_profile,
            route_candidate_count=0,
            weather_fetcher=(
                fake_weather_fetcher
            ),
        )


def test_route_candidates_cannot_exceed_recommendations(
    sample_profile: TravellerProfile,
) -> None:
    with pytest.raises(
        ValueError,
        match="cannot exceed",
    ):
        generate_trip_plan(
            sample_profile,
            recommendation_count=5,
            route_candidate_count=6,
            weather_fetcher=(
                fake_weather_fetcher
            ),
        )


def test_integrated_recommendations_have_final_scores(
    sample_plan: TripPlan,
) -> None:
    required_columns = {
        "final_score",
        "final_recommendation_rank",
        "preference_score",
        "budget_score",
        "route_efficiency_score",
        "ranking_weather_score",
    }

    assert required_columns.issubset(
        sample_plan.recommendations.columns
    )


def test_final_recommendation_rank_is_continuous(
    sample_plan: TripPlan,
) -> None:
    ranks = (
        sample_plan.recommendations[
            "final_recommendation_rank"
        ]
        .astype(int)
        .tolist()
    )

    assert ranks == list(
        range(
            1,
            len(ranks) + 1,
        )
    )


def test_candidate_weather_is_available(
    sample_plan: TripPlan,
) -> None:
    assert (
        sample_plan.recommendations[
            "weather_available"
        ]
        .all()
    )

    assert (
        sample_plan.recommendations[
            "ranking_weather_score"
        ]
        .between(
            0,
            100,
        )
        .all()
    )


def test_weather_forecasts_are_reused(
    sample_plan: TripPlan,
) -> None:
    assert (
        len(
            sample_plan.weather_forecasts
        )
        == 10
    )

    assert (
        sample_plan.weather_failure_count
        == 0
    )


def test_scheduled_itinerary_has_day_weather(
    sample_plan: TripPlan,
) -> None:
    scheduled = (
        sample_plan.itinerary[
            sample_plan.itinerary[
                "scheduled"
            ]
        ]
    )

    assert (
        scheduled[
            "weather_available"
        ].all()
    )

    assert (
        scheduled[
            "weather_score"
        ]
        .between(
            0,
            100,
        )
        .all()
    )


def test_weather_failure_does_not_break_planner(
    failed_weather_plan: TripPlan,
) -> None:
    assert (
        len(
            failed_weather_plan.recommendations
        )
        == 10
    )

    assert (
        failed_weather_plan.weather_failure_count
        == 10
    )

    assert (
        len(
            failed_weather_plan.weather_forecasts
        )
        == 0
    )


def test_weather_failure_excludes_weather_weight(
    failed_weather_plan: TripPlan,
) -> None:
    assert (
        failed_weather_plan.recommendations[
            "weather_component_active"
        ]
        .eq(False)
        .all()
    )

    assert (
        failed_weather_plan.recommendations[
            "active_weight_total"
        ]
        .eq(0.85)
        .all()
    )


def test_no_preference_excludes_crowd_in_integrated_plan(
    no_crowd_preference_plan: TripPlan,
) -> None:
    recommendations = (
        no_crowd_preference_plan.recommendations
    )

    assert (
        recommendations[
            "crowd_component_active"
        ]
        .eq(False)
        .all()
    )

    assert (
        recommendations[
            "crowd_weight_used"
        ]
        .eq(0.0)
        .all()
    )

    assert (
        recommendations[
            "active_weight_total"
        ]
        .eq(0.90)
        .all()
    )