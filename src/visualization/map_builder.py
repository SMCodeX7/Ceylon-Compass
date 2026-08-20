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


def _validate_optimized_route(
    optimized_route: pd.DataFrame,
) -> None:
    """
    Validate optimized route data before route
    visualization.
    """

    _validate_destinations(
        optimized_route
    )

    if (
        "route_order"
        not in optimized_route.columns
    ):
        raise ValueError(
            "Optimized route map data is missing "
            "the route_order column."
        )

    route_order = pd.to_numeric(
        optimized_route[
            "route_order"
        ],
        errors="coerce",
    )

    if route_order.isna().any():
        raise ValueError(
            "Route order values must be numeric."
        )

    if (
        route_order
        <= 0
    ).any():
        raise ValueError(
            "Route order values must be positive."
        )

    if route_order.duplicated().any():
        raise ValueError(
            "Route order values must be unique."
        )

    sorted_orders = sorted(
        int(value)
        for value in route_order
    )

    expected_orders = list(
        range(
            1,
            len(optimized_route) + 1,
        )
    )

    if sorted_orders != expected_orders:
        raise ValueError(
            "Route order values must form a "
            "continuous sequence starting from 1."
        )


def _destination_popup(
    destination: pd.Series,
) -> str:
    """
    Build destination information for a marker
    popup.
    """

    popup_lines = [
        f"<b>{destination['name']}</b>",
    ]

    if (
        "route_order"
        in destination.index
    ):
        popup_lines.append(
            "Route Stop: "
            f"{int(destination['route_order'])}"
        )

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

    if (
        "distance_from_previous_km"
        in destination.index
    ):
        popup_lines.append(
            "Distance From Previous: "
            f"{float(destination['distance_from_previous_km']):.1f} km"
        )

    return "<br>".join(
        popup_lines
    )


def _create_base_map() -> folium.Map:
    """
    Create the shared OpenStreetMap map object.
    """

    return folium.Map(
        location=DEFAULT_MAP_CENTER,
        zoom_start=DEFAULT_ZOOM_START,
        tiles="OpenStreetMap",
        control_scale=True,
    )


def _add_starting_point_marker(
    trip_map: folium.Map,
    starting_point: str,
) -> tuple[float, float]:
    """
    Add the traveller's starting point to the map.
    """

    start_latitude, start_longitude = (
        get_starting_coordinates(
            starting_point
        )
    )

    start_latitude = float(
        start_latitude
    )

    start_longitude = float(
        start_longitude
    )

    _validate_coordinates(
        start_latitude,
        start_longitude,
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

    return (
        start_latitude,
        start_longitude,
    )


def build_destination_map(
    destinations: pd.DataFrame,
    starting_point: str | None = None,
) -> folium.Map:
    """
    Build an interactive OpenStreetMap-based Folium
    map containing destination markers.
    """

    _validate_destinations(
        destinations
    )

    trip_map = (
        _create_base_map()
    )

    map_points: list[
        tuple[float, float]
    ] = []

    if starting_point is not None:
        start_coordinates = (
            _add_starting_point_marker(
                trip_map,
                starting_point,
            )
        )

        map_points.append(
            start_coordinates
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

    trip_map.fit_bounds(
        map_points,
        padding=(
            30,
            30,
        ),
    )

    return trip_map


def build_optimized_route_map(
    optimized_route: pd.DataFrame,
    starting_point: str,
) -> folium.Map:
    """
    Build an interactive route map showing:

    - the traveller starting point,
    - optimized route order,
    - numbered destination markers,
    - a line connecting the route.

    The connecting line represents the geographic
    sequence between coordinates. It is not a
    road-navigation path.
    """

    _validate_optimized_route(
        optimized_route
    )

    route = (
        optimized_route
        .sort_values(
            "route_order"
        )
        .reset_index(
            drop=True
        )
    )

    trip_map = (
        _create_base_map()
    )

    start_coordinates = (
        _add_starting_point_marker(
            trip_map,
            starting_point,
        )
    )

    map_points: list[
        tuple[float, float]
    ] = [
        start_coordinates
    ]

    route_line_points: list[
        tuple[float, float]
    ] = [
        start_coordinates
    ]

    for _, destination in (
        route.iterrows()
    ):
        route_order = int(
            destination[
                "route_order"
            ]
        )

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

        marker_html = f"""
        <div
            class="route-stop-number"
            style="
                background-color: #2563eb;
                color: white;
                border: 2px solid white;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                line-height: 26px;
                text-align: center;
                font-size: 14px;
                font-weight: bold;
                box-shadow: 0 1px 4px rgba(0,0,0,0.45);
            "
        >
            {route_order}
        </div>
        """

        folium.Marker(
            location=[
                latitude,
                longitude,
            ],
            tooltip=(
                f"Stop {route_order}: "
                f"{destination['name']}"
            ),
            popup=folium.Popup(
                _destination_popup(
                    destination
                ),
                max_width=320,
            ),
            icon=folium.DivIcon(
                html=marker_html,
                icon_size=(
                    30,
                    30,
                ),
                icon_anchor=(
                    15,
                    15,
                ),
            ),
        ).add_to(
            trip_map
        )

        coordinates = (
            latitude,
            longitude,
        )

        map_points.append(
            coordinates
        )

        route_line_points.append(
            coordinates
        )

    folium.PolyLine(
        locations=route_line_points,
        weight=5,
        opacity=0.8,
        tooltip=(
            "Optimized Geographic Route"
        ),
    ).add_to(
        trip_map
    )

    trip_map.fit_bounds(
        map_points,
        padding=(
            30,
            30,
        ),
    )

    return trip_map