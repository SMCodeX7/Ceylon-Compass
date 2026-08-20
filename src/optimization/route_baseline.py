import pandas as pd

from src.optimization.distance import haversine_distance


STARTING_POINT_COORDINATES = {
    "Colombo": (6.9271, 79.8612),
    "Kandy": (7.2906, 80.6337),
    "Galle": (6.0329, 80.2168),
    "Jaffna": (9.6615, 80.0255),
    "Negombo": (7.2083, 79.8358),
}


def get_starting_coordinates(
    starting_point: str,
) -> tuple[float, float]:
    """
    Return latitude and longitude for a supported
    traveller starting point.
    """

    if starting_point not in STARTING_POINT_COORDINATES:
        raise ValueError(
            f"Unsupported starting point: {starting_point}"
        )

    return STARTING_POINT_COORDINATES[
        starting_point
    ]


def nearest_neighbour_route(
    destinations: pd.DataFrame,
    starting_point: str,
) -> pd.DataFrame:
    """
    Order recommended destinations using a
    nearest-neighbour route heuristic.

    The algorithm starts at the traveller's selected
    starting point and repeatedly visits the closest
    unvisited destination.
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
            "Destination data is missing route columns: "
            + ", ".join(sorted(missing_columns))
        )

    if destinations.empty:
        return destinations.copy()

    start_latitude, start_longitude = (
        get_starting_coordinates(
            starting_point
        )
    )

    remaining = destinations.copy().reset_index(
        drop=True
    )

    ordered_rows = []

    current_latitude = start_latitude
    current_longitude = start_longitude

    route_order = 1

    while not remaining.empty:
        distances = remaining.apply(
            lambda destination: haversine_distance(
                current_latitude,
                current_longitude,
                float(destination["latitude"]),
                float(destination["longitude"]),
            ),
            axis=1,
        )

        nearest_index = distances.idxmin()

        nearest_destination = (
            remaining.loc[nearest_index].copy()
        )

        nearest_destination[
            "distance_from_previous_km"
        ] = round(
            float(distances.loc[nearest_index]),
            2,
        )

        nearest_destination[
            "route_order"
        ] = route_order

        ordered_rows.append(
            nearest_destination
        )

        current_latitude = float(
            nearest_destination["latitude"]
        )

        current_longitude = float(
            nearest_destination["longitude"]
        )

        remaining = (
            remaining
            .drop(index=nearest_index)
            .reset_index(drop=True)
        )

        route_order += 1

    routed = pd.DataFrame(
        ordered_rows
    ).reset_index(drop=True)

    return routed


def calculate_baseline_route_distance(
    routed_destinations: pd.DataFrame,
) -> float:
    """
    Calculate the total distance represented by a
    nearest-neighbour route result.
    """

    if routed_destinations.empty:
        return 0.0

    if (
        "distance_from_previous_km"
        not in routed_destinations.columns
    ):
        raise ValueError(
            "Route data is missing "
            "distance_from_previous_km."
        )

    return float(
        routed_destinations[
            "distance_from_previous_km"
        ].sum()
    )