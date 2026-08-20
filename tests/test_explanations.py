import pandas as pd

from src.recommendation.explanations import (
    explain_destination,
    get_budget_reason,
    get_crowd_reason,
    get_interest_reasons,
    get_tradeoffs,
)
from src.recommendation.traveller_profile import TravellerProfile


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


def make_destination(**overrides) -> pd.Series:
    data = {
        "name": "Test Destination",
        "hiking": 5,
        "nature": 4,
        "adventure": 3,
        "beach": 0,
        "wildlife": 1,
        "culture": 1,
        "history": 1,
        "budget_compatible": True,
        "crowd_level": 2,
        "current_stage_score": 90.0,
    }

    data.update(overrides)

    return pd.Series(data)


def test_strong_interest_reason() -> None:
    destination = make_destination(
        hiking=5,
    )

    reasons = get_interest_reasons(
        destination,
        make_profile(
            interests=("Hiking",),
        ),
    )

    assert "Strong match for Hiking" in reasons


def test_moderate_interest_reason() -> None:
    destination = make_destination(
        adventure=3,
    )

    reasons = get_interest_reasons(
        destination,
        make_profile(
            interests=("Adventure",),
        ),
    )

    assert "Moderate match for Adventure" in reasons


def test_low_interest_is_not_positive_reason() -> None:
    destination = make_destination(
        hiking=2,
    )

    reasons = get_interest_reasons(
        destination,
        make_profile(
            interests=("Hiking",),
        ),
    )

    assert reasons == []


def test_budget_reason_when_compatible() -> None:
    destination = make_destination(
        budget_compatible=True,
    )

    reason = get_budget_reason(destination)

    assert reason == (
        "Fits within your estimated daily budget"
    )


def test_budget_reason_when_not_compatible() -> None:
    destination = make_destination(
        budget_compatible=False,
    )

    reason = get_budget_reason(destination)

    assert "above your current daily budget" in reason


def test_less_crowded_reason() -> None:
    destination = make_destination(
        crowd_level=2,
    )

    reason = get_crowd_reason(
        destination,
        make_profile(
            crowd_preference="Prefer Less Crowded Places",
        ),
    )

    assert reason == "Relatively low crowd level"


def test_busy_destination_warning() -> None:
    destination = make_destination(
        crowd_level=5,
    )

    reason = get_crowd_reason(
        destination,
        make_profile(
            crowd_preference="Prefer Less Crowded Places",
        ),
    )

    assert reason == "May be busier than you prefer"


def test_popular_destination_reason() -> None:
    destination = make_destination(
        crowd_level=5,
    )

    reason = get_crowd_reason(
        destination,
        make_profile(
            crowd_preference="Popular Tourist Places",
        ),
    )

    assert reason == (
        "Popular and frequently visited destination"
    )


def test_no_crowd_preference_returns_none() -> None:
    destination = make_destination()

    reason = get_crowd_reason(
        destination,
        make_profile(
            crowd_preference="No Preference",
        ),
    )

    assert reason is None


def test_low_interest_becomes_tradeoff() -> None:
    destination = make_destination(
        hiking=1,
    )

    tradeoffs = get_tradeoffs(
        destination,
        make_profile(
            interests=("Hiking",),
        ),
    )

    assert "Limited Hiking relevance" in tradeoffs


def test_budget_issue_becomes_tradeoff() -> None:
    destination = make_destination(
        budget_compatible=False,
    )

    tradeoffs = get_tradeoffs(
        destination,
        make_profile(),
    )

    assert (
        "May require more than your estimated daily budget"
        in tradeoffs
    )


def test_explanation_structure() -> None:
    destination = make_destination()

    explanation = explain_destination(
        destination,
        make_profile(),
    )

    assert explanation["destination"] == "Test Destination"
    assert explanation["score"] == 90.0
    assert isinstance(explanation["reasons"], list)
    assert isinstance(explanation["tradeoffs"], list)


def test_explanation_contains_budget_reason() -> None:
    destination = make_destination(
        budget_compatible=True,
    )

    explanation = explain_destination(
        destination,
        make_profile(),
    )

    assert (
        "Fits within your estimated daily budget"
        in explanation["reasons"]
    )


def test_explanation_contains_crowd_reason() -> None:
    destination = make_destination(
        crowd_level=2,
    )

    explanation = explain_destination(
        destination,
        make_profile(),
    )

    assert (
        "Relatively low crowd level"
        in explanation["reasons"]
    )