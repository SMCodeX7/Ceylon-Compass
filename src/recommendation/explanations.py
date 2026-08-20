import pandas as pd

from src.recommendation.traveller_profile import TravellerProfile


HIGH_MATCH_THRESHOLD = 4
MODERATE_MATCH_THRESHOLD = 3


def get_interest_reasons(
    destination: pd.Series,
    profile: TravellerProfile,
) -> list[str]:
    """Explain which selected interests match a destination."""

    reasons: list[str] = []

    for interest in profile.normalized_interests:
        score = float(destination[interest])

        readable_interest = interest.title()

        if score >= HIGH_MATCH_THRESHOLD:
            reasons.append(
                f"Strong match for {readable_interest}"
            )

        elif score >= MODERATE_MATCH_THRESHOLD:
            reasons.append(
                f"Moderate match for {readable_interest}"
            )

    return reasons


def get_budget_reason(
    destination: pd.Series,
) -> str:
    """Explain destination budget compatibility."""

    if bool(destination["budget_compatible"]):
        return "Fits within your estimated daily budget"

    return (
        "Estimated daily cost is above your current "
        "daily budget"
    )


def get_crowd_reason(
    destination: pd.Series,
    profile: TravellerProfile,
) -> str | None:
    """Explain crowd compatibility."""

    crowd_level = int(destination["crowd_level"])

    if profile.crowd_preference == "No Preference":
        return None

    if (
        profile.crowd_preference
        == "Prefer Less Crowded Places"
    ):
        if crowd_level <= 2:
            return "Relatively low crowd level"

        if crowd_level == 3:
            return "Moderate crowd level"

        return "May be busier than you prefer"

    if (
        profile.crowd_preference
        == "Popular Tourist Places"
    ):
        if crowd_level >= 4:
            return "Popular and frequently visited destination"

        if crowd_level == 3:
            return "Moderately popular destination"

        return "Quieter than your selected crowd preference"

    return None


def get_tradeoffs(
    destination: pd.Series,
    profile: TravellerProfile,
) -> list[str]:
    """Identify relevant weaknesses in a recommendation."""

    tradeoffs: list[str] = []

    for interest in profile.normalized_interests:
        score = float(destination[interest])

        if score <= 2:
            tradeoffs.append(
                f"Limited {interest.title()} relevance"
            )

    if not bool(destination["budget_compatible"]):
        tradeoffs.append(
            "May require more than your estimated daily budget"
        )

    return tradeoffs


def explain_destination(
    destination: pd.Series,
    profile: TravellerProfile,
) -> dict:
    """
    Produce deterministic explanation information
    for a ranked destination.
    """

    reasons = get_interest_reasons(
        destination,
        profile,
    )

    reasons.append(
        get_budget_reason(destination)
    )

    crowd_reason = get_crowd_reason(
        destination,
        profile,
    )

    if crowd_reason:
        reasons.append(crowd_reason)

    tradeoffs = get_tradeoffs(
        destination,
        profile,
    )

    return {
        "destination": destination["name"],
        "score": float(
            destination["current_stage_score"]
        ),
        "reasons": reasons,
        "tradeoffs": tradeoffs,
    }