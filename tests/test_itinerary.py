import pandas as pd
import pytest

from src.itinerary.planner import (
    generate_itinerary,
    itinerary_summary,
)


def make_route() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": [
                "Destination A",
                "Destination B",
                "Destination C",
            ],
            "route_order": [
                1,
                2,
                3,
            ],
            "recommended_duration_hours": [
                3.0,
                4.0,
                5.0,
            ],
        }
    )


def test_destinations_are_allocated_across_days() -> None:
    route = make_route()

    itinerary = generate_itinerary(
        route,
        trip_days=2,
    )

    assert itinerary["itinerary_day"].tolist() == [
        1,
        1,
        2,
    ]


def test_route_order_is_preserved() -> None:
    route = pd.DataFrame(
        {
            "name": [
                "Third",
                "First",
                "Second",
            ],
            "route_order": [
                3,
                1,
                2,
            ],
            "recommended_duration_hours": [
                2.0,
                2.0,
                2.0,
            ],
        }
    )

    itinerary = generate_itinerary(
        route,
        trip_days=2,
    )

    assert itinerary["name"].tolist() == [
        "First",
        "Second",
        "Third",
    ]


def test_daily_activity_limit_is_respected() -> None:
    route = make_route()

    itinerary = generate_itinerary(
        route,
        trip_days=3,
        daily_activity_hours=8.0,
    )

    scheduled = itinerary[
        itinerary["scheduled"]
    ]

    daily_totals = (
        scheduled.groupby("itinerary_day")[
            "recommended_duration_hours"
        ].sum()
    )

    assert (
        daily_totals <= 8.0
    ).all()


def test_exact_daily_limit_is_allowed() -> None:
    route = pd.DataFrame(
        {
            "name": [
                "A",
                "B",
            ],
            "route_order": [
                1,
                2,
            ],
            "recommended_duration_hours": [
                3.0,
                5.0,
            ],
        }
    )

    itinerary = generate_itinerary(
        route,
        trip_days=1,
        daily_activity_hours=8.0,
    )

    assert itinerary["scheduled"].tolist() == [
        True,
        True,
    ]

    assert itinerary["itinerary_day"].tolist() == [
        1,
        1,
    ]


def test_visit_order_resets_on_new_day() -> None:
    route = make_route()

    itinerary = generate_itinerary(
        route,
        trip_days=2,
    )

    assert (
        itinerary["visit_order_in_day"].tolist()
        == [
            1,
            2,
            1,
        ]
    )


def test_destinations_beyond_trip_duration_are_unscheduled() -> None:
    route = pd.DataFrame(
        {
            "name": [
                "A",
                "B",
                "C",
            ],
            "route_order": [
                1,
                2,
                3,
            ],
            "recommended_duration_hours": [
                8.0,
                8.0,
                8.0,
            ],
        }
    )

    itinerary = generate_itinerary(
        route,
        trip_days=2,
    )

    assert itinerary["scheduled"].tolist() == [
        True,
        True,
        False,
    ]

    assert pd.isna(
        itinerary.iloc[2]["itinerary_day"]
    )

    assert pd.isna(
        itinerary.iloc[2][
            "visit_order_in_day"
        ]
    )


def test_summary_reports_correct_values() -> None:
    route = pd.DataFrame(
        {
            "name": [
                "A",
                "B",
                "C",
            ],
            "route_order": [
                1,
                2,
                3,
            ],
            "recommended_duration_hours": [
                8.0,
                6.0,
                5.0,
            ],
        }
    )

    itinerary = generate_itinerary(
        route,
        trip_days=2,
    )

    summary = itinerary_summary(
        itinerary
    )

    assert summary == {
        "scheduled_destinations": 2,
        "unscheduled_destinations": 1,
        "days_used": 2,
        "total_activity_hours": 14.0,
    }


def test_invalid_trip_duration_is_rejected() -> None:
    route = make_route()

    with pytest.raises(
        ValueError,
        match="at least 1 day",
    ):
        generate_itinerary(
            route,
            trip_days=0,
        )


def test_invalid_daily_activity_hours_are_rejected() -> None:
    route = make_route()

    with pytest.raises(
        ValueError,
        match="greater than 0",
    ):
        generate_itinerary(
            route,
            trip_days=2,
            daily_activity_hours=0,
        )


def test_missing_itinerary_columns_are_rejected() -> None:
    route = pd.DataFrame(
        {
            "name": ["A"],
        }
    )

    with pytest.raises(
        ValueError,
        match="missing itinerary columns",
    ):
        generate_itinerary(
            route,
            trip_days=1,
        )


def test_zero_duration_is_rejected() -> None:
    route = pd.DataFrame(
        {
            "name": ["A"],
            "route_order": [1],
            "recommended_duration_hours": [0],
        }
    )

    with pytest.raises(
        ValueError,
        match="greater than 0",
    ):
        generate_itinerary(
            route,
            trip_days=1,
        )


def test_negative_duration_is_rejected() -> None:
    route = pd.DataFrame(
        {
            "name": ["A"],
            "route_order": [1],
            "recommended_duration_hours": [-2],
        }
    )

    with pytest.raises(
        ValueError,
        match="greater than 0",
    ):
        generate_itinerary(
            route,
            trip_days=1,
        )


def test_destination_longer_than_daily_limit_is_rejected() -> None:
    route = pd.DataFrame(
        {
            "name": ["A"],
            "route_order": [1],
            "recommended_duration_hours": [9.0],
        }
    )

    with pytest.raises(
        ValueError,
        match="more activity time",
    ):
        generate_itinerary(
            route,
            trip_days=2,
            daily_activity_hours=8.0,
        )


def test_empty_route_returns_empty_itinerary() -> None:
    route = pd.DataFrame(
        columns=[
            "name",
            "route_order",
            "recommended_duration_hours",
        ]
    )

    itinerary = generate_itinerary(
        route,
        trip_days=3,
    )

    assert itinerary.empty

    assert "itinerary_day" in itinerary.columns
    assert "visit_order_in_day" in itinerary.columns
    assert "scheduled" in itinerary.columns
    assert "day_activity_hours" in itinerary.columns


def test_empty_itinerary_summary() -> None:
    summary = itinerary_summary(
        pd.DataFrame()
    )

    assert summary == {
        "scheduled_destinations": 0,
        "unscheduled_destinations": 0,
        "days_used": 0,
        "total_activity_hours": 0.0,
    }


def test_original_route_is_not_modified() -> None:
    route = make_route()

    original = route.copy(
        deep=True
    )

    generate_itinerary(
        route,
        trip_days=2,
    )

    pd.testing.assert_frame_equal(
        route,
        original,
    )