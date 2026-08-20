from pathlib import Path

import pandas as pd
import pytest

from src.recommendation.recommender import (
    calculate_budget_scores,
    calculate_crowd_scores,
    calculate_current_stage_scores,
    calculate_preference_similarity,
    rank_destinations,
)
from src.recommendation.traveller_profile import TravellerProfile


DATA_PATH = Path("data/destinations.csv")


def make_profile(**overrides) -> TravellerProfile:
    data = {
        "starting_point": "Colombo",
        "trip_days": 6,
        "budget_usd": 500,
        "travel_style": "Budget",
        "crowd_preference": "Prefer Less Crowded Places",
        "transport": "Public Transport",
        "interests": (
            "Hiking",
            "Nature",
            "Adventure",
        ),
    }

    data.update(overrides)

    return TravellerProfile(**data)


def test_similarity_is_added_to_dataframe() -> None:
    destinations = pd.read_csv(DATA_PATH)

    result = calculate_preference_similarity(
        destinations,
        make_profile(),
    )

    assert "preference_similarity" in result.columns
    assert "preference_score" in result.columns


def test_similarity_range_is_valid() -> None:
    destinations = pd.read_csv(DATA_PATH)

    result = calculate_preference_similarity(
        destinations,
        make_profile(),
    )

    assert result["preference_similarity"].between(
        0,
        1,
    ).all()

    assert result["preference_score"].between(
        0,
        100,
    ).all()


def test_all_destinations_receive_similarity_scores() -> None:
    destinations = pd.read_csv(DATA_PATH)

    result = calculate_preference_similarity(
        destinations,
        make_profile(),
    )

    assert len(result) == 48


def test_budget_score_for_affordable_destination() -> None:
    destinations = pd.DataFrame(
        {
            "estimated_daily_cost_usd": [30, 60],
        }
    )

    profile = make_profile(
        trip_days=4,
        budget_usd=120,
    )

    result = calculate_budget_scores(
        destinations,
        profile,
    )

    assert result.iloc[0]["budget_score"] == 100
    assert bool(result.iloc[0]["budget_compatible"])


def test_budget_score_penalizes_expensive_destination() -> None:
    destinations = pd.DataFrame(
        {
            "estimated_daily_cost_usd": [30, 60, 120],
        }
    )

    profile = make_profile(
        trip_days=4,
        budget_usd=120,
    )

    result = calculate_budget_scores(
        destinations,
        profile,
    )

    assert result.iloc[0]["budget_score"] == 100
    assert result.iloc[1]["budget_score"] == 50
    assert result.iloc[2]["budget_score"] == 25


def test_expensive_destination_is_not_budget_compatible() -> None:
    destinations = pd.DataFrame(
        {
            "estimated_daily_cost_usd": [60],
        }
    )

    profile = make_profile(
        trip_days=4,
        budget_usd=120,
    )

    result = calculate_budget_scores(
        destinations,
        profile,
    )

    assert not bool(
        result.iloc[0]["budget_compatible"]
    )


def test_less_crowded_preference_scores() -> None:
    destinations = pd.DataFrame(
        {
            "crowd_level": [1, 3, 5],
        }
    )

    profile = make_profile(
        crowd_preference="Prefer Less Crowded Places",
    )

    result = calculate_crowd_scores(
        destinations,
        profile,
    )

    assert result["crowd_score"].tolist() == [
        100.0,
        60.0,
        20.0,
    ]


def test_popular_places_preference_scores() -> None:
    destinations = pd.DataFrame(
        {
            "crowd_level": [1, 3, 5],
        }
    )

    profile = make_profile(
        crowd_preference="Popular Tourist Places",
    )

    result = calculate_crowd_scores(
        destinations,
        profile,
    )

    assert result["crowd_score"].tolist() == [
        20.0,
        60.0,
        100.0,
    ]


def test_no_crowd_preference_gives_full_score() -> None:
    destinations = pd.DataFrame(
        {
            "crowd_level": [1, 2, 3, 4, 5],
        }
    )

    profile = make_profile(
        crowd_preference="No Preference",
    )

    result = calculate_crowd_scores(
        destinations,
        profile,
    )

    assert result["crowd_score"].tolist() == [
        100.0,
        100.0,
        100.0,
        100.0,
        100.0,
    ]


def test_current_stage_scores_are_added() -> None:
    destinations = pd.read_csv(DATA_PATH)

    result = calculate_current_stage_scores(
        destinations,
        make_profile(),
    )

    expected_columns = {
        "preference_score",
        "budget_score",
        "budget_compatible",
        "crowd_score",
        "current_stage_score",
    }

    assert expected_columns.issubset(
        result.columns
    )


def test_current_stage_scores_are_valid() -> None:
    destinations = pd.read_csv(DATA_PATH)

    result = calculate_current_stage_scores(
        destinations,
        make_profile(),
    )

    assert result["current_stage_score"].between(
        0,
        100,
    ).all()


def test_rank_destinations_returns_requested_number() -> None:
    result = rank_destinations(
        make_profile(),
        top_n=10,
    )

    assert len(result) == 10


def test_rank_starts_at_one() -> None:
    result = rank_destinations(
        make_profile(),
        top_n=10,
    )

    assert result.iloc[0]["recommendation_rank"] == 1


def test_ranking_uses_current_stage_score() -> None:
    result = rank_destinations(
        make_profile(),
        top_n=10,
    )

    scores = result[
        "current_stage_score"
    ].tolist()

    assert scores == sorted(
        scores,
        reverse=True,
    )


def test_invalid_top_n_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="top_n must be at least 1",
    ):
        rank_destinations(
            make_profile(),
            top_n=0,
        )


def test_hiking_nature_adventure_profile_is_relevant() -> None:
    result = rank_destinations(
        make_profile(),
        top_n=10,
    )

    combined_score = (
        result["hiking"]
        + result["nature"]
        + result["adventure"]
    )

    assert combined_score.mean() >= 12


def test_beach_profile_returns_beach_relevant_places() -> None:
    result = rank_destinations(
        make_profile(
            interests=("Beach",),
            crowd_preference="No Preference",
        ),
        top_n=10,
    )

    assert result["beach"].mean() >= 4.0


def test_wildlife_profile_returns_wildlife_relevant_places() -> None:
    result = rank_destinations(
        make_profile(
            interests=("Wildlife",),
            crowd_preference="No Preference",
        ),
        top_n=10,
    )

    assert result["wildlife"].mean() >= 4.0


def test_culture_history_profile_is_relevant() -> None:
    result = rank_destinations(
        make_profile(
            interests=(
                "Culture",
                "History",
            ),
            crowd_preference="No Preference",
        ),
        top_n=10,
    )

    combined_score = (
        result["culture"]
        + result["history"]
    )

    assert combined_score.mean() >= 8.0


def test_original_dataframe_is_not_modified() -> None:
    destinations = pd.read_csv(DATA_PATH)

    original_columns = list(
        destinations.columns
    )

    calculate_current_stage_scores(
        destinations,
        make_profile(),
    )

    assert list(
        destinations.columns
    ) == original_columns