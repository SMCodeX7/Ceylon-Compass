from __future__ import annotations

from collections.abc import Callable
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
from src.recommendation.final_scoring import (
    rank_final_destinations,
)
from src.recommendation.recommender import (
    DATA_PATH,
    rank_destinations,
)
from src.recommendation.traveller_profile import (
    TravellerProfile,
)
from src.weather.client import (
    fetch_weather_forecast,
)
from src.weather.scoring import (
    score_weather_forecast,
    weather_forecast_summary,
    weather_suitability_label,
)


DEFAULT_RECOMMENDATION_COUNT = 10
DEFAULT_ROUTE_CANDIDATE_COUNT = 7
MAX_WEATHER_FORECAST_DAYS = 16

WeatherFetcher = Callable[
    [float, float, int],
    pd.DataFrame,
]


@dataclass
class TripPlan:
    """
    Complete result produced by the CeylonCompass
    planning pipeline.
    """

    profile: TravellerProfile

    recommendations: pd.DataFrame

    optimized_route: pd.DataFrame

    itinerary: pd.DataFrame

    itinerary_summary: dict

    budget: dict

    optimized_route_distance_km: float

    weather_forecasts: dict[
        str,
        pd.DataFrame,
    ]

    weather_failure_count: int


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


def _destination_weather_key(
    destination: pd.Series,
) -> str:
    """
    Return a stable key used for cached weather
    forecasts.
    """

    if (
        "destination_id"
        in destination.index
    ):
        return str(
            destination[
                "destination_id"
            ]
        )

    return str(
        destination[
            "name"
        ]
    )


def _weather_forecast_days(
    profile: TravellerProfile,
) -> int:
    """
    Limit weather requests to the Open-Meteo
    forecast horizon used by CeylonCompass.
    """

    return min(
        max(
            int(
                profile.trip_days
            ),
            1,
        ),
        MAX_WEATHER_FORECAST_DAYS,
    )


def _attach_candidate_weather(
    destinations: pd.DataFrame,
    profile: TravellerProfile,
    weather_fetcher: WeatherFetcher,
) -> tuple[
    pd.DataFrame,
    dict[str, pd.DataFrame],
]:
    """
    Attach average forecast suitability to candidate
    destinations before final ranking.

    Forecasts are also retained so the itinerary can
    reuse them after route optimization.
    """

    weather_candidates = (
        destinations.copy()
    )

    weather_candidates[
        "weather_available"
    ] = False

    weather_candidates[
        "weather_score"
    ] = float("nan")

    weather_candidates[
        "weather_suitability"
    ] = None

    weather_candidates[
        "weather_forecast_days"
    ] = 0

    forecast_days = (
        _weather_forecast_days(
            profile
        )
    )

    forecast_cache: dict[
        str,
        pd.DataFrame,
    ] = {}

    for index, destination in (
        weather_candidates.iterrows()
    ):
        key = (
            _destination_weather_key(
                destination
            )
        )

        try:
            forecast = (
                weather_fetcher(
                    float(
                        destination[
                            "latitude"
                        ]
                    ),
                    float(
                        destination[
                            "longitude"
                        ]
                    ),
                    forecast_days,
                )
            )

            scored_forecast = (
                score_weather_forecast(
                    forecast
                )
            )

            if scored_forecast.empty:
                continue

            summary = (
                weather_forecast_summary(
                    scored_forecast
                )
            )

            average_score = float(
                summary[
                    "average_weather_score"
                ]
            )

            weather_candidates.at[
                index,
                "weather_available",
            ] = True

            weather_candidates.at[
                index,
                "weather_score",
            ] = average_score

            weather_candidates.at[
                index,
                "weather_suitability",
            ] = (
                weather_suitability_label(
                    average_score
                )
            )

            weather_candidates.at[
                index,
                "weather_forecast_days",
            ] = len(
                scored_forecast
            )

            forecast_cache[
                key
            ] = scored_forecast

        except (
            RuntimeError,
            ValueError,
        ):
            continue

    return (
        weather_candidates,
        forecast_cache,
    )


def _attach_itinerary_weather(
    itinerary: pd.DataFrame,
    forecast_cache: dict[
        str,
        pd.DataFrame,
    ],
) -> pd.DataFrame:
    """
    Attach the forecast corresponding to each
    scheduled itinerary day.

    Candidate ranking uses average forecast
    suitability.

    The itinerary uses the specific forecast row for
    the day on which the destination is scheduled.
    """

    weather_itinerary = (
        itinerary.copy()
    )

    weather_itinerary[
        "weather_available"
    ] = False

    weather_itinerary[
        "weather_date"
    ] = None

    weather_itinerary[
        "weather_description"
    ] = None

    weather_itinerary[
        "weather_temperature_max_c"
    ] = float("nan")

    weather_itinerary[
        "weather_temperature_min_c"
    ] = float("nan")

    weather_itinerary[
        "weather_rain_probability"
    ] = float("nan")

    weather_itinerary[
        "weather_precipitation_mm"
    ] = float("nan")

    weather_itinerary[
        "weather_score"
    ] = float("nan")

    weather_itinerary[
        "weather_suitability"
    ] = None

    for index, destination in (
        weather_itinerary[
            weather_itinerary[
                "scheduled"
            ]
        ].iterrows()
    ):
        key = (
            _destination_weather_key(
                destination
            )
        )

        forecast = (
            forecast_cache.get(
                key
            )
        )

        if (
            forecast is None
            or forecast.empty
        ):
            continue

        day_number = int(
            destination[
                "itinerary_day"
            ]
        )

        forecast_index = (
            day_number - 1
        )

        if (
            forecast_index < 0
            or forecast_index
            >= len(forecast)
        ):
            continue

        weather = (
            forecast.iloc[
                forecast_index
            ]
        )

        weather_itinerary.at[
            index,
            "weather_available",
        ] = True

        weather_date = (
            weather[
                "date"
            ]
        )

        if hasattr(
            weather_date,
            "strftime",
        ):
            weather_date = (
                weather_date.strftime(
                    "%Y-%m-%d"
                )
            )
        else:
            weather_date = str(
                weather_date
            )

        weather_itinerary.at[
            index,
            "weather_date",
        ] = weather_date

        weather_itinerary.at[
            index,
            "weather_description",
        ] = weather[
            "weather_description"
        ]

        weather_itinerary.at[
            index,
            "weather_temperature_max_c",
        ] = float(
            weather[
                "temperature_max_c"
            ]
        )

        weather_itinerary.at[
            index,
            "weather_temperature_min_c",
        ] = float(
            weather[
                "temperature_min_c"
            ]
        )

        weather_itinerary.at[
            index,
            "weather_rain_probability",
        ] = float(
            weather[
                "precipitation_probability_max"
            ]
        )

        weather_itinerary.at[
            index,
            "weather_precipitation_mm",
        ] = float(
            weather[
                "precipitation_sum_mm"
            ]
        )

        weather_itinerary.at[
            index,
            "weather_score",
        ] = float(
            weather[
                "weather_score"
            ]
        )

        weather_itinerary.at[
            index,
            "weather_suitability",
        ] = weather[
            "weather_suitability"
        ]

    return weather_itinerary


def generate_trip_plan(
    profile: TravellerProfile,
    recommendation_count: int = (
        DEFAULT_RECOMMENDATION_COUNT
    ),
    route_candidate_count: int = (
        DEFAULT_ROUTE_CANDIDATE_COUNT
    ),
    data_path: Path = DATA_PATH,
    weather_fetcher: WeatherFetcher = (
        fetch_weather_forecast
    ),
) -> TripPlan:
    """
    Run the integrated CeylonCompass planning
    pipeline.

    Pipeline:

    1. Preselect destinations using preference,
       budget, and crowd compatibility.
    2. Retrieve live weather for the candidate pool.
    3. Apply the final weighted recommendation model.
    4. Select the strongest route candidates.
    5. Optimize their visit sequence with OR-Tools.
    6. Allocate destinations across available days.
    7. Reuse cached forecasts for itinerary-day
       weather.
    8. Estimate trip spending.
    9. Return one structured TripPlan object.

    The weather component degrades gracefully when
    forecast retrieval fails.
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

    base_recommendations = (
        rank_destinations(
            profile=profile,
            top_n=recommendation_count,
            data_path=data_path,
        )
    )

    if base_recommendations.empty:
        raise RuntimeError(
            "No destination recommendations "
            "were generated."
        )

    (
        weather_candidates,
        forecast_cache,
    ) = _attach_candidate_weather(
        base_recommendations,
        profile,
        weather_fetcher,
    )

    recommendations = (
        rank_final_destinations(
            weather_candidates,
            profile,
            top_n=recommendation_count,
        )
    )

    recommendations[
        "recommendation_rank"
    ] = recommendations[
        "final_recommendation_rank"
    ]

    recommendations[
        "ranking_weather_score"
    ] = recommendations[
        "weather_score"
    ]

    recommendations[
        "ranking_weather_suitability"
    ] = recommendations[
        "weather_suitability"
    ]

    route_candidates = (
        recommendations
        .head(
            route_candidate_count
        )
        .copy()
    )

    # Maintain compatibility with map/explanation
    # components that previously displayed
    # current_stage_score.
    route_candidates[
        "current_stage_score"
    ] = route_candidates[
        "final_score"
    ]

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

    itinerary = (
        _attach_itinerary_weather(
            itinerary,
            forecast_cache,
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

    weather_failure_count = (
        len(
            base_recommendations
        )
        - len(
            forecast_cache
        )
    )

    return TripPlan(
        profile=profile,
        recommendations=recommendations,
        optimized_route=optimized_route,
        itinerary=itinerary,
        itinerary_summary=summary,
        budget=budget,
        optimized_route_distance_km=round(
            float(
                optimized_route_distance
            ),
            2,
        ),
        weather_forecasts=forecast_cache,
        weather_failure_count=(
            weather_failure_count
        ),
    )