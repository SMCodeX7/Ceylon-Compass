from src.recommendation.recommender import rank_destinations
from src.recommendation.traveller_profile import TravellerProfile


SCENARIOS = [
    {
        "name": "Budget Beach Traveller",
        "profile": TravellerProfile(
            starting_point="Colombo",
            trip_days=4,
            budget_usd=120,
            travel_style="Budget",
            crowd_preference="No Preference",
            transport="Public Transport",
            interests=("Beach",),
        ),
    },
    {
        "name": "Wildlife Traveller",
        "profile": TravellerProfile(
            starting_point="Colombo",
            trip_days=5,
            budget_usd=400,
            travel_style="Balanced",
            crowd_preference="Prefer Less Crowded Places",
            transport="Mixed Transport",
            interests=("Wildlife", "Nature"),
        ),
    },
    {
        "name": "Culture and History Traveller",
        "profile": TravellerProfile(
            starting_point="Kandy",
            trip_days=5,
            budget_usd=350,
            travel_style="Balanced",
            crowd_preference="No Preference",
            transport="Public Transport",
            interests=("Culture", "History"),
        ),
    },
    {
        "name": "Adventure and Hiking Traveller",
        "profile": TravellerProfile(
            starting_point="Colombo",
            trip_days=6,
            budget_usd=500,
            travel_style="Budget",
            crowd_preference="Prefer Less Crowded Places",
            transport="Public Transport",
            interests=("Hiking", "Nature", "Adventure"),
        ),
    },
    {
        "name": "Popular Coastal Traveller",
        "profile": TravellerProfile(
            starting_point="Galle",
            trip_days=5,
            budget_usd=600,
            travel_style="Comfort",
            crowd_preference="Popular Tourist Places",
            transport="Private Vehicle",
            interests=("Beach", "Adventure"),
        ),
    },
]


def main() -> None:
    print("\nCEYLONCOMPASS MULTI-PROFILE CHECK")
    print("=" * 70)

    for scenario in SCENARIOS:
        profile = scenario["profile"]

        results = rank_destinations(
            profile,
            top_n=5,
        )

        print(f"\n{scenario['name']}")
        print("-" * 70)

        print(
            f"Daily Budget: "
            f"${profile.daily_budget():.2f}"
        )

        print(
            f"Interests: "
            f"{', '.join(profile.normalized_interests)}"
        )

        print(
            f"Crowd Preference: "
            f"{profile.crowd_preference}"
        )

        print()

        print(
            results[
                [
                    "recommendation_rank",
                    "name",
                    "category",
                    "estimated_daily_cost_usd",
                    "preference_score",
                    "budget_score",
                    "crowd_score",
                    "current_stage_score",
                ]
            ].to_string(index=False)
        )


if __name__ == "__main__":
    main()