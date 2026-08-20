from __future__ import annotations

from dataclasses import dataclass

from src.recommendation.traveller_profile import (
    TravellerProfile,
)


@dataclass(frozen=True)
class EvaluationScenario:
    """
    One reproducible traveller scenario used for
    quantitative CeylonCompass evaluation.

    segment is used only for grouping evaluation
    results. Recommendation behaviour is determined
    entirely by the TravellerProfile.
    """

    scenario_id: str

    segment: str

    description: str

    profile: TravellerProfile


def _make_scenario(
    scenario_id: str,
    segment: str,
    description: str,
    starting_point: str,
    trip_days: int,
    budget_usd: float,
    travel_style: str,
    crowd_preference: str,
    transport: str,
    interests: tuple[str, ...],
) -> EvaluationScenario:
    """
    Construct a validated evaluation scenario.
    """

    return EvaluationScenario(
        scenario_id=scenario_id,
        segment=segment,
        description=description,
        profile=TravellerProfile(
            starting_point=starting_point,
            trip_days=trip_days,
            budget_usd=budget_usd,
            travel_style=travel_style,
            crowd_preference=crowd_preference,
            transport=transport,
            interests=interests,
        ),
    )


EVALUATION_SCENARIOS = [
    _make_scenario(
        scenario_id="E001",
        segment="Beach",
        description="Budget beach traveller from Colombo",
        starting_point="Colombo",
        trip_days=4,
        budget_usd=180,
        travel_style="Budget",
        crowd_preference="Prefer Less Crowded Places",
        transport="Public Transport",
        interests=(
            "Beach",
            "Nature",
        ),
    ),
    _make_scenario(
        scenario_id="E002",
        segment="Beach",
        description="Popular coastal traveller from Galle",
        starting_point="Galle",
        trip_days=5,
        budget_usd=450,
        travel_style="Balanced",
        crowd_preference="Popular Tourist Places",
        transport="Mixed Transport",
        interests=(
            "Beach",
            "Adventure",
        ),
    ),
    _make_scenario(
        scenario_id="E003",
        segment="Beach",
        description="Comfort coastal trip from Negombo",
        starting_point="Negombo",
        trip_days=7,
        budget_usd=950,
        travel_style="Comfort",
        crowd_preference="No Preference",
        transport="Private Vehicle",
        interests=(
            "Beach",
            "Nature",
            "Culture",
        ),
    ),
    _make_scenario(
        scenario_id="E004",
        segment="Wildlife",
        description="Budget wildlife traveller from Colombo",
        starting_point="Colombo",
        trip_days=5,
        budget_usd=280,
        travel_style="Budget",
        crowd_preference="Prefer Less Crowded Places",
        transport="Public Transport",
        interests=(
            "Wildlife",
            "Nature",
        ),
    ),
    _make_scenario(
        scenario_id="E005",
        segment="Wildlife",
        description="Wildlife adventure traveller from Kandy",
        starting_point="Kandy",
        trip_days=6,
        budget_usd=600,
        travel_style="Balanced",
        crowd_preference="No Preference",
        transport="Mixed Transport",
        interests=(
            "Wildlife",
            "Adventure",
            "Nature",
        ),
    ),
    _make_scenario(
        scenario_id="E006",
        segment="Wildlife",
        description="Comfort wildlife traveller from Galle",
        starting_point="Galle",
        trip_days=8,
        budget_usd=1200,
        travel_style="Comfort",
        crowd_preference="Popular Tourist Places",
        transport="Private Vehicle",
        interests=(
            "Wildlife",
            "Nature",
        ),
    ),
    _make_scenario(
        scenario_id="E007",
        segment="Hiking",
        description="Budget hiking traveller from Kandy",
        starting_point="Kandy",
        trip_days=4,
        budget_usd=220,
        travel_style="Budget",
        crowd_preference="Prefer Less Crowded Places",
        transport="Public Transport",
        interests=(
            "Hiking",
            "Nature",
            "Adventure",
        ),
    ),
    _make_scenario(
        scenario_id="E008",
        segment="Hiking",
        description="Active hiking trip from Colombo",
        starting_point="Colombo",
        trip_days=6,
        budget_usd=500,
        travel_style="Balanced",
        crowd_preference="No Preference",
        transport="Mixed Transport",
        interests=(
            "Hiking",
            "Adventure",
        ),
    ),
    _make_scenario(
        scenario_id="E009",
        segment="Hiking",
        description="Comfort mountain trip from N/A start proxy Kandy",
        starting_point="Kandy",
        trip_days=9,
        budget_usd=1300,
        travel_style="Comfort",
        crowd_preference="Prefer Less Crowded Places",
        transport="Private Vehicle",
        interests=(
            "Hiking",
            "Nature",
        ),
    ),
    _make_scenario(
        scenario_id="E010",
        segment="Culture",
        description="Budget culture and history traveller from Jaffna",
        starting_point="Jaffna",
        trip_days=4,
        budget_usd=250,
        travel_style="Budget",
        crowd_preference="No Preference",
        transport="Public Transport",
        interests=(
            "Culture",
            "History",
        ),
    ),
    _make_scenario(
        scenario_id="E011",
        segment="Culture",
        description="Popular heritage traveller from Kandy",
        starting_point="Kandy",
        trip_days=5,
        budget_usd=500,
        travel_style="Balanced",
        crowd_preference="Popular Tourist Places",
        transport="Mixed Transport",
        interests=(
            "Culture",
            "History",
        ),
    ),
    _make_scenario(
        scenario_id="E012",
        segment="Culture",
        description="Comfort heritage tour from Colombo",
        starting_point="Colombo",
        trip_days=8,
        budget_usd=1100,
        travel_style="Comfort",
        crowd_preference="No Preference",
        transport="Private Vehicle",
        interests=(
            "Culture",
            "History",
            "Nature",
        ),
    ),
    _make_scenario(
        scenario_id="E013",
        segment="Adventure",
        description="Budget adventure traveller from Galle",
        starting_point="Galle",
        trip_days=4,
        budget_usd=240,
        travel_style="Budget",
        crowd_preference="Prefer Less Crowded Places",
        transport="Public Transport",
        interests=(
            "Adventure",
            "Hiking",
        ),
    ),
    _make_scenario(
        scenario_id="E014",
        segment="Adventure",
        description="Mixed adventure traveller from Negombo",
        starting_point="Negombo",
        trip_days=6,
        budget_usd=550,
        travel_style="Balanced",
        crowd_preference="No Preference",
        transport="Mixed Transport",
        interests=(
            "Adventure",
            "Nature",
            "Hiking",
        ),
    ),
    _make_scenario(
        scenario_id="E015",
        segment="Adventure",
        description="Comfort adventure traveller from Colombo",
        starting_point="Colombo",
        trip_days=8,
        budget_usd=1200,
        travel_style="Comfort",
        crowd_preference="Popular Tourist Places",
        transport="Private Vehicle",
        interests=(
            "Adventure",
            "Nature",
        ),
    ),
    _make_scenario(
        scenario_id="E016",
        segment="Nature",
        description="Low-cost nature traveller from Jaffna",
        starting_point="Jaffna",
        trip_days=5,
        budget_usd=300,
        travel_style="Budget",
        crowd_preference="Prefer Less Crowded Places",
        transport="Public Transport",
        interests=(
            "Nature",
        ),
    ),
    _make_scenario(
        scenario_id="E017",
        segment="Nature",
        description="Balanced nature traveller from Kandy",
        starting_point="Kandy",
        trip_days=7,
        budget_usd=650,
        travel_style="Balanced",
        crowd_preference="No Preference",
        transport="Mixed Transport",
        interests=(
            "Nature",
            "Wildlife",
        ),
    ),
    _make_scenario(
        scenario_id="E018",
        segment="Nature",
        description="Comfort nature traveller from Galle",
        starting_point="Galle",
        trip_days=10,
        budget_usd=1500,
        travel_style="Comfort",
        crowd_preference="Prefer Less Crowded Places",
        transport="Private Vehicle",
        interests=(
            "Nature",
            "Hiking",
            "Wildlife",
        ),
    ),
    _make_scenario(
        scenario_id="E019",
        segment="Mixed",
        description="Beach and culture traveller from Negombo",
        starting_point="Negombo",
        trip_days=5,
        budget_usd=420,
        travel_style="Balanced",
        crowd_preference="Popular Tourist Places",
        transport="Mixed Transport",
        interests=(
            "Beach",
            "Culture",
            "History",
        ),
    ),
    _make_scenario(
        scenario_id="E020",
        segment="Mixed",
        description="Wildlife and history traveller from Jaffna",
        starting_point="Jaffna",
        trip_days=7,
        budget_usd=700,
        travel_style="Balanced",
        crowd_preference="No Preference",
        transport="Private Vehicle",
        interests=(
            "Wildlife",
            "History",
            "Nature",
        ),
    ),
    _make_scenario(
        scenario_id="E021",
        segment="Mixed",
        description="Beach and wildlife traveller from Galle",
        starting_point="Galle",
        trip_days=6,
        budget_usd=480,
        travel_style="Budget",
        crowd_preference="Prefer Less Crowded Places",
        transport="Mixed Transport",
        interests=(
            "Beach",
            "Wildlife",
            "Nature",
        ),
    ),
    _make_scenario(
        scenario_id="E022",
        segment="Mixed",
        description="Culture and hiking traveller from Kandy",
        starting_point="Kandy",
        trip_days=6,
        budget_usd=520,
        travel_style="Balanced",
        crowd_preference="Popular Tourist Places",
        transport="Public Transport",
        interests=(
            "Culture",
            "Hiking",
            "History",
        ),
    ),
    _make_scenario(
        scenario_id="E023",
        segment="Mixed",
        description="Nature and beach comfort traveller from Negombo",
        starting_point="Negombo",
        trip_days=9,
        budget_usd=1250,
        travel_style="Comfort",
        crowd_preference="No Preference",
        transport="Private Vehicle",
        interests=(
            "Nature",
            "Beach",
            "Adventure",
        ),
    ),
    _make_scenario(
        scenario_id="E024",
        segment="Mixed",
        description="History and adventure traveller from Jaffna",
        starting_point="Jaffna",
        trip_days=5,
        budget_usd=380,
        travel_style="Budget",
        crowd_preference="Prefer Less Crowded Places",
        transport="Public Transport",
        interests=(
            "History",
            "Adventure",
            "Culture",
        ),
    ),
    _make_scenario(
        scenario_id="E025",
        segment="Short Trip",
        description="Two-day Colombo nature escape",
        starting_point="Colombo",
        trip_days=2,
        budget_usd=160,
        travel_style="Budget",
        crowd_preference="No Preference",
        transport="Public Transport",
        interests=(
            "Nature",
            "Culture",
        ),
    ),
    _make_scenario(
        scenario_id="E026",
        segment="Short Trip",
        description="Three-day Galle coastal escape",
        starting_point="Galle",
        trip_days=3,
        budget_usd=300,
        travel_style="Balanced",
        crowd_preference="Popular Tourist Places",
        transport="Mixed Transport",
        interests=(
            "Beach",
            "Adventure",
        ),
    ),
    _make_scenario(
        scenario_id="E027",
        segment="Short Trip",
        description="Three-day Jaffna heritage trip",
        starting_point="Jaffna",
        trip_days=3,
        budget_usd=260,
        travel_style="Budget",
        crowd_preference="Prefer Less Crowded Places",
        transport="Public Transport",
        interests=(
            "Culture",
            "History",
        ),
    ),
    _make_scenario(
        scenario_id="E028",
        segment="Long Trip",
        description="Extended island nature exploration from Negombo",
        starting_point="Negombo",
        trip_days=12,
        budget_usd=1400,
        travel_style="Balanced",
        crowd_preference="Prefer Less Crowded Places",
        transport="Private Vehicle",
        interests=(
            "Nature",
            "Wildlife",
            "Hiking",
            "Adventure",
        ),
    ),
    _make_scenario(
        scenario_id="E029",
        segment="Long Trip",
        description="Extended heritage and nature trip from Jaffna",
        starting_point="Jaffna",
        trip_days=14,
        budget_usd=1700,
        travel_style="Comfort",
        crowd_preference="No Preference",
        transport="Private Vehicle",
        interests=(
            "Culture",
            "History",
            "Nature",
        ),
    ),
    _make_scenario(
        scenario_id="E030",
        segment="Long Trip",
        description="Extended mixed-interest trip from Negombo",
        starting_point="Negombo",
        trip_days=14,
        budget_usd=1600,
        travel_style="Comfort",
        crowd_preference="Popular Tourist Places",
        transport="Private Vehicle",
        interests=(
            "Beach",
            "Wildlife",
            "Nature",
            "Culture",
            "Adventure",
        ),
    ),
]


def get_evaluation_scenarios() -> tuple[
    EvaluationScenario,
    ...,
]:
    """
    Return the fixed evaluation scenarios as an
    immutable tuple.
    """

    return tuple(
        EVALUATION_SCENARIOS
    )