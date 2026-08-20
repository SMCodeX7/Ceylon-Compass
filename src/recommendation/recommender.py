from pathlib import Path

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from src.recommendation.traveller_profile import (
    INTERESTS,
    TravellerProfile,
)
from src.utils.data_validation import validate_dataset


DATA_PATH = Path("data/destinations.csv")

PREFERENCE_WEIGHT = 0.45
BUDGET_WEIGHT = 0.20
CROWD_WEIGHT = 0.10

CURRENT_WEIGHT_TOTAL = (
    PREFERENCE_WEIGHT
    + BUDGET_WEIGHT
    + CROWD_WEIGHT
)


def calculate_preference_similarity(
    destinations: pd.DataFrame,
    profile: TravellerProfile,
) -> pd.DataFrame:
    """
    Calculate cosine similarity between a traveller's
    interest vector and destination interest vectors.
    """

    required_columns = set(INTERESTS)

    if not required_columns.issubset(destinations.columns):
        missing = (
            required_columns
            - set(destinations.columns)
        )

        raise ValueError(
            "Destination data is missing interest columns: "
            + ", ".join(sorted(missing))
        )

    traveller_vector = (
        profile.to_interest_vector()
        .reshape(1, -1)
    )

    destination_matrix = (
        destinations[INTERESTS]
        .astype(float)
        .to_numpy()
    )

    similarities = cosine_similarity(
        destination_matrix,
        traveller_vector,
    ).flatten()

    results = destinations.copy()

    results["preference_similarity"] = similarities

    results["preference_score"] = (
        results["preference_similarity"]
        * 100
    ).round(2)

    return results


def calculate_budget_scores(
    destinations: pd.DataFrame,
    profile: TravellerProfile,
) -> pd.DataFrame:
    """
    Calculate destination affordability relative to
    the traveller's available daily budget.

    A destination within the daily budget receives 100.

    Destinations above the daily budget receive a
    gradually decreasing score based on the
    affordability ratio.
    """

    results = destinations.copy()

    daily_budget = profile.daily_budget()

    destination_costs = (
        results[
            "estimated_daily_cost_usd"
        ]
        .astype(float)
    )

    affordability_ratio = (
        daily_budget
        / destination_costs
    )

    results["budget_compatible"] = (
        destination_costs
        <= daily_budget
    )

    results["budget_score"] = (
        affordability_ratio
        .clip(upper=1.0)
        .mul(100)
        .round(2)
    )

    return results


def calculate_crowd_scores(
    destinations: pd.DataFrame,
    profile: TravellerProfile,
) -> pd.DataFrame:
    """
    Calculate compatibility between destination crowd
    level and the traveller's crowd preference.

    crowd_level:
        1 = very low crowd
        5 = very high crowd
    """

    results = destinations.copy()

    crowd_levels = (
        results["crowd_level"]
        .astype(float)
    )

    if (
        profile.crowd_preference
        == "No Preference"
    ):
        crowd_scores = pd.Series(
            100.0,
            index=results.index,
        )

    elif (
        profile.crowd_preference
        == "Prefer Less Crowded Places"
    ):
        crowd_scores = (
            (6.0 - crowd_levels)
            / 5.0
            * 100
        )

    elif (
        profile.crowd_preference
        == "Popular Tourist Places"
    ):
        crowd_scores = (
            crowd_levels
            / 5.0
            * 100
        )

    else:
        raise ValueError(
            "Unsupported crowd preference: "
            f"{profile.crowd_preference}"
        )

    results["crowd_score"] = (
        crowd_scores.round(2)
    )

    return results


def calculate_current_stage_scores(
    destinations: pd.DataFrame,
    profile: TravellerProfile,
) -> pd.DataFrame:
    """
    Calculate the current recommendation score using
    the components implemented so far.

    Current components:
        45% preference similarity
        20% budget compatibility
        10% crowd compatibility

    Weather and route-efficiency components will be
    added later.

    Because the available weights currently total
    0.75, the partial weighted result is normalized
    back to 0-100.
    """

    results = calculate_preference_similarity(
        destinations,
        profile,
    )

    results = calculate_budget_scores(
        results,
        profile,
    )

    results = calculate_crowd_scores(
        results,
        profile,
    )

    weighted_score = (
        results["preference_score"]
        * PREFERENCE_WEIGHT
        + results["budget_score"]
        * BUDGET_WEIGHT
        + results["crowd_score"]
        * CROWD_WEIGHT
    )

    results["current_stage_score"] = (
        weighted_score
        / CURRENT_WEIGHT_TOTAL
    ).round(2)

    return results


def rank_destinations(
    profile: TravellerProfile,
    top_n: int = 10,
    data_path: Path = DATA_PATH,
) -> pd.DataFrame:
    """
    Rank destinations using the recommendation
    components currently implemented by
    CeylonCompass.

    Geographic and itinerary-related fields are
    retained so ranked destinations can be passed
    directly into later route optimization and
    itinerary modules.
    """

    if top_n < 1:
        raise ValueError(
            "top_n must be at least 1."
        )

    destinations = validate_dataset(
        data_path
    )

    scored = calculate_current_stage_scores(
        destinations,
        profile,
    )

    ranked = (
        scored
        .sort_values(
            by=[
                "current_stage_score",
                "preference_score",
                "name",
            ],
            ascending=[
                False,
                False,
                True,
            ],
        )
        .reset_index(drop=True)
    )

    ranked["recommendation_rank"] = (
        ranked.index + 1
    )

    columns = [
        "recommendation_rank",
        "destination_id",
        "name",
        "district",
        "province",
        "latitude",
        "longitude",
        "category",
        *INTERESTS,
        "estimated_daily_cost_usd",
        "recommended_duration_hours",
        "crowd_level",
        "fitness_requirement",
        "family_suitability",
        "best_months",
        "preference_similarity",
        "preference_score",
        "budget_score",
        "budget_compatible",
        "crowd_score",
        "current_stage_score",
    ]

    return (
        ranked[columns]
        .head(top_n)
    )


if __name__ == "__main__":
    example_profile = TravellerProfile(
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

    recommendations = rank_destinations(
        example_profile,
        top_n=10,
    )

    print(
        recommendations[
            [
                "recommendation_rank",
                "name",
                "latitude",
                "longitude",
                "estimated_daily_cost_usd",
                "preference_score",
                "budget_score",
                "crowd_score",
                "current_stage_score",
            ]
        ].to_string(index=False)
    )