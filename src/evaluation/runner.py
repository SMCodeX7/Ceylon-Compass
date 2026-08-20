from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

from src.evaluation.metrics import (
    evaluate_trip_plan,
)
from src.evaluation.scenarios import (
    EvaluationScenario,
    get_evaluation_scenarios,
)
from src.planning.service import (
    generate_trip_plan,
)


CONTROLLED_WEATHER_CODES = (
    0,
    1,
    2,
    3,
    61,
    80,
)

CONTROLLED_PRECIPITATION = (
    0.0,
    0.3,
    1.0,
    2.5,
    5.0,
    8.0,
)


def controlled_weather_fetcher(
    latitude: float,
    longitude: float,
    forecast_days: int,
) -> pd.DataFrame:
    """
    Generate deterministic synthetic forecast data for
    reproducible system evaluation.

    This does not measure Open-Meteo forecast accuracy.
    It provides controlled weather variation so the
    weather-aware ranking logic can be benchmarked
    consistently across repeated experiments.
    """

    latitude = float(
        latitude
    )

    longitude = float(
        longitude
    )

    coordinate_seed = int(
        abs(
            round(
                latitude
                * 1000
            )
            + round(
                longitude
                * 1000
            )
        )
    )

    weather_codes = []
    maximum_temperatures = []
    minimum_temperatures = []
    rain_probabilities = []
    precipitation_amounts = []

    for day_index in range(
        forecast_days
    ):
        weather_codes.append(
            CONTROLLED_WEATHER_CODES[
                (
                    coordinate_seed
                    + day_index
                )
                % len(
                    CONTROLLED_WEATHER_CODES
                )
            ]
        )

        maximum_temperature = float(
            27
            + (
                coordinate_seed
                + day_index
            )
            % 6
        )

        minimum_temperature = (
            maximum_temperature
            - 6.0
        )

        maximum_temperatures.append(
            maximum_temperature
        )

        minimum_temperatures.append(
            minimum_temperature
        )

        rain_probabilities.append(
            float(
                (
                    coordinate_seed
                    + day_index
                    * 17
                )
                % 70
            )
        )

        precipitation_amounts.append(
            CONTROLLED_PRECIPITATION[
                (
                    coordinate_seed
                    + day_index
                )
                % len(
                    CONTROLLED_PRECIPITATION
                )
            ]
        )

    return pd.DataFrame(
        {
            "date": pd.date_range(
                "2026-08-20",
                periods=forecast_days,
                freq="D",
            ),
            "weather_code": (
                weather_codes
            ),
            "temperature_max_c": (
                maximum_temperatures
            ),
            "temperature_min_c": (
                minimum_temperatures
            ),
            "precipitation_probability_max": (
                rain_probabilities
            ),
            "precipitation_sum_mm": (
                precipitation_amounts
            ),
        }
    )


def evaluate_scenario(
    scenario: EvaluationScenario,
) -> dict:
    """
    Generate and quantitatively evaluate one fixed
    traveller scenario.
    """

    plan = generate_trip_plan(
        profile=scenario.profile,
        weather_fetcher=(
            controlled_weather_fetcher
        ),
    )

    metrics = (
        evaluate_trip_plan(
            plan
        )
    )

    return {
        "scenario_id": (
            scenario.scenario_id
        ),
        "segment": (
            scenario.segment
        ),
        "description": (
            scenario.description
        ),
        "starting_point": (
            scenario.profile.starting_point
        ),
        "trip_days": (
            scenario.profile.trip_days
        ),
        "budget_usd": (
            scenario.profile.budget_usd
        ),
        "travel_style": (
            scenario.profile.travel_style
        ),
        "crowd_preference": (
            scenario.profile.crowd_preference
        ),
        "transport": (
            scenario.profile.transport
        ),
        "interest_count": len(
            scenario.profile.interests
        ),
        **metrics,
    }


def run_evaluation(
    scenarios: Iterable[
        EvaluationScenario
    ]
    | None = None,
) -> pd.DataFrame:
    """
    Evaluate a collection of scenarios and return one
    result row per traveller profile.
    """

    if scenarios is None:
        scenarios = (
            get_evaluation_scenarios()
        )

    records = [
        evaluate_scenario(
            scenario
        )
        for scenario in scenarios
    ]

    return pd.DataFrame(
        records
    )


def summarize_evaluation(
    results: pd.DataFrame,
) -> dict:
    """
    Produce overall aggregate metrics from scenario
    evaluation results.
    """

    if results.empty:
        raise ValueError(
            "Cannot summarize empty evaluation results."
        )

    required_columns = {
        "scenario_id",
        "mean_preference_score",
        "mean_final_score",
        "category_diversity_pct",
        "budget_compliant",
        "duration_compliant",
        "scheduled_coverage_pct",
        "weather_coverage_pct",
        "mean_weather_score",
        "route_valid",
        "route_distance_saving_pct",
        "optimized_not_worse",
    }

    missing_columns = (
        required_columns
        - set(
            results.columns
        )
    )

    if missing_columns:
        raise ValueError(
            "Evaluation results are missing columns: "
            + ", ".join(
                sorted(
                    missing_columns
                )
            )
        )

    return {
        "scenario_count": int(
            len(
                results
            )
        ),
        "mean_preference_score": round(
            float(
                results[
                    "mean_preference_score"
                ].mean()
            ),
            2,
        ),
        "mean_final_score": round(
            float(
                results[
                    "mean_final_score"
                ].mean()
            ),
            2,
        ),
        "mean_category_diversity_pct": round(
            float(
                results[
                    "category_diversity_pct"
                ].mean()
            ),
            2,
        ),
        "budget_compliance_rate_pct": round(
            float(
                results[
                    "budget_compliant"
                ]
                .astype(float)
                .mean()
                * 100.0
            ),
            2,
        ),
        "duration_compliance_rate_pct": round(
            float(
                results[
                    "duration_compliant"
                ]
                .astype(float)
                .mean()
                * 100.0
            ),
            2,
        ),
        "mean_scheduled_coverage_pct": round(
            float(
                results[
                    "scheduled_coverage_pct"
                ].mean()
            ),
            2,
        ),
        "mean_weather_coverage_pct": round(
            float(
                results[
                    "weather_coverage_pct"
                ].mean()
            ),
            2,
        ),
        "mean_weather_score": round(
            float(
                results[
                    "mean_weather_score"
                ].dropna()
                .mean()
            ),
            2,
        ),
        "route_validity_rate_pct": round(
            float(
                results[
                    "route_valid"
                ]
                .astype(float)
                .mean()
                * 100.0
            ),
            2,
        ),
        "mean_route_distance_saving_pct": round(
            float(
                results[
                    "route_distance_saving_pct"
                ].mean()
            ),
            2,
        ),
        "optimized_not_worse_rate_pct": round(
            float(
                results[
                    "optimized_not_worse"
                ]
                .astype(float)
                .mean()
                * 100.0
            ),
            2,
        ),
    }


def summarize_by_segment(
    results: pd.DataFrame,
) -> pd.DataFrame:
    """
    Aggregate selected evaluation metrics by traveller
    scenario segment.
    """

    if results.empty:
        raise ValueError(
            "Cannot summarize empty evaluation results."
        )

    if (
        "segment"
        not in results.columns
    ):
        raise ValueError(
            "Evaluation results are missing segment."
        )

    summary = (
        results
        .groupby(
            "segment",
            as_index=False,
        )
        .agg(
            scenario_count=(
                "scenario_id",
                "count",
            ),
            mean_preference_score=(
                "mean_preference_score",
                "mean",
            ),
            mean_final_score=(
                "mean_final_score",
                "mean",
            ),
            budget_compliance_rate=(
                "budget_compliant",
                "mean",
            ),
            scheduled_coverage_pct=(
                "scheduled_coverage_pct",
                "mean",
            ),
            category_diversity_pct=(
                "category_diversity_pct",
                "mean",
            ),
            route_distance_saving_pct=(
                "route_distance_saving_pct",
                "mean",
            ),
        )
    )

    summary[
        "budget_compliance_rate_pct"
    ] = (
        summary[
            "budget_compliance_rate"
        ]
        * 100.0
    )

    summary = summary.drop(
        columns=[
            "budget_compliance_rate",
        ]
    )

    numeric_columns = (
        summary
        .select_dtypes(
            include="number"
        )
        .columns
    )

    summary[
        numeric_columns
    ] = (
        summary[
            numeric_columns
        ].round(2)
    )

    return summary