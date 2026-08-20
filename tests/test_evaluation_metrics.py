import pandas as pd

from src.evaluation.metrics import (
    budget_compliant,
    evaluate_trip_plan,
    itinerary_duration_compliant,
    itinerary_weather_metrics,
    mean_final_score,
    mean_preference_score,
    recommendation_diversity,
    route_comparison_metrics,
    route_valid,
    scheduled_destination_coverage,
)
from src.evaluation.runner import (
    controlled_weather_fetcher,
    run_evaluation,
    summarize_by_segment,
    summarize_evaluation,
)
from src.evaluation.scenarios import (
    get_evaluation_scenarios,
)
from src.planning.service import (
    TripPlan,
)
from src.recommendation.traveller_profile import (
    TravellerProfile,
)


def make_plan() -> TripPlan:
    profile = TravellerProfile(
        starting_point="Colombo",
        trip_days=3,
        budget_usd=400,
        travel_style="Balanced",
        crowd_preference="No Preference",
        transport="Mixed Transport",
        interests=(
            "Nature",
            "Hiking",
        ),
    )

    recommendations = pd.DataFrame(
        {
            "name": [
                "A",
                "B",
                "C",
            ],
            "category": [
                "Nature",
                "Hiking",
                "Nature",
            ],
            "preference_score": [
                90.0,
                80.0,
                70.0,
            ],
            "final_score": [
                88.0,
                78.0,
                68.0,
            ],
        }
    )

    optimized_route = pd.DataFrame(
        {
            "name": [
                "A",
                "B",
                "C",
            ],
            "latitude": [
                6.95,
                7.10,
                7.30,
            ],
            "longitude": [
                79.90,
                80.00,
                80.20,
            ],
            "route_order": [
                1,
                2,
                3,
            ],
            "distance_from_previous_km": [
                5.0,
                20.0,
                30.0,
            ],
        }
    )

    itinerary = (
        optimized_route.copy()
    )

    itinerary[
        "recommended_duration_hours"
    ] = [
        4.0,
        4.0,
        5.0,
    ]

    itinerary[
        "scheduled"
    ] = [
        True,
        True,
        True,
    ]

    itinerary[
        "itinerary_day"
    ] = pd.Series(
        [
            1,
            1,
            2,
        ],
        dtype="Int64",
    )

    itinerary[
        "visit_order_in_day"
    ] = pd.Series(
        [
            1,
            2,
            1,
        ],
        dtype="Int64",
    )

    itinerary[
        "weather_available"
    ] = [
        True,
        True,
        False,
    ]

    itinerary[
        "weather_score"
    ] = [
        80.0,
        70.0,
        float("nan"),
    ]

    return TripPlan(
        profile=profile,
        recommendations=recommendations,
        optimized_route=optimized_route,
        itinerary=itinerary,
        itinerary_summary={
            "scheduled_destinations": 3,
            "unscheduled_destinations": 0,
            "days_used": 2,
            "total_activity_hours": 13.0,
        },
        budget={
            "total_budget_usd": 400.0,
            "estimated_total_cost_usd": 300.0,
            "within_budget": True,
        },
        optimized_route_distance_km=55.0,
        weather_forecasts={},
        weather_failure_count=0,
    )


def make_summary_results() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "scenario_id": [
                "E001",
                "E002",
            ],
            "segment": [
                "Beach",
                "Beach",
            ],
            "mean_preference_score": [
                80.0,
                90.0,
            ],
            "mean_final_score": [
                75.0,
                85.0,
            ],
            "category_diversity_pct": [
                60.0,
                80.0,
            ],
            "budget_compliant": [
                True,
                False,
            ],
            "duration_compliant": [
                True,
                True,
            ],
            "scheduled_coverage_pct": [
                100.0,
                80.0,
            ],
            "weather_coverage_pct": [
                100.0,
                100.0,
            ],
            "mean_weather_score": [
                70.0,
                80.0,
            ],
            "route_valid": [
                True,
                True,
            ],
            "route_distance_saving_pct": [
                10.0,
                20.0,
            ],
            "optimized_not_worse": [
                True,
                True,
            ],
        }
    )


def test_mean_recommendation_scores() -> None:
    plan = make_plan()

    assert (
        mean_preference_score(
            plan
        )
        == 80.0
    )

    assert (
        mean_final_score(
            plan
        )
        == 78.0
    )


def test_recommendation_diversity() -> None:
    result = (
        recommendation_diversity(
            make_plan()
        )
    )

    assert (
        result[
            "unique_category_count"
        ]
        == 2
    )

    assert (
        result[
            "category_diversity_pct"
        ]
        == 66.67
    )


def test_budget_compliance() -> None:
    assert (
        budget_compliant(
            make_plan()
        )
        is True
    )


def test_itinerary_duration_is_compliant() -> None:
    assert (
        itinerary_duration_compliant(
            make_plan()
        )
        is True
    )


def test_itinerary_duration_detects_violation() -> None:
    plan = make_plan()

    plan.itinerary.loc[
        1,
        "recommended_duration_hours",
    ] = 5.0

    assert (
        itinerary_duration_compliant(
            plan
        )
        is False
    )


def test_scheduled_destination_coverage() -> None:
    assert (
        scheduled_destination_coverage(
            make_plan()
        )
        == 100.0
    )


def test_weather_metrics() -> None:
    weather = (
        itinerary_weather_metrics(
            make_plan()
        )
    )

    assert (
        weather[
            "weather_available_count"
        ]
        == 2
    )

    assert (
        weather[
            "weather_coverage_pct"
        ]
        == 66.67
    )

    assert (
        weather[
            "mean_weather_score"
        ]
        == 75.0
    )


def test_route_is_valid() -> None:
    assert (
        route_valid(
            make_plan()
        )
        is True
    )


def test_invalid_route_order_is_detected() -> None:
    plan = make_plan()

    plan.optimized_route.loc[
        1,
        "route_order",
    ] = 1

    assert (
        route_valid(
            plan
        )
        is False
    )


def test_route_comparison_returns_metrics() -> None:
    metrics = (
        route_comparison_metrics(
            make_plan()
        )
    )

    required = {
        "baseline_route_distance_km",
        "optimized_route_distance_km",
        "route_distance_saving_km",
        "route_distance_saving_pct",
        "optimized_not_worse",
    }

    assert required.issubset(
        metrics
    )


def test_evaluate_trip_plan_returns_complete_metrics() -> None:
    metrics = (
        evaluate_trip_plan(
            make_plan()
        )
    )

    assert (
        "mean_preference_score"
        in metrics
    )

    assert (
        "budget_compliant"
        in metrics
    )

    assert (
        "route_valid"
        in metrics
    )

    assert (
        "route_distance_saving_pct"
        in metrics
    )


def test_controlled_weather_is_deterministic() -> None:
    first = (
        controlled_weather_fetcher(
            7.0,
            80.0,
            5,
        )
    )

    second = (
        controlled_weather_fetcher(
            7.0,
            80.0,
            5,
        )
    )

    pd.testing.assert_frame_equal(
        first,
        second,
    )


def test_controlled_weather_respects_forecast_days() -> None:
    weather = (
        controlled_weather_fetcher(
            7.0,
            80.0,
            6,
        )
    )

    assert len(
        weather
    ) == 6


def test_runner_evaluates_real_scenario() -> None:
    scenario = (
        get_evaluation_scenarios()[
            0
        ]
    )

    results = (
        run_evaluation(
            scenarios=(
                scenario,
            )
        )
    )

    assert len(
        results
    ) == 1

    assert (
        results.iloc[0][
            "scenario_id"
        ]
        == "E001"
    )

    assert (
        results.iloc[0][
            "route_valid"
        ]
        == True
    )


def test_evaluation_summary() -> None:
    summary = (
        summarize_evaluation(
            make_summary_results()
        )
    )

    assert (
        summary[
            "scenario_count"
        ]
        == 2
    )

    assert (
        summary[
            "mean_preference_score"
        ]
        == 85.0
    )

    assert (
        summary[
            "budget_compliance_rate_pct"
        ]
        == 50.0
    )

    assert (
        summary[
            "mean_route_distance_saving_pct"
        ]
        == 15.0
    )


def test_segment_summary() -> None:
    summary = (
        summarize_by_segment(
            make_summary_results()
        )
    )

    assert len(
        summary
    ) == 1

    assert (
        summary.iloc[0][
            "segment"
        ]
        == "Beach"
    )

    assert (
        summary.iloc[0][
            "scenario_count"
        ]
        == 2
    )

    assert (
        summary.iloc[0][
            "budget_compliance_rate_pct"
        ]
        == 50.0
    )