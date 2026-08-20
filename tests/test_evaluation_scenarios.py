from src.evaluation.scenarios import (
    EvaluationScenario,
    get_evaluation_scenarios,
)
from src.recommendation.traveller_profile import (
    TravellerProfile,
)


def test_evaluation_suite_contains_30_scenarios() -> None:
    scenarios = (
        get_evaluation_scenarios()
    )

    assert len(
        scenarios
    ) == 30


def test_all_scenario_ids_are_unique() -> None:
    scenarios = (
        get_evaluation_scenarios()
    )

    scenario_ids = [
        scenario.scenario_id
        for scenario in scenarios
    ]

    assert len(
        scenario_ids
    ) == len(
        set(
            scenario_ids
        )
    )


def test_scenario_ids_are_continuous() -> None:
    scenarios = (
        get_evaluation_scenarios()
    )

    expected_ids = [
        f"E{index:03d}"
        for index in range(
            1,
            31,
        )
    ]

    actual_ids = [
        scenario.scenario_id
        for scenario in scenarios
    ]

    assert (
        actual_ids
        == expected_ids
    )


def test_every_scenario_has_valid_profile() -> None:
    scenarios = (
        get_evaluation_scenarios()
    )

    for scenario in scenarios:
        assert isinstance(
            scenario,
            EvaluationScenario,
        )

        assert isinstance(
            scenario.profile,
            TravellerProfile,
        )

        assert (
            scenario.profile.trip_days
            >= 1
        )

        assert (
            scenario.profile.budget_usd
            > 0
        )

        assert (
            len(
                scenario.profile.interests
            )
            >= 1
        )


def test_all_starting_points_are_represented() -> None:
    scenarios = (
        get_evaluation_scenarios()
    )

    starting_points = {
        scenario.profile.starting_point
        for scenario in scenarios
    }

    assert starting_points == {
        "Colombo",
        "Kandy",
        "Galle",
        "Jaffna",
        "Negombo",
    }


def test_all_travel_styles_are_represented() -> None:
    scenarios = (
        get_evaluation_scenarios()
    )

    styles = {
        scenario.profile.travel_style
        for scenario in scenarios
    }

    assert styles == {
        "Budget",
        "Balanced",
        "Comfort",
    }


def test_all_crowd_preferences_are_represented() -> None:
    scenarios = (
        get_evaluation_scenarios()
    )

    crowd_preferences = {
        scenario.profile.crowd_preference
        for scenario in scenarios
    }

    assert crowd_preferences == {
        "No Preference",
        "Prefer Less Crowded Places",
        "Popular Tourist Places",
    }


def test_all_transport_modes_are_represented() -> None:
    scenarios = (
        get_evaluation_scenarios()
    )

    transport_modes = {
        scenario.profile.transport
        for scenario in scenarios
    }

    assert transport_modes == {
        "Public Transport",
        "Mixed Transport",
        "Private Vehicle",
    }


def test_all_interest_dimensions_are_represented() -> None:
    scenarios = (
        get_evaluation_scenarios()
    )

    interests = {
        interest
        for scenario in scenarios
        for interest in scenario.profile.interests
    }

    assert interests == {
        "Beach",
        "Wildlife",
        "Hiking",
        "Nature",
        "Culture",
        "History",
        "Adventure",
    }


def test_get_scenarios_returns_immutable_tuple() -> None:
    scenarios = (
        get_evaluation_scenarios()
    )

    assert isinstance(
        scenarios,
        tuple,
    )