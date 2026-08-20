from __future__ import annotations

import folium
import pandas as pd

from src.optimization.route_baseline import (
    get_starting_coordinates,
)


DEFAULT_MAP_CENTER = (
    7.8731,
    80.7718,
)

DEFAULT_ZOOM_START = 7


def _validate_coordinates(
    latitude: float,
    longitude: float,
) -> None:
    """
    Validate geographic coordinates before adding
    them to a Folium map.
    """

    if not -90 <= latitude <= 90:
        raise ValueError(
            "Latitude must be between -90 and 90."
        )

    if not -180 <= longitude <= 180:
        raise ValueError(
            "Longitude must be between -180 and 180."
        )


def _validate_destinations(
    destinations: pd.DataFrame,
) -> None:
    """
    Validate the minimum destination fields required
    for map visualization.
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
            "Destination map data is missing columns: "
            + ", ".join(
                sorted(missing_columns)
            )
        )

    if destinations.empty:
        raise ValueError(
            "Cannot build a destination map from "
            "an empty dataset."
        )

    if destinations[
        [
            "latitude",
            "longitude",
        ]
    ].isna().any().any():
        raise ValueError(
            "Destination coordinates cannot be missing."
        )

    for _, destination in (
        destinations.iterrows()
    ):
        _validate_coordinates(
            float(
                destination[
                    "latitude"
                ]
            ),
            float(
                destination[
                    "longitude"
                ]
            ),
        )


def _destination_popup(
    destination: pd.Series,
) -> str:
    """
    Build simple destination information for the
    marker popup.
    """

    popup_lines = [
        f"<b>{destination['name']}</b>",
    ]

    if "category" in destination.index:
        popup_lines.append(
            f"Category: {destination['category']}"
        )

    if "district" in destination.index:
        popup_lines.append(
            f"District: {destination['district']}"
        )

    if (
        "current_stage_score"
        in destination.index
    ):
        popup_lines.append(
            "Recommendation Score: "
            f"{float(destination['current_stage_score']):.1f}%"
        )

    if (
        "recommended_duration_hours"
        in destination.index
    ):
        popup_lines.append(
            "Visit Duration: "
            f"{float(destination['recommended_duration_hours']):.0f} h"
        )

    return "<br>".join(
        popup_lines
    )


def build_destination_map(
    destinations: pd.DataFrame,
    starting_point: str | None = None,
) -> folium.Map:
    """
    Build an interactive OpenStreetMap-based Folium
    map containing destination markers.

    A starting-point marker is also included when a
    supported starting point is supplied.

    Route lines and numbered route-order markers are
    intentionally added in the next visualization
    stage.
    """

    _validate_destinations(
        destinations
    )

    trip_map = folium.Map(
        location=DEFAULT_MAP_CENTER,
        zoom_start=DEFAULT_ZOOM_START,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    map_points: list[
        tuple[float, float]
    ] = []

    if starting_point is not None:
        start_latitude, start_longitude = (
            get_starting_coordinates(
                starting_point
            )
        )

        _validate_coordinates(
            float(start_latitude),
            float(start_longitude),
        )

        folium.Marker(
            location=[
                start_latitude,
                start_longitude,
            ],
            tooltip=(
                f"Starting Point: "
                f"{starting_point}"
            ),
            popup=(
                f"<b>Starting Point</b><br>"
                f"{starting_point}"
            ),
            icon=folium.Icon(
                color="green",
                icon="home",
                prefix="fa",
            ),
        ).add_to(
            trip_map
        )

        map_points.append(
            (
                float(start_latitude),
                float(start_longitude),
            )
        )

    for _, destination in (
        destinations.iterrows()
    ):
        latitude = float(
            destination[
                "latitude"
            ]
        )

        longitude = float(
            destination[
                "longitude"
            ]
        )

        folium.Marker(
            location=[
                latitude,
                longitude,
            ],
            tooltip=str(
                destination[
                    "name"
                ]
            ),
            popup=folium.Popup(
                _destination_popup(
                    destination
                ),
                max_width=300,
            ),
            icon=folium.Icon(
                color="blue",
                icon="map-marker",
                prefix="fa",
            ),
        ).add_to(
            trip_map
        )

        map_points.append(
            (
                latitude,
                longitude,
            )
        )

    if map_points:
        trip_map.fit_bounds(
            map_points,
            padding=(
                30,
                30,
            ),
        )

    return trip_map