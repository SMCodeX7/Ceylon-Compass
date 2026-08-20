import pandas as pd
import pytest

from src.optimization.route_optimizer import (
    build_optimizer_distance_matrix,
    calculate_optimized_route_distance,
    optimize_route,
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


def test_optimizer_matrix_size() -> None:
    destinations = make_destinations()

    matrix = build_optimizer_distance_matrix(
        destinations,
        "Colombo",
    )

    # Start node + 3 destinations + dummy end.
    assert len(matrix) == 5

    assert all(
        len(row) == 5
        for row in matrix
    )


def test_optimizer_matrix_diagonal_is_zero() -> None:
    destinations = make_destinations()

    matrix = build_optimizer_distance_matrix(
        destinations,
        "Colombo",
    )

    for index in range(len(matrix)):
        assert matrix[index][index] == 0


def test_dummy_end_has_zero_incoming_cost() -> None:
    destinations = make_destinations()

    matrix = build_optimizer_distance_matrix(
        destinations,
        "Colombo",
    )

    dummy_end = len(matrix) - 1

    for row in matrix:
        assert row[dummy_end] == 0


def test_missing_optimizer_columns_are_rejected() -> None:
    destinations = pd.DataFrame(
        {
            "name": ["Kandy"],
        }
    )

    with pytest.raises(
        ValueError,
        match="missing route columns",
    ):
        build_optimizer_distance_matrix(
            destinations,
            "Colombo",
        )


def test_empty_destinations_return_empty_route() -> None:
    destinations = pd.DataFrame(
        columns=[
            "name",
            "latitude",
            "longitude",
        ]
    )

    route = optimize_route(
        destinations,
        "Colombo",
    )

    assert route.empty


def test_optimized_route_contains_all_destinations() -> None:
    destinations = make_destinations()

    route = optimize_route(
        destinations,
        "Colombo",
    )

    assert len(route) == len(destinations)

    assert set(route["name"]) == set(
        destinations["name"]
    )


def test_optimized_route_has_unique_destinations() -> None:
    destinations = make_destinations()

    route = optimize_route(
        destinations,
        "Colombo",
    )

    assert route["name"].is_unique


def test_optimized_route_order_is_sequential() -> None:
    destinations = make_destinations()

    route = optimize_route(
        destinations,
        "Colombo",
    )

    assert route["route_order"].tolist() == [
        1,
        2,
        3,
    ]


def test_segment_distances_are_non_negative() -> None:
    destinations = make_destinations()

    route = optimize_route(
        destinations,
        "Colombo",
    )

    assert (
        route["distance_from_previous_km"]
        >= 0
    ).all()


def test_calculate_optimized_distance() -> None:
    destinations = make_destinations()

    route = optimize_route(
        destinations,
        "Colombo",
    )

    total = calculate_optimized_route_distance(
        route
    )

    expected = route[
        "distance_from_previous_km"
    ].sum()

    assert total == pytest.approx(
        expected,
        abs=1e-9,
    )


def test_empty_optimized_route_distance_is_zero() -> None:
    assert (
        calculate_optimized_route_distance(
            pd.DataFrame()
        )
        == 0.0
    )


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
        calculate_optimized_route_distance(
            route
        )


def test_original_dataframe_is_not_modified() -> None:
    destinations = make_destinations()

    original = destinations.copy(
        deep=True
    )

    optimize_route(
        destinations,
        "Colombo",
    )

    pd.testing.assert_frame_equal(
        destinations,
        original,
    )