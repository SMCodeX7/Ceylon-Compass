import numpy as np
import pandas as pd
import pytest

from src.optimization.distance import (
    build_distance_matrix,
    calculate_route_distance,
    haversine_distance,
)


def test_same_location_distance_is_zero() -> None:
    distance = haversine_distance(
        6.9271,
        79.8612,
        6.9271,
        79.8612,
    )

    assert distance == pytest.approx(
        0.0,
        abs=1e-9,
    )


def test_colombo_to_kandy_distance() -> None:
    distance = haversine_distance(
        6.9271,
        79.8612,
        7.2906,
        80.6337,
    )

    assert distance == pytest.approx(
        94.34,
        abs=0.5,
    )


def test_distance_is_symmetric() -> None:
    forward = haversine_distance(
        6.9271,
        79.8612,
        7.2906,
        80.6337,
    )

    backward = haversine_distance(
        7.2906,
        80.6337,
        6.9271,
        79.8612,
    )

    assert forward == pytest.approx(
        backward,
        abs=1e-9,
    )


def test_distance_matrix_shape() -> None:
    destinations = pd.DataFrame(
        {
            "latitude": [
                6.9271,
                7.2906,
                6.0329,
            ],
            "longitude": [
                79.8612,
                80.6337,
                80.2168,
            ],
        }
    )

    matrix = build_distance_matrix(
        destinations
    )

    assert matrix.shape == (3, 3)


def test_distance_matrix_diagonal_is_zero() -> None:
    destinations = pd.DataFrame(
        {
            "latitude": [
                6.9271,
                7.2906,
                6.0329,
            ],
            "longitude": [
                79.8612,
                80.6337,
                80.2168,
            ],
        }
    )

    matrix = build_distance_matrix(
        destinations
    )

    assert np.allclose(
        np.diag(matrix),
        0.0,
    )


def test_distance_matrix_is_symmetric() -> None:
    destinations = pd.DataFrame(
        {
            "latitude": [
                6.9271,
                7.2906,
                6.0329,
            ],
            "longitude": [
                79.8612,
                80.6337,
                80.2168,
            ],
        }
    )

    matrix = build_distance_matrix(
        destinations
    )

    assert np.allclose(
        matrix,
        matrix.T,
    )


def test_missing_geographic_columns_are_rejected() -> None:
    destinations = pd.DataFrame(
        {
            "name": [
                "Colombo",
                "Kandy",
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="missing geographic columns",
    ):
        build_distance_matrix(
            destinations
        )


def test_single_destination_route_distance_is_zero() -> None:
    destinations = pd.DataFrame(
        {
            "latitude": [6.9271],
            "longitude": [79.8612],
        }
    )

    distance = calculate_route_distance(
        destinations
    )

    assert distance == 0.0


def test_route_distance_matches_segment_sum() -> None:
    destinations = pd.DataFrame(
        {
            "latitude": [
                6.9271,
                7.2906,
                6.0329,
            ],
            "longitude": [
                79.8612,
                80.6337,
                80.2168,
            ],
        }
    )

    route_distance = calculate_route_distance(
        destinations
    )

    expected = (
        haversine_distance(
            6.9271,
            79.8612,
            7.2906,
            80.6337,
        )
        + haversine_distance(
            7.2906,
            80.6337,
            6.0329,
            80.2168,
        )
    )

    assert route_distance == pytest.approx(
        expected,
        abs=1e-9,
    )