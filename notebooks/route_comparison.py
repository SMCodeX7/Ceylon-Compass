from src.optimization.route_baseline import (
    calculate_baseline_route_distance,
    nearest_neighbour_route,
)
from src.optimization.route_optimizer import (
    calculate_optimized_route_distance,
    optimize_route,
)
from src.recommendation.recommender import rank_destinations
from src.recommendation.traveller_profile import TravellerProfile


SCENARIOS = [
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
        "name": "Beach Traveller",
        "profile": TravellerProfile(
            starting_point="Colombo",
            trip_days=5,
            budget_usd=500,
            travel_style="Balanced",
            crowd_preference="No Preference",
            transport="Mixed Transport",
            interests=("Beach",),
        ),
    },
    {
        "name": "Wildlife Traveller",
        "profile": TravellerProfile(
            starting_point="Colombo",
            trip_days=6,
            budget_usd=600,
            travel_style="Balanced",
            crowd_preference="Prefer Less Crowded Places",
            transport="Private Vehicle",
            interests=("Wildlife", "Nature"),
        ),
    },
    {
        "name": "Culture History Traveller",
        "profile": TravellerProfile(
            starting_point="Kandy",
            trip_days=6,
            budget_usd=500,
            travel_style="Balanced",
            crowd_preference="No Preference",
            transport="Public Transport",
            interests=("Culture", "History"),
        ),
    },
    {
        "name": "Popular Coastal Traveller",
        "profile": TravellerProfile(
            starting_point="Galle",
            trip_days=5,
            budget_usd=700,
            travel_style="Comfort",
            crowd_preference="Popular Tourist Places",
            transport="Private Vehicle",
            interests=("Beach", "Adventure"),
        ),
    },
]


def main() -> None:
    print("\nCEYLONCOMPASS ROUTE OPTIMIZATION COMPARISON")
    print("=" * 78)

    for scenario in SCENARIOS:
        profile = scenario["profile"]

        recommendations = rank_destinations(
            profile,
            top_n=7,
        )

        baseline_route = nearest_neighbour_route(
            recommendations,
            profile.starting_point,
        )

        optimized_route = optimize_route(
            recommendations,
            profile.starting_point,
        )

        baseline_distance = (
            calculate_baseline_route_distance(
                baseline_route
            )
        )

        optimized_distance = (
            calculate_optimized_route_distance(
                optimized_route
            )
        )

        improvement_km = (
            baseline_distance
            - optimized_distance
        )

        if baseline_distance > 0:
            improvement_percent = (
                improvement_km
                / baseline_distance
                * 100
            )
        else:
            improvement_percent = 0.0

        print(f"\n{scenario['name']}")
        print("-" * 78)

        print(
            f"Starting Point: "
            f"{profile.starting_point}"
        )

        print("\nBaseline Route:")

        print(
            " -> ".join(
                baseline_route["name"].tolist()
            )
        )

        print(
            f"Baseline Distance: "
            f"{baseline_distance:.2f} km"
        )

        print("\nOR-Tools Route:")

        print(
            " -> ".join(
                optimized_route["name"].tolist()
            )
        )

        print(
            f"Optimized Distance: "
            f"{optimized_distance:.2f} km"
        )

        print(
            f"Distance Saved: "
            f"{improvement_km:.2f} km"
        )

        print(
            f"Improvement: "
            f"{improvement_percent:.2f}%"
        )


if __name__ == "__main__":
    main()