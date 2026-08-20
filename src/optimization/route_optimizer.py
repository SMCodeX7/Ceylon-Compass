import pandas as pd
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

from src.optimization.distance import haversine_distance
from src.optimization.route_baseline import (
    get_starting_coordinates,
)


DISTANCE_SCALE = 1000


def build_optimizer_distance_matrix(
    destinations: pd.DataFrame,
    starting_point: str,
) -> list[list[int]]:
    """
    Build an integer distance matrix for OR-Tools.

    Nodes:
        0 = traveller starting point
        1..N = recommended destinations
        final node = dummy end node

    The dummy end node allows CeylonCompass to optimize
    an open route without forcing the traveller to return
    to the original starting point.
    """

    required_columns = {
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

    start_coordinates = get_starting_coordinates(
        starting_point
    )

    coordinates = [
        start_coordinates,
    ]

    for _, destination in destinations.iterrows():
        coordinates.append(
            (
                float(destination["latitude"]),
                float(destination["longitude"]),
            )
        )

    coordinates.append((0.0, 0.0))

    node_count = len(coordinates)
    dummy_end_index = node_count - 1

    matrix = [
        [0 for _ in range(node_count)]
        for _ in range(node_count)
    ]

    for from_index in range(node_count):
        for to_index in range(node_count):
            if from_index == to_index:
                continue

            if to_index == dummy_end_index:
                matrix[from_index][to_index] = 0
                continue

            if from_index == dummy_end_index:
                matrix[from_index][to_index] = 0
                continue

            latitude_1, longitude_1 = coordinates[
                from_index
            ]

            latitude_2, longitude_2 = coordinates[
                to_index
            ]

            distance_km = haversine_distance(
                latitude_1,
                longitude_1,
                latitude_2,
                longitude_2,
            )

            matrix[from_index][to_index] = int(
                round(
                    distance_km
                    * DISTANCE_SCALE
                )
            )

    return matrix


def _optimize_remaining_destinations(
    destinations: pd.DataFrame,
    starting_point: str,
) -> pd.DataFrame:
    """
    Optimize destinations that still need to be visited.

    This internal helper assumes destinations located
    at the traveller's starting point have already
    been handled.
    """

    if destinations.empty:
        return destinations.copy()

    destinations = (
        destinations
        .copy()
        .reset_index(drop=True)
    )

    distance_matrix = (
        build_optimizer_distance_matrix(
            destinations,
            starting_point,
        )
    )

    destination_count = len(destinations)

    start_node = 0
    dummy_end_node = destination_count + 1

    manager = pywrapcp.RoutingIndexManager(
        len(distance_matrix),
        1,
        [start_node],
        [dummy_end_node],
    )

    routing = pywrapcp.RoutingModel(
        manager
    )

    def distance_callback(
        from_index: int,
        to_index: int,
    ) -> int:
        from_node = manager.IndexToNode(
            from_index
        )

        to_node = manager.IndexToNode(
            to_index
        )

        return distance_matrix[
            from_node
        ][
            to_node
        ]

    transit_callback_index = (
        routing.RegisterTransitCallback(
            distance_callback
        )
    )

    routing.SetArcCostEvaluatorOfAllVehicles(
        transit_callback_index
    )

    search_parameters = (
        pywrapcp.DefaultRoutingSearchParameters()
    )

    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy
        .PATH_CHEAPEST_ARC
    )

    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic
        .GUIDED_LOCAL_SEARCH
    )

    search_parameters.time_limit.seconds = 2

    solution = routing.SolveWithParameters(
        search_parameters
    )

    if solution is None:
        raise RuntimeError(
            "OR-Tools could not generate a route."
        )

    ordered_destination_indexes: list[int] = []

    index = routing.Start(0)

    while not routing.IsEnd(index):
        node = manager.IndexToNode(index)

        if 1 <= node <= destination_count:
            ordered_destination_indexes.append(
                node - 1
            )

        index = solution.Value(
            routing.NextVar(index)
        )

    return (
        destinations
        .iloc[ordered_destination_indexes]
        .copy()
        .reset_index(drop=True)
    )


def optimize_route(
    destinations: pd.DataFrame,
    starting_point: str,
) -> pd.DataFrame:
    """
    Optimize recommended destination order using
    Google OR-Tools.

    If a recommended destination is the same as the
    traveller's starting point, it is visited first
    with zero travel distance.
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

    destinations = (
        destinations
        .copy()
        .reset_index(drop=True)
    )

    starting_mask = (
        destinations["name"]
        .astype(str)
        .str.casefold()
        == starting_point.casefold()
    )

    starting_destinations = (
        destinations[starting_mask]
        .copy()
        .reset_index(drop=True)
    )

    remaining_destinations = (
        destinations[~starting_mask]
        .copy()
        .reset_index(drop=True)
    )

    optimized_remaining = (
        _optimize_remaining_destinations(
            remaining_destinations,
            starting_point,
        )
    )

    routed = pd.concat(
        [
            starting_destinations,
            optimized_remaining,
        ],
        ignore_index=True,
    )

    routed["route_order"] = range(
        1,
        len(routed) + 1,
    )

    start_latitude, start_longitude = (
        get_starting_coordinates(
            starting_point
        )
    )

    previous_latitude = start_latitude
    previous_longitude = start_longitude

    segment_distances: list[float] = []

    for _, destination in routed.iterrows():
        distance = haversine_distance(
            previous_latitude,
            previous_longitude,
            float(destination["latitude"]),
            float(destination["longitude"]),
        )

        segment_distances.append(
            round(distance, 2)
        )

        previous_latitude = float(
            destination["latitude"]
        )

        previous_longitude = float(
            destination["longitude"]
        )

    routed["distance_from_previous_km"] = (
        segment_distances
    )

    return routed


def calculate_optimized_route_distance(
    routed_destinations: pd.DataFrame,
) -> float:
    """Return total distance of an optimized route."""

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