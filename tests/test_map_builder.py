import folium
import pandas as pd
import pytest

from src.visualization.map_builder import (
    build_destination_map,
    build_optimized_route_map,
)


def make_destinations() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": [
                "Destination A",
                "Destination B",
            ],
            "latitude": [
                7.2,
                7.5,
            ],
            "longitude": [
                80.1,
                80.6,
            ],
            "category": [
                "Nature",
                "Hiking",
            ],
            "district": [
                "District A",
                "District B",
            ],
            "current_stage_score": [
                90.0,
                85.0,
            ],
            "recommended_duration_hours": [
                4.0,
                5.0,
            ],
        }
    )


def make_route() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": [
                "Second Stop",
                "First Stop",
                "Third Stop",
            ],
            "latitude": [
                7.2,
                6.95,
                7.6,
            ],
            "longitude": [
                80.2,
                79.95,
                80.7,
            ],
            "category": [
                "Nature",
                "Culture",
                "Hiking",
            ],
            "district": [
                "District B",
                "District A",
                "District C",
            ],
            "current_stage_score": [
                88.0,
                92.0,
                84.0,
            ],
            "recommended_duration_hours": [
                4.0,
                3.0,
                5.0,
            ],
            "distance_from_previous_km": [
                30.0,
                10.0,
                45.0,
            ],
            "route_order": [
                2,
                1,
                3,
            ],
        }
    )


def get_polylines(
    trip_map: folium.Map,
):
    return [
        child
        for child in trip_map._children.values()
        if isinstance(
            child,
            folium.vector_layers.PolyLine,
        )
    ]


def test_build_destination_map_returns_folium_map() -> None:
    trip_map = build_destination_map(
        make_destinations(),
        "Colombo",
    )

    assert isinstance(
        trip_map,
        folium.Map,
    )


def test_destination_map_rejects_missing_columns() -> None:
    destinations = pd.DataFrame(
        {
            "name": [
                "Test",
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="missing columns",
    ):
        build_destination_map(
            destinations
        )


def test_destination_map_rejects_empty_data() -> None:
    destinations = pd.DataFrame(
        columns=[
            "name",
            "latitude",
            "longitude",
        ]
    )

    with pytest.raises(
        ValueError,
        match="empty dataset",
    ):
        build_destination_map(
            destinations
        )


def test_destination_map_rejects_missing_coordinates() -> None:
    destinations = make_destinations()

    destinations.loc[
        0,
        "latitude",
    ] = None

    with pytest.raises(
        ValueError,
        match="cannot be missing",
    ):
        build_destination_map(
            destinations
        )


def test_destination_map_rejects_invalid_latitude() -> None:
    destinations = make_destinations()

    destinations.loc[
        0,
        "latitude",
    ] = 100.0

    with pytest.raises(
        ValueError,
        match="Latitude",
    ):
        build_destination_map(
            destinations
        )


def test_route_map_requires_route_order() -> None:
    route = (
        make_route()
        .drop(
            columns=[
                "route_order",
            ]
        )
    )

    with pytest.raises(
        ValueError,
        match="route_order",
    ):
        build_optimized_route_map(
            route,
            "Colombo",
        )


def test_route_order_must_be_unique() -> None:
    route = make_route()

    route[
        "route_order"
    ] = [
        1,
        1,
        2,
    ]

    with pytest.raises(
        ValueError,
        match="unique",
    ):
        build_optimized_route_map(
            route,
            "Colombo",
        )


def test_route_order_must_be_continuous() -> None:
    route = make_route()

    route[
        "route_order"
    ] = [
        1,
        2,
        4,
    ]

    with pytest.raises(
        ValueError,
        match="continuous sequence",
    ):
        build_optimized_route_map(
            route,
            "Colombo",
        )


def test_optimized_route_map_returns_folium_map() -> None:
    trip_map = build_optimized_route_map(
        make_route(),
        "Colombo",
    )

    assert isinstance(
        trip_map,
        folium.Map,
    )


def test_route_map_contains_one_polyline() -> None:
    trip_map = build_optimized_route_map(
        make_route(),
        "Colombo",
    )

    polylines = get_polylines(
        trip_map
    )

    assert len(polylines) == 1


def test_route_polyline_starts_at_starting_point() -> None:
    trip_map = build_optimized_route_map(
        make_route(),
        "Colombo",
    )

    polyline = get_polylines(
        trip_map
    )[0]

    first_point = (
        polyline.locations[
            0
        ]
    )

    assert first_point[
        0
    ] == pytest.approx(
        6.9271
    )

    assert first_point[
        1
    ] == pytest.approx(
        79.8612
    )


def test_route_polyline_follows_route_order() -> None:
    trip_map = build_optimized_route_map(
        make_route(),
        "Colombo",
    )

    polyline = get_polylines(
        trip_map
    )[0]

    locations = (
        polyline.locations
    )

    assert locations[
        1
    ][0] == pytest.approx(
        6.95
    )

    assert locations[
        2
    ][0] == pytest.approx(
        7.2
    )

    assert locations[
        3
    ][0] == pytest.approx(
        7.6
    )


def test_route_map_contains_numbered_stops_and_popups() -> None:
    trip_map = build_optimized_route_map(
        make_route(),
        "Colombo",
    )

    rendered_map = (
        trip_map
        .get_root()
        .render()
    )

    assert (
        rendered_map.count(
            "route-stop-number"
        )
        == 3
    )

    assert (
        "First Stop"
        in rendered_map
    )

    assert (
        "Second Stop"
        in rendered_map
    )

    assert (
        "Third Stop"
        in rendered_map
    )

    assert (
        "Route Stop: 1"
        in rendered_map
    )

    assert (
        "Route Stop: 2"
        in rendered_map
    )

    assert (
        "Route Stop: 3"
        in rendered_map
    )