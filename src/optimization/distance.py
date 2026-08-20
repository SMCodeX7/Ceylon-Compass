from math import asin, cos, radians, sin, sqrt

import numpy as np
import pandas as pd


EARTH_RADIUS_KM = 6371.0088


def haversine_distance(
    latitude_1: float,
    longitude_1: float,
    latitude_2: float,
    longitude_2: float,
) -> float:
    """
    Calculate the great-circle distance between two
    geographic coordinates using the Haversine formula.

    Returns distance in kilometres.
    """

    lat1 = radians(latitude_1)
    lon1 = radians(longitude_1)
    lat2 = radians(latitude_2)
    lon2 = radians(longitude_2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    haversine_value = (
        sin(delta_lat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(delta_lon / 2) ** 2
    )

    central_angle = 2 * asin(
        sqrt(haversine_value)
    )

    return EARTH_RADIUS_KM * central_angle


def build_distance_matrix(
    destinations: pd.DataFrame,
) -> np.ndarray:
    """
    Build a symmetric pairwise distance matrix
    for a collection of destinations.

    Required columns:
        latitude
        longitude
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
            "Destination data is missing geographic columns: "
            + ", ".join(sorted(missing_columns))
        )

    destination_count = len(destinations)

    distance_matrix = np.zeros(
        (
            destination_count,
            destination_count,
        ),
        dtype=float,
    )

    for i in range(destination_count):
        for j in range(
            i + 1,
            destination_count,
        ):
            distance = haversine_distance(
                float(
                    destinations.iloc[i][
                        "latitude"
                    ]
                ),
                float(
                    destinations.iloc[i][
                        "longitude"
                    ]
                ),
                float(
                    destinations.iloc[j][
                        "latitude"
                    ]
                ),
                float(
                    destinations.iloc[j][
                        "longitude"
                    ]
                ),
            )

            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance

    return distance_matrix


def calculate_route_distance(
    destinations: pd.DataFrame,
) -> float:
    """
    Calculate the total distance of destinations
    visited sequentially in their current order.
    """

    if len(destinations) < 2:
        return 0.0

    total_distance = 0.0

    for index in range(
        len(destinations) - 1
    ):
        current = destinations.iloc[index]
        next_destination = destinations.iloc[
            index + 1
        ]

        total_distance += haversine_distance(
            float(current["latitude"]),
            float(current["longitude"]),
            float(next_destination["latitude"]),
            float(next_destination["longitude"]),
        )

    return total_distance