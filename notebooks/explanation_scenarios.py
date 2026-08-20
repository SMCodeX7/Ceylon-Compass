from src.recommendation.explanations import explain_destination
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
        "name": "Wildlife Nature Traveller",
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
        "name": "Culture History Traveller",
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
        "name": "Adventure Hiking Traveller",
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
    print("\nCEYLONCOMPASS EXPLANATION AUDIT")
    print("=" * 72)

    for scenario in SCENARIOS:
        profile = scenario["profile"]

        recommendations = rank_destinations(
            profile,
            top_n=3,
        )

        print(f"\n{scenario['name']}")
        print("=" * 72)

        for _, destination in recommendations.iterrows():
            explanation = explain_destination(
                destination,
                profile,
            )

            print(
                f"\n#{int(destination['recommendation_rank'])} "
                f"{destination['name']} "
                f"({destination['current_stage_score']:.2f}%)"
            )

            print("Reasons:")

            for reason in explanation["reasons"]:
                print(f"  + {reason}")

            if explanation["tradeoffs"]:
                print("Trade-offs:")

                for tradeoff in explanation["tradeoffs"]:
                    print(f"  - {tradeoff}")
            else:
                print("Trade-offs: None")


if __name__ == "__main__":
    main()