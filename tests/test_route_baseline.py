import pandas as pd
import pytest

from src.optimization.route_baseline import (
    calculate_baseline_route_distance,
    get_starting_coordinates,
    nearest_neighbour_route,
)


def make_destinations() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": [
                "Kandy",
                "Galle",
                "Negombo",
            ],
            "latitude": [
                7.2906,
                6.0329,
                7.2083,
            ],
            "longitude": [
                80.6337,
                80.2168,
                79.8358,
            ],
        }
    )


def test_get_supported_starting_coordinates() -> None:
    coordinates = get_starting_coordinates(
        "Colombo"
    )

    assert coordinates == (
        6.9271,
        79.8612,
    )


def test_unsupported_starting_point_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Unsupported starting point",
    ):
        get_starting_coordinates(
            "Unknown City"
        )


def test_empty_destination_data_returns_empty_route() -> None:
    destinations = pd.DataFrame(
        columns=[
            "name",
            "latitude",
            "longitude",
        ]
    )

    result = nearest_neighbour_route(
        destinations,
        "Colombo",
    )

    assert result.empty


def test_missing_route_columns_are_rejected() -> None:
    destinations = pd.DataFrame(
        {
            "name": [
                "Kandy",
                "Galle",
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="missing route columns",
    ):
        nearest_neighbour_route(
            destinations,
            "Colombo",
        )


def test_route_contains_all_destinations_once() -> None:
    destinations = make_destinations()

    route = nearest_neighbour_route(
        destinations,
        "Colombo",
    )

    assert len(route) == len(destinations)

    assert set(route["name"]) == set(
        destinations["name"]
    )

    assert route["name"].is_unique


def test_route_order_starts_at_one_and_is_sequential() -> None:
    destinations = make_destinations()

    route = nearest_neighbour_route(
        destinations,
        "Colombo",
    )

    assert route["route_order"].tolist() == [
        1,
        2,
        3,
    ]


def test_nearest_destination_from_colombo_is_negombo() -> None:
    destinations = make_destinations()

    route = nearest_neighbour_route(
        destinations,
        "Colombo",
    )

    assert route.iloc[0]["name"] == "Negombo"


def test_distance_from_previous_is_non_negative() -> None:
    destinations = make_destinations()

    route = nearest_neighbour_route(
        destinations,
        "Colombo",
    )

    assert (
        route["distance_from_previous_km"]
        >= 0
    ).all()


def test_calculate_baseline_route_distance() -> None:
    destinations = make_destinations()

    route = nearest_neighbour_route(
        destinations,
        "Colombo",
    )

    total = calculate_baseline_route_distance(
        route
    )

    expected = route[
        "distance_from_previous_km"
    ].sum()

    assert total == pytest.approx(
        expected,
        abs=1e-9,
    )


def test_empty_route_distance_is_zero() -> None:
    route = pd.DataFrame()

    total = calculate_baseline_route_distance(
        route
    )

    assert total == 0.0


def test_missing_distance_column_is_rejected() -> None:
    route = pd.DataFrame(
        {
            "name": ["Kandy"],
        }
    )

    with pytest.raises(
        ValueError,
        match="distance_from_previous_km",
    ):
        calculate_baseline_route_distance(
            route
        )


def test_original_dataframe_is_not_modified() -> None:
    destinations = make_destinations()

    original = destinations.copy(
        deep=True
    )

    nearest_neighbour_route(
        destinations,
        "Colombo",
    )

    pd.testing.assert_frame_equal(
        destinations,
        original,
    )