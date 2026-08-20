import pandas as pd
import pytest

from src.recommendation.final_scoring import (
    calculate_final_scores,
    calculate_route_efficiency_scores,
    rank_final_destinations,
)
from src.recommendation.traveller_profile import (
    TravellerProfile,
)


def make_destinations() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "destination_id": [
                "T001",
                "T002",
                "T003",
            ],
            "name": [
                "Near Nature",
                "Mid Adventure",
                "Far Nature",
            ],
            "latitude": [
                6.95,
                7.30,
                9.00,
            ],
            "longitude": [
                79.90,
                80.20,
                81.50,
            ],
            "estimated_daily_cost_usd": [
                30.0,
                45.0,
                35.0,
            ],
            "crowd_level": [
                2,
                3,
                5,
            ],
            "beach": [
                0,
                0,
                0,
            ],
            "wildlife": [
                2,
                2,
                3,
            ],
            "hiking": [
                4,
                5,
                3,
            ],
            "nature": [
                5,
                4,
                5,
            ],
            "culture": [
                1,
                1,
                1,
            ],
            "history": [
                0,
                0,
                0,
            ],
            "adventure": [
                4,
                5,
                3,
            ],
            "weather_score": [
                90.0,
                70.0,
                40.0,
            ],
            "weather_available": [
                True,
                True,
                True,
            ],
        }
    )


def make_profile(
    crowd_preference: str = (
        "Prefer Less Crowded Places"
    ),
) -> TravellerProfile:
    return TravellerProfile(
        starting_point="Colombo",
        trip_days=5,
        budget_usd=400,
        travel_style="Balanced",
        crowd_preference=crowd_preference,
        transport="Mixed Transport",
        interests=(
            "Hiking",
            "Nature",
            "Adventure",
        ),
    )


def test_route_efficiency_adds_required_columns() -> None:
    scored = (
        calculate_route_efficiency_scores(
            make_destinations(),
            "Colombo",
        )
    )

    required_columns = {
        "distance_from_start_km",
        "mean_peer_distance_km",
        "route_efficiency_distance_km",
        "route_efficiency_score",
    }

    assert required_columns.issubset(
        scored.columns
    )


def test_route_efficiency_scores_are_bounded() -> None:
    scored = (
        calculate_route_efficiency_scores(
            make_destinations(),
            "Colombo",
        )
    )

    assert (
        scored[
            "route_efficiency_score"
        ]
        .between(
            0,
            100,
        )
        .all()
    )


def test_near_destination_scores_better_than_far_destination() -> None:
    scored = (
        calculate_route_efficiency_scores(
            make_destinations(),
            "Colombo",
        )
        .set_index(
            "name"
        )
    )

    assert (
        scored.loc[
            "Near Nature",
            "route_efficiency_score",
        ]
        > scored.loc[
            "Far Nature",
            "route_efficiency_score",
        ]
    )


def test_single_destination_route_score_is_100() -> None:
    destination = (
        make_destinations()
        .head(1)
    )

    scored = (
        calculate_route_efficiency_scores(
            destination,
            "Colombo",
        )
    )

    assert (
        scored.iloc[0][
            "route_efficiency_score"
        ]
        == 100.0
    )


def test_invalid_latitude_is_rejected() -> None:
    destinations = (
        make_destinations()
    )

    destinations.loc[
        0,
        "latitude",
    ] = 100.0

    with pytest.raises(
        ValueError,
        match="Latitude",
    ):
        calculate_route_efficiency_scores(
            destinations,
            "Colombo",
        )


def test_final_scores_are_between_0_and_100() -> None:
    scored = (
        calculate_final_scores(
            make_destinations(),
            make_profile(),
        )
    )

    assert (
        scored[
            "final_score"
        ]
        .between(
            0,
            100,
        )
        .all()
    )


def test_all_weights_active_with_weather_and_crowd_preference() -> None:
    scored = (
        calculate_final_scores(
            make_destinations(),
            make_profile(),
        )
    )

    assert (
        scored[
            "active_weight_total"
        ]
        == 1.0
    ).all()


def test_no_preference_excludes_crowd_weight() -> None:
    scored = (
        calculate_final_scores(
            make_destinations(),
            make_profile(
                "No Preference"
            ),
        )
    )

    assert (
        scored[
            "crowd_component_active"
        ]
        == False
    ).all()

    assert (
        scored[
            "crowd_weight_used"
        ]
        == 0.0
    ).all()

    assert (
        scored[
            "active_weight_total"
        ]
        == 0.90
    ).all()


def test_no_preference_crowd_level_does_not_change_final_score() -> None:
    destinations = (
        make_destinations()
        .head(1)
        .copy()
    )

    profile = make_profile(
        "No Preference"
    )

    low_crowd = (
        destinations.copy()
    )

    high_crowd = (
        destinations.copy()
    )

    low_crowd[
        "crowd_level"
    ] = 1

    high_crowd[
        "crowd_level"
    ] = 5

    low_score = float(
        calculate_final_scores(
            low_crowd,
            profile,
        ).iloc[0][
            "final_score"
        ]
    )

    high_score = float(
        calculate_final_scores(
            high_crowd,
            profile,
        ).iloc[0][
            "final_score"
        ]
    )

    assert (
        low_score
        == high_score
    )


def test_crowd_preference_affects_score_when_active() -> None:
    destinations = (
        make_destinations()
        .head(1)
        .copy()
    )

    less_crowded = (
        destinations.copy()
    )

    popular = (
        destinations.copy()
    )

    less_crowded[
        "crowd_level"
    ] = 1

    popular[
        "crowd_level"
    ] = 5

    profile = make_profile()

    less_crowded_score = float(
        calculate_final_scores(
            less_crowded,
            profile,
        ).iloc[0][
            "final_score"
        ]
    )

    popular_score = float(
        calculate_final_scores(
            popular,
            profile,
        ).iloc[0][
            "final_score"
        ]
    )

    assert (
        less_crowded_score
        > popular_score
    )


def test_missing_weather_excludes_weather_weight() -> None:
    destinations = (
        make_destinations()
    )

    destinations.loc[
        0,
        "weather_available",
    ] = False

    destinations.loc[
        0,
        "weather_score",
    ] = None

    scored = (
        calculate_final_scores(
            destinations,
            make_profile(),
        )
    )

    assert (
        scored.iloc[0][
            "weather_component_active"
        ]
        == False
    )

    assert (
        scored.iloc[0][
            "weather_weight_used"
        ]
        == 0.0
    )

    assert (
        scored.iloc[0][
            "active_weight_total"
        ]
        == pytest.approx(
            0.85
        )
    )


def test_better_weather_improves_otherwise_equal_score() -> None:
    destinations = (
        make_destinations()
        .head(2)
        .copy()
    )

    for column in [
        "latitude",
        "longitude",
        "estimated_daily_cost_usd",
        "crowd_level",
        "beach",
        "wildlife",
        "hiking",
        "nature",
        "culture",
        "history",
        "adventure",
    ]:
        destinations.loc[
            1,
            column,
        ] = destinations.loc[
            0,
            column,
        ]

    destinations.loc[
        0,
        "weather_score",
    ] = 95.0

    destinations.loc[
        1,
        "weather_score",
    ] = 35.0

    scored = (
        calculate_final_scores(
            destinations,
            make_profile(),
        )
    )

    assert (
        scored.iloc[0][
            "final_score"
        ]
        > scored.iloc[1][
            "final_score"
        ]
    )


def test_invalid_weather_score_is_rejected() -> None:
    destinations = (
        make_destinations()
    )

    destinations.loc[
        0,
        "weather_score",
    ] = 120.0

    with pytest.raises(
        ValueError,
        match="between 0 and 100",
    ):
        calculate_final_scores(
            destinations,
            make_profile(),
        )


def test_available_weather_requires_score() -> None:
    destinations = (
        make_destinations()
    )

    destinations.loc[
        0,
        "weather_score",
    ] = None

    destinations.loc[
        0,
        "weather_available",
    ] = True

    with pytest.raises(
        ValueError,
        match="must include a weather score",
    ):
        calculate_final_scores(
            destinations,
            make_profile(),
        )


def test_rank_final_destinations_sorts_final_score() -> None:
    ranked = (
        rank_final_destinations(
            make_destinations(),
            make_profile(),
        )
    )

    scores = (
        ranked[
            "final_score"
        ].tolist()
    )

    assert scores == sorted(
        scores,
        reverse=True,
    )


def test_final_rank_is_continuous() -> None:
    ranked = (
        rank_final_destinations(
            make_destinations(),
            make_profile(),
        )
    )

    assert (
        ranked[
            "final_recommendation_rank"
        ].tolist()
        == [
            1,
            2,
            3,
        ]
    )


def test_top_n_limits_final_results() -> None:
    ranked = (
        rank_final_destinations(
            make_destinations(),
            make_profile(),
            top_n=2,
        )
    )

    assert len(
        ranked
    ) == 2


def test_invalid_top_n_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="top_n",
    ):
        rank_final_destinations(
            make_destinations(),
            make_profile(),
            top_n=0,
        )