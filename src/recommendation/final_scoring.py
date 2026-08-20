from __future__ import annotations

import pandas as pd

from src.optimization.distance import (
    haversine_distance,
)
from src.optimization.route_baseline import (
    get_starting_coordinates,
)
from src.recommendation.recommender import (
    calculate_budget_scores,
    calculate_crowd_scores,
    calculate_preference_similarity,
)
from src.recommendation.traveller_profile import (
    TravellerProfile,
)


PREFERENCE_WEIGHT = 0.45
BUDGET_WEIGHT = 0.20
WEATHER_WEIGHT = 0.15
CROWD_WEIGHT = 0.10
ROUTE_EFFICIENCY_WEIGHT = 0.10

FINAL_WEIGHT_TOTAL = (
    PREFERENCE_WEIGHT
    + BUDGET_WEIGHT
    + WEATHER_WEIGHT
    + CROWD_WEIGHT
    + ROUTE_EFFICIENCY_WEIGHT
)

ROUTE_START_DISTANCE_WEIGHT = 0.50
ROUTE_CLUSTER_DISTANCE_WEIGHT = 0.50


def _validate_coordinates(
    latitude: float,
    longitude: float,
) -> None:
    """
    Validate geographic coordinates used by the
    route-efficiency scoring model.
    """

    if not -90 <= latitude <= 90:
        raise ValueError(
            "Latitude must be between -90 and 90."
        )

    if not -180 <= longitude <= 180:
        raise ValueError(
            "Longitude must be between -180 and 180."
        )


def _validate_route_columns(
    destinations: pd.DataFrame,
) -> None:
    """
    Validate destination fields required for
    geographic efficiency scoring.
    """

    required_columns = {
        "name",
        "latitude",
        "longitude",
    }

    missing_columns = (
        required_columns
        - set(destinations.columns)
    )

    if missing_columns:
        raise ValueError(
            "Destination data is missing route-efficiency "
            "columns: "
            + ", ".join(
                sorted(missing_columns)
            )
        )

    if destinations.empty:
        raise ValueError(
            "Cannot score an empty destination set."
        )

    if destinations[
        [
            "latitude",
            "longitude",
        ]
    ].isna().any().any():
        raise ValueError(
            "Destination coordinates cannot be missing."
        )

    for _, destination in (
        destinations.iterrows()
    ):
        _validate_coordinates(
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
        )


def calculate_route_efficiency_scores(
    destinations: pd.DataFrame,
    starting_point: str,
) -> pd.DataFrame:
    """
    Calculate a pre-route geographic efficiency proxy.

    The score considers:

    1. Distance from the traveller's starting point.
    2. Mean geographic distance from the destination
       to the other candidates.

    Lower combined distance receives a higher score.

    This is a candidate-selection proxy only. It does
    not represent road distance or the final OR-Tools
    optimized route.
    """

    _validate_route_columns(
        destinations
    )

    results = (
        destinations
        .copy()
        .reset_index(
            drop=True
        )
    )

    start_latitude, start_longitude = (
        get_starting_coordinates(
            starting_point
        )
    )

    start_latitude = float(
        start_latitude
    )

    start_longitude = float(
        start_longitude
    )

    _validate_coordinates(
        start_latitude,
        start_longitude,
    )

    coordinates = [
        (
            float(row["latitude"]),
            float(row["longitude"]),
        )
        for _, row in results.iterrows()
    ]

    start_distances: list[float] = []
    peer_distances: list[float] = []

    for index, (
        latitude,
        longitude,
    ) in enumerate(
        coordinates
    ):
        start_distance = (
            haversine_distance(
                start_latitude,
                start_longitude,
                latitude,
                longitude,
            )
        )

        start_distances.append(
            float(
                start_distance
            )
        )

        distances_to_peers: list[
            float
        ] = []

        for peer_index, (
            peer_latitude,
            peer_longitude,
        ) in enumerate(
            coordinates
        ):
            if (
                peer_index
                == index
            ):
                continue

            peer_distance = (
                haversine_distance(
                    latitude,
                    longitude,
                    peer_latitude,
                    peer_longitude,
                )
            )

            distances_to_peers.append(
                float(
                    peer_distance
                )
            )

        if distances_to_peers:
            mean_peer_distance = (
                sum(
                    distances_to_peers
                )
                / len(
                    distances_to_peers
                )
            )
        else:
            mean_peer_distance = 0.0

        peer_distances.append(
            mean_peer_distance
        )

    results[
        "distance_from_start_km"
    ] = [
        round(
            distance,
            2,
        )
        for distance in start_distances
    ]

    results[
        "mean_peer_distance_km"
    ] = [
        round(
            distance,
            2,
        )
        for distance in peer_distances
    ]

    route_proxy = (
        pd.Series(
            start_distances,
            index=results.index,
            dtype=float,
        )
        * ROUTE_START_DISTANCE_WEIGHT
        + pd.Series(
            peer_distances,
            index=results.index,
            dtype=float,
        )
        * ROUTE_CLUSTER_DISTANCE_WEIGHT
    )

    results[
        "route_efficiency_distance_km"
    ] = (
        route_proxy.round(
            2
        )
    )

    minimum_proxy = float(
        route_proxy.min()
    )

    maximum_proxy = float(
        route_proxy.max()
    )

    if (
        len(results) == 1
        or abs(
            maximum_proxy
            - minimum_proxy
        )
        < 1e-9
    ):
        route_scores = pd.Series(
            100.0,
            index=results.index,
        )

    else:
        route_scores = (
            (
                maximum_proxy
                - route_proxy
            )
            / (
                maximum_proxy
                - minimum_proxy
            )
            * 100.0
        )

    results[
        "route_efficiency_score"
    ] = (
        route_scores
        .clip(
            lower=0.0,
            upper=100.0,
        )
        .round(2)
    )

    return results


def _prepare_weather_component(
    destinations: pd.DataFrame,
) -> pd.DataFrame:
    """
    Validate optional weather information.

    When weather data is unavailable, its weight is
    excluded rather than replacing it with invented
    forecast values.
    """

    results = (
        destinations.copy()
    )

    if (
        "weather_score"
        not in results.columns
    ):
        results[
            "weather_score"
        ] = float("nan")

    results[
        "weather_score"
    ] = pd.to_numeric(
        results[
            "weather_score"
        ],
        errors="coerce",
    )

    non_missing_weather = (
        results[
            "weather_score"
        ].notna()
    )

    invalid_weather = (
        non_missing_weather
        & (
            (
                results[
                    "weather_score"
                ]
                < 0
            )
            | (
                results[
                    "weather_score"
                ]
                > 100
            )
        )
    )

    if invalid_weather.any():
        raise ValueError(
            "Weather scores must be between "
            "0 and 100."
        )

    if (
        "weather_available"
        in results.columns
    ):
        weather_available = (
            results[
                "weather_available"
            ]
        )

        valid_boolean_values = (
            weather_available
            .dropna()
            .isin(
                [
                    True,
                    False,
                ]
            )
            .all()
        )

        if not valid_boolean_values:
            raise ValueError(
                "weather_available must contain "
                "boolean values."
            )

        weather_available = (
            weather_available
            .fillna(False)
            .astype(bool)
        )

        inconsistent_weather = (
            weather_available
            & ~non_missing_weather
        )

        if inconsistent_weather.any():
            raise ValueError(
                "Weather marked as available must "
                "include a weather score."
            )

    else:
        weather_available = (
            non_missing_weather
        )

    results[
        "weather_available"
    ] = weather_available

    results[
        "weather_component_active"
    ] = (
        weather_available
        & non_missing_weather
    )

    return results


def calculate_final_scores(
    destinations: pd.DataFrame,
    profile: TravellerProfile,
) -> pd.DataFrame:
    """
    Calculate the final CeylonCompass destination
    recommendation score.

    Standard weights:

        45% preference similarity
        20% budget compatibility
        15% weather suitability
        10% crowd compatibility
        10% route-efficiency proxy

    If the traveller selects No Preference for crowd,
    the crowd component is excluded.

    If live weather is unavailable for a destination,
    the weather component is excluded for that row.

    The remaining active weights are normalized so
    every final score remains on a 0-100 scale.
    """

    if not isinstance(
        profile,
        TravellerProfile,
    ):
        raise TypeError(
            "profile must be a TravellerProfile."
        )

    results = (
        calculate_preference_similarity(
            destinations,
            profile,
        )
    )

    results = (
        calculate_budget_scores(
            results,
            profile,
        )
    )

    results = (
        calculate_crowd_scores(
            results,
            profile,
        )
    )

    results = (
        calculate_route_efficiency_scores(
            results,
            profile.starting_point,
        )
    )

    results = (
        _prepare_weather_component(
            results
        )
    )

    weighted_score = (
        results[
            "preference_score"
        ]
        * PREFERENCE_WEIGHT
        + results[
            "budget_score"
        ]
        * BUDGET_WEIGHT
        + results[
            "route_efficiency_score"
        ]
        * ROUTE_EFFICIENCY_WEIGHT
    )

    active_weight_total = pd.Series(
        (
            PREFERENCE_WEIGHT
            + BUDGET_WEIGHT
            + ROUTE_EFFICIENCY_WEIGHT
        ),
        index=results.index,
        dtype=float,
    )

    crowd_component_active = (
        profile.crowd_preference
        != "No Preference"
    )

    results[
        "crowd_component_active"
    ] = crowd_component_active

    if crowd_component_active:
        weighted_score = (
            weighted_score
            + results[
                "crowd_score"
            ]
            * CROWD_WEIGHT
        )

        active_weight_total = (
            active_weight_total
            + CROWD_WEIGHT
        )

    weather_active = (
        results[
            "weather_component_active"
        ]
    )

    weighted_score = (
        weighted_score
        + results[
            "weather_score"
        ]
        .fillna(0.0)
        * WEATHER_WEIGHT
        * weather_active.astype(float)
    )

    active_weight_total = (
        active_weight_total
        + WEATHER_WEIGHT
        * weather_active.astype(float)
    )

    results[
        "active_weight_total"
    ] = (
        active_weight_total.round(
            2
        )
    )

    results[
        "preference_weight_used"
    ] = PREFERENCE_WEIGHT

    results[
        "budget_weight_used"
    ] = BUDGET_WEIGHT

    results[
        "route_efficiency_weight_used"
    ] = ROUTE_EFFICIENCY_WEIGHT

    results[
        "crowd_weight_used"
    ] = (
        CROWD_WEIGHT
        if crowd_component_active
        else 0.0
    )

    results[
        "weather_weight_used"
    ] = (
        weather_active.astype(float)
        * WEATHER_WEIGHT
    )

    results[
        "final_score"
    ] = (
        weighted_score
        / active_weight_total
    ).round(2)

    return results


def rank_final_destinations(
    destinations: pd.DataFrame,
    profile: TravellerProfile,
    top_n: int | None = None,
) -> pd.DataFrame:
    """
    Rank candidate destinations using the final
    weighted CeylonCompass scoring model.
    """

    if (
        top_n is not None
        and top_n < 1
    ):
        raise ValueError(
            "top_n must be at least 1."
        )

    scored = (
        calculate_final_scores(
            destinations,
            profile,
        )
    )

    ranked = (
        scored
        .sort_values(
            by=[
                "final_score",
                "preference_score",
                "route_efficiency_score",
                "name",
            ],
            ascending=[
                False,
                False,
                False,
                True,
            ],
        )
        .reset_index(
            drop=True
        )
    )

    ranked[
        "final_recommendation_rank"
    ] = (
        ranked.index
        + 1
    )

    if top_n is not None:
        ranked = (
            ranked
            .head(
                top_n
            )
            .copy()
        )

    return ranked