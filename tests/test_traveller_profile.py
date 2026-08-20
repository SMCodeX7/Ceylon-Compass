import numpy as np
import pytest

from src.recommendation.traveller_profile import TravellerProfile


def make_profile(**overrides) -> TravellerProfile:
    data = {
        "starting_point": "Colombo",
        "trip_days": 6,
        "budget_usd": 500,
        "travel_style": "Budget",
        "crowd_preference": "Prefer Less Crowded Places",
        "transport": "Public Transport",
        "interests": ("Hiking", "Nature", "Adventure"),
    }

    data.update(overrides)

    return TravellerProfile(**data)


def test_profile_creation() -> None:
    profile = make_profile()

    assert profile.starting_point == "Colombo"
    assert profile.trip_days == 6
    assert profile.budget_usd == 500


def test_daily_budget_calculation() -> None:
    profile = make_profile()

    assert profile.daily_budget() == pytest.approx(
        83.333333,
        rel=1e-5,
    )


def test_interest_normalization() -> None:
    profile = make_profile(
        interests=(" Hiking ", "NATURE", "Adventure"),
    )

    assert profile.normalized_interests == (
        "hiking",
        "nature",
        "adventure",
    )


def test_interest_vector() -> None:
    profile = make_profile()

    expected = np.array(
        [0.0, 0.0, 5.0, 5.0, 0.0, 0.0, 5.0]
    )

    np.testing.assert_array_equal(
        profile.to_interest_vector(),
        expected,
    )


def test_profile_to_dict() -> None:
    profile = make_profile()

    result = profile.to_dict()

    assert result["starting_point"] == "Colombo"
    assert result["trip_days"] == 6
    assert result["budget_usd"] == 500
    assert result["daily_budget_usd"] == 83.33
    assert result["interests"] == [
        "hiking",
        "nature",
        "adventure",
    ]


def test_empty_starting_point_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Starting point cannot be empty",
    ):
        make_profile(starting_point="   ")


def test_invalid_trip_days_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Trip duration must be at least 1 day",
    ):
        make_profile(trip_days=0)


def test_invalid_budget_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Budget must be greater than 0",
    ):
        make_profile(budget_usd=0)


def test_invalid_travel_style_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Invalid travel style",
    ):
        make_profile(travel_style="Luxury")


def test_invalid_crowd_preference_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Invalid crowd preference",
    ):
        make_profile(crowd_preference="Very Quiet")


def test_invalid_transport_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Invalid transport option",
    ):
        make_profile(transport="Helicopter")


def test_empty_interests_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="At least one travel interest",
    ):
        make_profile(interests=())


def test_unknown_interest_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Unknown travel interests",
    ):
        make_profile(
            interests=("Nature", "Shopping"),
        )