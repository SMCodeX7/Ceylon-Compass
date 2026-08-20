import streamlit as st
from streamlit_folium import st_folium

from src.budget.estimator import (
    TRANSPORT_COST_PER_KM,
    TRAVEL_STYLE_FACTORS,
)
from src.planning.service import (
    TripPlan,
    generate_trip_plan,
)
from src.recommendation.explanations import (
    explain_destination,
)
from src.recommendation.final_scoring import (
    BUDGET_WEIGHT,
    CROWD_WEIGHT,
    PREFERENCE_WEIGHT,
    ROUTE_EFFICIENCY_WEIGHT,
    WEATHER_WEIGHT,
)
from src.recommendation.traveller_profile import (
    TravellerProfile,
)
from src.visualization.map_builder import (
    build_optimized_route_map,
)
from src.weather.client import (
    fetch_weather_forecast,
)
from src.weather.scoring import (
    weather_suitability_label,
)


WEATHER_CACHE_TTL_SECONDS = 1800


st.set_page_config(
    page_title="CeylonCompass",
    page_icon="\U0001F1F1\U0001F1F0",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(
    ttl=WEATHER_CACHE_TTL_SECONDS,
    show_spinner=False,
)
def get_cached_weather_forecast(
    latitude: float,
    longitude: float,
    forecast_days: int,
):
    """
    Retrieve and temporarily cache Open-Meteo
    forecast data.

    The unified planning service receives this
    function as its weather provider.
    """

    return fetch_weather_forecast(
        latitude=latitude,
        longitude=longitude,
        forecast_days=forecast_days,
    )


def display_scoring_methodology() -> None:
    """
    Explain the final weighted recommendation model.
    """

    with st.expander(
        "How the final recommendation score works"
    ):
        st.markdown(
            "### Final CeylonCompass Ranking Model"
        )

        st.write(
            f"- **Preference Similarity:** "
            f"{PREFERENCE_WEIGHT * 100:.0f}%"
        )

        st.write(
            f"- **Budget Compatibility:** "
            f"{BUDGET_WEIGHT * 100:.0f}%"
        )

        st.write(
            f"- **Weather Suitability:** "
            f"{WEATHER_WEIGHT * 100:.0f}%"
        )

        st.write(
            f"- **Crowd Compatibility:** "
            f"{CROWD_WEIGHT * 100:.0f}%"
        )

        st.write(
            f"- **Route Efficiency:** "
            f"{ROUTE_EFFICIENCY_WEIGHT * 100:.0f}%"
        )

        st.info(
            "If live weather is unavailable for a "
            "destination, the weather component is "
            "excluded and the remaining active weights "
            "are normalized."
        )

        st.info(
            "If Crowd Preference is set to "
            "'No Preference', the crowd component is "
            "excluded instead of artificially rewarding "
            "every destination."
        )

        st.caption(
            "Route efficiency is currently a geographic "
            "candidate-selection proxy based on distance "
            "from the starting point and relative "
            "proximity to the candidate cluster. "
            "It is not road-routing distance."
        )


def display_recommendations(
    plan: TripPlan,
) -> None:
    """
    Display final destination recommendations produced
    by the unified planning service.
    """

    recommendations = (
        plan.recommendations
    )

    st.header(
        "Final Destination Recommendations"
    )

    st.caption(
        "Destinations are ranked using traveller "
        "preferences, budget compatibility, live weather, "
        "crowd preference when selected, and geographic "
        "route-efficiency information."
    )

    display_scoring_methodology()

    display_df = recommendations[
        [
            "final_recommendation_rank",
            "name",
            "category",
            "estimated_daily_cost_usd",
            "preference_score",
            "budget_score",
            "ranking_weather_score",
            "crowd_score",
            "route_efficiency_score",
            "final_score",
        ]
    ].copy()

    display_df.columns = [
        "Rank",
        "Destination",
        "Category",
        "Daily Cost (USD)",
        "Interest Match",
        "Budget Match",
        "Weather",
        "Crowd Match",
        "Route Efficiency",
        "Final Score",
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader(
        "Recommendation Details"
    )

    for _, destination in (
        recommendations
        .head(5)
        .iterrows()
    ):
        explanation = explain_destination(
            destination,
            plan.profile,
        )

        rank = int(
            destination[
                "final_recommendation_rank"
            ]
        )

        final_score = float(
            destination[
                "final_score"
            ]
        )

        with st.expander(
            f"#{rank} "
            f"{destination['name']} "
            f"— {final_score:.2f}%"
        ):
            col1, col2, col3, col4, col5 = (
                st.columns(5)
            )

            col1.metric(
                "Interest",
                (
                    f"{float(destination['preference_score']):.1f}%"
                ),
            )

            col2.metric(
                "Budget",
                (
                    f"{float(destination['budget_score']):.1f}%"
                ),
            )

            if bool(
                destination[
                    "weather_component_active"
                ]
            ):
                col3.metric(
                    "Weather",
                    (
                        f"{float(destination['ranking_weather_score']):.1f}%"
                    ),
                )
            else:
                col3.metric(
                    "Weather",
                    "Unavailable",
                )

            col4.metric(
                "Route Efficiency",
                (
                    f"{float(destination['route_efficiency_score']):.1f}%"
                ),
            )

            col5.metric(
                "Final Score",
                f"{final_score:.1f}%",
            )

            st.divider()

            if bool(
                destination[
                    "crowd_component_active"
                ]
            ):
                st.write(
                    f"**Crowd Compatibility:** "
                    f"{float(destination['crowd_score']):.1f}%"
                )
            else:
                st.write(
                    "**Crowd Compatibility:** "
                    "Excluded — no crowd preference selected"
                )

            st.write(
                f"**Category:** "
                f"{destination['category']}"
            )

            st.write(
                f"**Location:** "
                f"{destination['district']} District, "
                f"{destination['province']} Province"
            )

            st.write(
                f"**Estimated Daily Cost:** "
                f"${float(destination['estimated_daily_cost_usd']):.0f}"
            )

            st.write(
                f"**Recommended Visit Duration:** "
                f"{float(destination['recommended_duration_hours']):.0f} "
                f"hours"
            )

            st.write(
                f"**Distance From Starting Point:** "
                f"{float(destination['distance_from_start_km']):.1f} km"
            )

            if bool(
                destination[
                    "weather_component_active"
                ]
            ):
                st.write(
                    f"**Forecast Suitability:** "
                    f"{destination['ranking_weather_suitability']}"
                )
            else:
                st.write(
                    "**Forecast Suitability:** "
                    "Live weather unavailable"
                )

            st.divider()

            st.markdown(
                "### Why this destination matches you"
            )

            for reason in explanation[
                "reasons"
            ]:
                st.write(
                    f"- {reason}"
                )

            if explanation[
                "tradeoffs"
            ]:
                st.markdown(
                    "### Trade-offs to consider"
                )

                for tradeoff in explanation[
                    "tradeoffs"
                ]:
                    st.write(
                        f"- {tradeoff}"
                    )

            st.divider()

            st.markdown(
                "### Active Score Weights"
            )

            weight_col1, weight_col2, weight_col3 = (
                st.columns(3)
            )

            weight_col1.write(
                f"Preference: "
                f"{float(destination['preference_weight_used']) * 100:.0f}%"
            )

            weight_col1.write(
                f"Budget: "
                f"{float(destination['budget_weight_used']) * 100:.0f}%"
            )

            weight_col2.write(
                f"Weather: "
                f"{float(destination['weather_weight_used']) * 100:.0f}%"
            )

            weight_col2.write(
                f"Crowd: "
                f"{float(destination['crowd_weight_used']) * 100:.0f}%"
            )

            weight_col3.write(
                f"Route Efficiency: "
                f"{float(destination['route_efficiency_weight_used']) * 100:.0f}%"
            )

            weight_col3.write(
                f"Active Weight Total: "
                f"{float(destination['active_weight_total']) * 100:.0f}%"
            )


def display_interactive_route_map(
    plan: TripPlan,
) -> None:
    """
    Display the optimized route using Folium and
    OpenStreetMap.
    """

    st.divider()

    st.header(
        "Interactive Trip Map"
    )

    st.caption(
        "The green marker is your starting location. "
        "Numbered markers show the optimized visit "
        "sequence."
    )

    route_map = (
        build_optimized_route_map(
            plan.optimized_route,
            plan.profile.starting_point,
        )
    )

    st_folium(
        route_map,
        height=560,
        use_container_width=True,
        returned_objects=[],
    )

    st.info(
        "The route line connects geographic coordinates "
        "in optimized visit order. It does not represent "
        "turn-by-turn road navigation."
    )

    st.caption(
        "Base map data: OpenStreetMap contributors."
    )


def display_route(
    plan: TripPlan,
) -> None:
    """
    Display optimized route information.
    """

    st.divider()

    st.header(
        "Optimized Trip Route"
    )

    summary = (
        plan.itinerary_summary
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    col1.metric(
        "Route Destinations",
        len(
            plan.optimized_route
        ),
    )

    col2.metric(
        "Route Distance",
        (
            f"{plan.optimized_route_distance_km:.1f} km"
        ),
    )

    col3.metric(
        "Scheduled Places",
        summary[
            "scheduled_destinations"
        ],
    )

    col4.metric(
        "Days Used",
        summary[
            "days_used"
        ],
    )

    st.caption(
        "Distance currently uses Haversine "
        "great-circle distance between coordinates. "
        "It is a geographic proxy rather than "
        "driving-road distance."
    )

    route_names = (
        plan.optimized_route[
            "name"
        ]
        .astype(str)
        .tolist()
    )

    if (
        route_names
        and route_names[
            0
        ].casefold()
        == plan.profile.starting_point.casefold()
    ):
        route_text = (
            " → ".join(
                route_names
            )
        )
    else:
        route_text = (
            plan.profile.starting_point
            + " → "
            + " → ".join(
                route_names
            )
        )

    st.markdown(
        "### Recommended Visit Order"
    )

    st.write(
        route_text
    )

    route_display = (
        plan.optimized_route[
            [
                "route_order",
                "name",
                "district",
                "category",
                "distance_from_previous_km",
                "final_score",
            ]
        ].copy()
    )

    route_display.columns = [
        "Route Order",
        "Destination",
        "District",
        "Category",
        "Distance From Previous (km)",
        "Final Recommendation Score",
    ]

    st.dataframe(
        route_display,
        use_container_width=True,
        hide_index=True,
    )

    display_interactive_route_map(
        plan
    )


def display_itinerary(
    plan: TripPlan,
) -> None:
    """
    Display the generated day-by-day itinerary.
    """

    st.divider()

    st.header(
        "Day-by-Day Itinerary"
    )

    itinerary = (
        plan.itinerary
    )

    summary = (
        plan.itinerary_summary
    )

    col1, col2, col3 = (
        st.columns(3)
    )

    col1.metric(
        "Scheduled Destinations",
        summary[
            "scheduled_destinations"
        ],
    )

    col2.metric(
        "Total Activity Time",
        (
            f"{summary['total_activity_hours']:.1f} "
            f"hours"
        ),
    )

    col3.metric(
        "Unscheduled Destinations",
        summary[
            "unscheduled_destinations"
        ],
    )

    scheduled = itinerary[
        itinerary[
            "scheduled"
        ]
    ].copy()

    if scheduled.empty:
        st.warning(
            "No destinations could be scheduled "
            "within the selected trip duration."
        )

    else:
        itinerary_days = sorted(
            scheduled[
                "itinerary_day"
            ]
            .dropna()
            .unique()
        )

        for day in itinerary_days:
            day_number = int(
                day
            )

            day_plan = (
                scheduled[
                    scheduled[
                        "itinerary_day"
                    ]
                    == day
                ]
                .sort_values(
                    "visit_order_in_day"
                )
            )

            day_hours = float(
                day_plan[
                    "recommended_duration_hours"
                ].sum()
            )

            with st.expander(
                (
                    f"Day {day_number} "
                    f"— {day_hours:.1f} activity hours"
                ),
                expanded=True,
            ):
                for _, destination in (
                    day_plan.iterrows()
                ):
                    st.markdown(
                        f"### "
                        f"{int(destination['visit_order_in_day'])}. "
                        f"{destination['name']}"
                    )

                    detail_col1, detail_col2, detail_col3 = (
                        st.columns(3)
                    )

                    detail_col1.write(
                        f"**Category:** "
                        f"{destination['category']}"
                    )

                    detail_col2.write(
                        f"**Visit Duration:** "
                        f"{float(destination['recommended_duration_hours']):.0f} "
                        f"hours"
                    )

                    detail_col3.write(
                        f"**Travel Distance:** "
                        f"{float(destination['distance_from_previous_km']):.1f} "
                        f"km"
                    )

                    st.write(
                        f"**Location:** "
                        f"{destination['district']} District, "
                        f"{destination['province']} Province"
                    )

                    if bool(
                        destination[
                            "weather_available"
                        ]
                    ):
                        weather_col1, weather_col2 = (
                            st.columns(2)
                        )

                        weather_col1.write(
                            f"**Weather:** "
                            f"{destination['weather_description']}"
                        )

                        weather_col1.write(
                            f"**Forecast Date:** "
                            f"{destination['weather_date']}"
                        )

                        weather_col2.write(
                            f"**Weather Suitability:** "
                            f"{float(destination['weather_score']):.1f}% "
                            f"({destination['weather_suitability']})"
                        )

                        weather_col2.write(
                            f"**Rain Probability:** "
                            f"{float(destination['weather_rain_probability']):.0f}%"
                        )
                    else:
                        st.caption(
                            "Live weather is unavailable "
                            "for this itinerary stop."
                        )

                    st.divider()

    unscheduled = itinerary[
        ~itinerary[
            "scheduled"
        ]
    ].copy()

    if not unscheduled.empty:
        st.warning(
            f"{len(unscheduled)} destination(s) could "
            f"not fit within the selected "
            f"{plan.profile.trip_days}-day trip while "
            f"respecting the current 8-hour daily "
            f"activity limit."
        )

        unscheduled_display = (
            unscheduled[
                [
                    "name",
                    "category",
                    "recommended_duration_hours",
                    "final_score",
                ]
            ].copy()
        )

        unscheduled_display.columns = [
            "Destination",
            "Category",
            "Required Activity Hours",
            "Final Score",
        ]

        st.dataframe(
            unscheduled_display,
            use_container_width=True,
            hide_index=True,
        )

    st.caption(
        "The current 8-hour daily limit applies to "
        "destination activity time only. Travel time "
        "is not yet included in the daily-hour limit."
    )


def display_weather_intelligence(
    plan: TripPlan,
) -> None:
    """
    Display itinerary-day weather already retrieved
    by the unified planning pipeline.
    """

    st.divider()

    st.header(
        "Live Weather Intelligence"
    )

    st.caption(
        "Candidate ranking uses average forecast "
        "suitability across the available trip horizon. "
        "The itinerary below uses the specific forecast "
        "for the day each destination is scheduled."
    )

    scheduled = (
        plan.itinerary[
            plan.itinerary[
                "scheduled"
            ]
        ].copy()
    )

    available = (
        scheduled[
            scheduled[
                "weather_available"
            ]
        ].copy()
    )

    if available.empty:
        st.warning(
            "Live weather could not be retrieved for "
            "the scheduled destinations. Other planning "
            "components remain available."
        )

        return

    average_score = float(
        available[
            "weather_score"
        ]
        .astype(float)
        .mean()
    )

    overall_label = (
        weather_suitability_label(
            average_score
        )
    )

    best_index = (
        available[
            "weather_score"
        ]
        .astype(float)
        .idxmax()
    )

    best_destination = (
        available.loc[
            best_index
        ]
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    col1.metric(
        "Itinerary Coverage",
        (
            f"{len(available)}/"
            f"{len(scheduled)} places"
        ),
    )

    col2.metric(
        "Average Weather Score",
        f"{average_score:.1f}%",
    )

    col3.metric(
        "Overall Suitability",
        overall_label,
    )

    col4.metric(
        "Best Weather Stop",
        best_destination[
            "name"
        ],
    )

    if (
        plan.weather_failure_count
        > 0
    ):
        st.warning(
            f"Live forecast retrieval failed for "
            f"{plan.weather_failure_count} candidate "
            f"destination(s). Their weather weight was "
            f"automatically excluded from final ranking."
        )

    weather_display = (
        available[
            [
                "itinerary_day",
                "name",
                "weather_date",
                "weather_description",
                "weather_temperature_max_c",
                "weather_temperature_min_c",
                "weather_rain_probability",
                "weather_precipitation_mm",
                "weather_score",
                "weather_suitability",
            ]
        ].copy()
    )

    weather_display.columns = [
        "Day",
        "Destination",
        "Forecast Date",
        "Condition",
        "Max Temp (°C)",
        "Min Temp (°C)",
        "Rain Probability (%)",
        "Rainfall (mm)",
        "Weather Score",
        "Suitability",
    ]

    st.dataframe(
        weather_display,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Weather data: Open-Meteo. Forecasts can "
        "change and should be rechecked close to "
        "travel time."
    )

    st.caption(
        "CeylonCompass currently assumes the trip "
        "starts within the current forecast horizon. "
        "A user-selected future travel start date is "
        "not yet implemented."
    )


def display_budget_breakdown(
    plan: TripPlan,
) -> None:
    """
    Display the budget already calculated by the
    unified planning service.
    """

    budget = (
        plan.budget
    )

    profile = (
        plan.profile
    )

    st.divider()

    st.header(
        "Estimated Trip Budget"
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    col1.metric(
        "Available Budget",
        (
            f"${budget['total_budget_usd']:.2f}"
        ),
    )

    col2.metric(
        "Destination Cost",
        (
            f"${budget['destination_cost_usd']:.2f}"
        ),
    )

    col3.metric(
        "Transport Cost",
        (
            f"${budget['transport_cost_usd']:.2f}"
        ),
    )

    col4.metric(
        "Estimated Total",
        (
            f"${budget['estimated_total_cost_usd']:.2f}"
        ),
    )

    budget_used_percent = (
        budget[
            "estimated_total_cost_usd"
        ]
        / budget[
            "total_budget_usd"
        ]
        * 100
    )

    st.write(
        f"**Estimated Budget Used:** "
        f"{budget_used_percent:.1f}%"
    )

    st.progress(
        min(
            budget_used_percent
            / 100.0,
            1.0,
        )
    )

    if budget[
        "within_budget"
    ]:
        st.success(
            f"Estimated trip cost is within budget. "
            f"Approximately "
            f"${budget['budget_difference_usd']:.2f} "
            f"remains available."
        )
    else:
        amount_over = abs(
            budget[
                "budget_difference_usd"
            ]
        )

        st.error(
            f"Estimated trip cost exceeds the "
            f"selected budget by approximately "
            f"${amount_over:.2f}."
        )

    style_factor = (
        TRAVEL_STYLE_FACTORS[
            profile.travel_style
        ]
    )

    transport_rate = (
        TRANSPORT_COST_PER_KM[
            profile.transport
        ]
    )

    with st.expander(
        "How this budget estimate is calculated"
    ):
        st.write(
            f"**Travel Style:** "
            f"{profile.travel_style}"
        )

        st.write(
            f"**Travel Style Cost Factor:** "
            f"{style_factor:.2f}"
        )

        st.write(
            f"**Transport:** "
            f"{profile.transport}"
        )

        st.write(
            f"**Transport Cost Assumption:** "
            f"${transport_rate:.2f} per km"
        )

        st.write(
            "Destination cost uses each destination's "
            "estimated daily cost, recommended activity "
            "duration, and selected travel-style factor."
        )

        st.write(
            "Transport cost uses the Haversine route "
            "distance proxy multiplied by the selected "
            "transport-rate assumption."
        )

        st.warning(
            "These are transparent V1 modelling "
            "assumptions rather than guaranteed current "
            "Sri Lankan market prices."
        )

        st.caption(
            "International flights, visas, insurance, "
            "shopping and other personal spending are "
            "not included."
        )


def display_trip_plan(
    plan: TripPlan,
) -> None:
    """
    Render all outputs from one unified TripPlan.
    """

    display_recommendations(
        plan
    )

    display_route(
        plan
    )

    display_itinerary(
        plan
    )

    display_weather_intelligence(
        plan
    )

    display_budget_breakdown(
        plan
    )


def main() -> None:
    st.title(
        "\U0001F1F1\U0001F1F0 CeylonCompass"
    )

    st.subheader(
        "Smart Sri Lanka Travel Recommendation "
        "& Route Optimization"
    )

    st.write(
        """
        Generate a personalized Sri Lankan journey
        using traveller interests, budget, travel style,
        crowd preference, live weather intelligence,
        geographic route efficiency and OR-Tools route
        optimization.
        """
    )

    st.info(
        "CeylonCompass V1 uses one integrated planning "
        "pipeline for recommendation, weather-aware "
        "ranking, route optimization, itinerary "
        "scheduling, interactive mapping and budget "
        "estimation."
    )

    st.divider()

    st.header(
        "Plan Your Trip"
    )

    col1, col2 = (
        st.columns(2)
    )

    with col1:
        starting_point = (
            st.selectbox(
                "Starting Point",
                [
                    "Colombo",
                    "Kandy",
                    "Galle",
                    "Jaffna",
                    "Negombo",
                ],
            )
        )

        trip_days = (
            st.slider(
                "Trip Duration (Days)",
                min_value=1,
                max_value=14,
                value=5,
            )
        )

        budget = (
            st.number_input(
                "Total Budget (USD)",
                min_value=50,
                max_value=5000,
                value=500,
                step=50,
            )
        )

    with col2:
        travel_style = (
            st.selectbox(
                "Travel Style",
                [
                    "Budget",
                    "Balanced",
                    "Comfort",
                ],
            )
        )

        crowd_preference = (
            st.selectbox(
                "Crowd Preference",
                [
                    "No Preference",
                    "Prefer Less Crowded Places",
                    "Popular Tourist Places",
                ],
            )
        )

        transport = (
            st.selectbox(
                "Preferred Transport",
                [
                    "Public Transport",
                    "Mixed Transport",
                    "Private Vehicle",
                ],
            )
        )

    st.subheader(
        "Your Interests"
    )

    interests = (
        st.multiselect(
            "Select one or more interests",
            [
                "Beach",
                "Wildlife",
                "Hiking",
                "Nature",
                "Culture",
                "History",
                "Adventure",
            ],
            default=[
                "Nature",
            ],
        )
    )

    st.divider()

    if st.button(
        "Generate Smart Trip",
        type="primary",
        use_container_width=True,
    ):
        if not interests:
            st.warning(
                "Please select at least one "
                "travel interest."
            )

            return

        try:
            profile = (
                TravellerProfile(
                    starting_point=(
                        starting_point
                    ),
                    trip_days=(
                        trip_days
                    ),
                    budget_usd=float(
                        budget
                    ),
                    travel_style=(
                        travel_style
                    ),
                    crowd_preference=(
                        crowd_preference
                    ),
                    transport=(
                        transport
                    ),
                    interests=tuple(
                        interests
                    ),
                )
            )

            st.success(
                "Traveller profile processed "
                "successfully."
            )

            st.subheader(
                "Traveller Profile"
            )

            profile_col1, profile_col2, profile_col3 = (
                st.columns(3)
            )

            profile_col1.metric(
                "Trip Duration",
                (
                    f"{profile.trip_days} days"
                ),
            )

            profile_col2.metric(
                "Total Budget",
                (
                    f"${profile.budget_usd:.0f}"
                ),
            )

            profile_col3.metric(
                "Daily Budget",
                (
                    f"${profile.daily_budget():.2f}"
                ),
            )

            st.write(
                f"**Starting Point:** "
                f"{profile.starting_point}"
            )

            st.write(
                f"**Travel Style:** "
                f"{profile.travel_style}"
            )

            st.write(
                f"**Crowd Preference:** "
                f"{profile.crowd_preference}"
            )

            st.write(
                f"**Transport:** "
                f"{profile.transport}"
            )

            st.write(
                f"**Interests:** "
                f"{', '.join(profile.interests)}"
            )

            st.divider()

            with st.spinner(
                "Generating recommendations, "
                "retrieving weather, optimizing route "
                "and building your itinerary..."
            ):
                plan = (
                    generate_trip_plan(
                        profile=profile,
                        weather_fetcher=(
                            get_cached_weather_forecast
                        ),
                    )
                )

            display_trip_plan(
                plan
            )

        except (
            TypeError,
            ValueError,
            RuntimeError,
        ) as error:
            st.error(
                str(error)
            )

    st.divider()

    st.caption(
        "CeylonCompass V1 • Explainable Recommendation "
        "• Weather-Aware Weighted Ranking "
        "• Route Optimization • Interactive Mapping "
        "• Itinerary Planning • Budget Estimation"
    )


if __name__ == "__main__":
    main()