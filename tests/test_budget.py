import pandas as pd
import pytest

from src.budget.estimator import (
    TRANSPORT_COST_PER_KM,
    TRAVEL_STYLE_FACTORS,
    calculate_destination_cost,
    calculate_transport_cost,
    estimate_trip_budget,
)


def make_itinerary() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": [
                "A",
                "B",
                "C",
            ],
            "scheduled": [
                True,
                True,
                False,
            ],
            "estimated_daily_cost_usd": [
                40.0,
                80.0,
                200.0,
            ],
            "recommended_duration_hours": [
                4.0,
                8.0,
                8.0,
            ],
            "distance_from_previous_km": [
                20.0,
                30.0,
                500.0,
            ],
        }
    )


def test_balanced_destination_cost() -> None:
    itinerary = make_itinerary()

    cost = calculate_destination_cost(
        itinerary,
        "Balanced",
    )

    # A: 40 * 4/8 = 20
    # B: 80 * 8/8 = 80
    # Total = 100
    assert cost == pytest.approx(
        100.0
    )


def test_budget_style_reduces_destination_cost() -> None:
    itinerary = make_itinerary()

    cost = calculate_destination_cost(
        itinerary,
        "Budget",
    )

    assert cost == pytest.approx(
        85.0
    )


def test_comfort_style_increases_destination_cost() -> None:
    itinerary = make_itinerary()

    cost = calculate_destination_cost(
        itinerary,
        "Comfort",
    )

    assert cost == pytest.approx(
        125.0
    )


def test_travel_style_cost_order() -> None:
    itinerary = make_itinerary()

    budget = calculate_destination_cost(
        itinerary,
        "Budget",
    )

    balanced = calculate_destination_cost(
        itinerary,
        "Balanced",
    )

    comfort = calculate_destination_cost(
        itinerary,
        "Comfort",
    )

    assert budget < balanced < comfort


def test_unscheduled_destination_is_excluded_from_cost() -> None:
    itinerary = make_itinerary()

    cost = calculate_destination_cost(
        itinerary,
        "Balanced",
    )

    assert cost == pytest.approx(
        100.0
    )


def test_public_transport_cost() -> None:
    itinerary = make_itinerary()

    cost = calculate_transport_cost(
        itinerary,
        "Public Transport",
    )

    # Only scheduled distance:
    # 20 + 30 = 50 km
    # 50 * 0.05 = 2.50
    assert cost == pytest.approx(
        2.50
    )


def test_mixed_transport_cost() -> None:
    itinerary = make_itinerary()

    cost = calculate_transport_cost(
        itinerary,
        "Mixed Transport",
    )

    assert cost == pytest.approx(
        6.00
    )


def test_private_vehicle_cost() -> None:
    itinerary = make_itinerary()

    cost = calculate_transport_cost(
        itinerary,
        "Private Vehicle",
    )

    assert cost == pytest.approx(
        11.00
    )


def test_transport_cost_order() -> None:
    itinerary = make_itinerary()

    public = calculate_transport_cost(
        itinerary,
        "Public Transport",
    )

    mixed = calculate_transport_cost(
        itinerary,
        "Mixed Transport",
    )

    private = calculate_transport_cost(
        itinerary,
        "Private Vehicle",
    )

    assert public < mixed < private


def test_budget_summary_within_budget() -> None:
    itinerary = make_itinerary()

    result = estimate_trip_budget(
        itinerary,
        total_budget_usd=200.0,
        travel_style="Balanced",
        transport="Public Transport",
    )

    assert result[
        "destination_cost_usd"
    ] == pytest.approx(100.0)

    assert result[
        "transport_cost_usd"
    ] == pytest.approx(2.50)

    assert result[
        "estimated_total_cost_usd"
    ] == pytest.approx(102.50)

    assert result[
        "budget_difference_usd"
    ] == pytest.approx(97.50)

    assert result[
        "within_budget"
    ] is True


def test_budget_summary_over_budget() -> None:
    itinerary = make_itinerary()

    result = estimate_trip_budget(
        itinerary,
        total_budget_usd=50.0,
        travel_style="Balanced",
        transport="Private Vehicle",
    )

    assert result[
        "estimated_total_cost_usd"
    ] == pytest.approx(111.0)

    assert result[
        "budget_difference_usd"
    ] == pytest.approx(-61.0)

    assert result[
        "within_budget"
    ] is False


def test_invalid_travel_style_is_rejected() -> None:
    itinerary = make_itinerary()

    with pytest.raises(
        ValueError,
        match="Unsupported travel style",
    ):
        calculate_destination_cost(
            itinerary,
            "Luxury",
        )


def test_invalid_transport_is_rejected() -> None:
    itinerary = make_itinerary()

    with pytest.raises(
        ValueError,
        match="Unsupported transport",
    ):
        calculate_transport_cost(
            itinerary,
            "Helicopter",
        )


def test_missing_destination_budget_columns_are_rejected() -> None:
    itinerary = pd.DataFrame(
        {
            "scheduled": [
                True,
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="missing budget columns",
    ):
        calculate_destination_cost(
            itinerary,
            "Balanced",
        )


def test_missing_distance_column_is_rejected() -> None:
    itinerary = pd.DataFrame(
        {
            "scheduled": [
                True,
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="distance_from_previous_km",
    ):
        calculate_transport_cost(
            itinerary,
            "Public Transport",
        )


def test_negative_destination_cost_is_rejected() -> None:
    itinerary = make_itinerary()

    itinerary.loc[
        0,
        "estimated_daily_cost_usd",
    ] = -20.0

    with pytest.raises(
        ValueError,
        match="cannot be negative",
    ):
        calculate_destination_cost(
            itinerary,
            "Balanced",
        )


def test_zero_destination_duration_is_rejected() -> None:
    itinerary = make_itinerary()

    itinerary.loc[
        0,
        "recommended_duration_hours",
    ] = 0.0

    with pytest.raises(
        ValueError,
        match="greater than 0",
    ):
        calculate_destination_cost(
            itinerary,
            "Balanced",
        )


def test_negative_travel_distance_is_rejected() -> None:
    itinerary = make_itinerary()

    itinerary.loc[
        0,
        "distance_from_previous_km",
    ] = -5.0

    with pytest.raises(
        ValueError,
        match="cannot be negative",
    ):
        calculate_transport_cost(
            itinerary,
            "Public Transport",
        )


def test_invalid_total_budget_is_rejected() -> None:
    itinerary = make_itinerary()

    with pytest.raises(
        ValueError,
        match="greater than 0",
    ):
        estimate_trip_budget(
            itinerary,
            total_budget_usd=0,
            travel_style="Balanced",
            transport="Public Transport",
        )


def test_empty_scheduled_itinerary_costs_zero() -> None:
    itinerary = pd.DataFrame(
        {
            "scheduled": [
                False,
            ],
            "estimated_daily_cost_usd": [
                50.0,
            ],
            "recommended_duration_hours": [
                4.0,
            ],
            "distance_from_previous_km": [
                100.0,
            ],
        }
    )

    assert (
        calculate_destination_cost(
            itinerary,
            "Balanced",
        )
        == 0.0
    )

    assert (
        calculate_transport_cost(
            itinerary,
            "Public Transport",
        )
        == 0.0
    )


def test_model_constants_are_positive() -> None:
    assert all(
        value > 0
        for value in TRAVEL_STYLE_FACTORS.values()
    )

    assert all(
        value > 0
        for value in TRANSPORT_COST_PER_KM.values()
    )