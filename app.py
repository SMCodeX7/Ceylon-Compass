import streamlit as st

from src.budget.estimator import (
    TRANSPORT_COST_PER_KM,
    TRAVEL_STYLE_FACTORS,
    estimate_trip_budget,
)
from src.itinerary.planner import (
    generate_itinerary,
    itinerary_summary,
)
from src.optimization.route_optimizer import (
    calculate_optimized_route_distance,
    optimize_route,
)
from src.recommendation.explanations import (
    explain_destination,
)
from src.recommendation.recommender import (
    rank_destinations,
)
from src.recommendation.traveller_profile import (
    TravellerProfile,
)


ROUTE_CANDIDATE_COUNT = 7


st.set_page_config(
    page_title="CeylonCompass",
    page_icon="\U0001F1F1\U0001F1F0",
    layout="wide",
    initial_sidebar_state="expanded",
)


def display_recommendations(
    profile: TravellerProfile,
):
    """
    Generate and display ranked destination
    recommendations.

    Returns the ranked recommendations so they can be
    passed directly to route optimization.
    """

    recommendations = rank_destinations(
        profile,
        top_n=10,
    )

    st.subheader(
        "Top Destination Recommendations"
    )

    st.caption(
        "Current ranking combines traveller interests, "
        "budget compatibility, and crowd preference."
    )

    display_df = recommendations[
        [
            "recommendation_rank",
            "name",
            "category",
            "estimated_daily_cost_usd",
            "preference_score",
            "budget_score",
            "crowd_score",
            "current_stage_score",
        ]
    ].copy()

    display_df.columns = [
        "Rank",
        "Destination",
        "Category",
        "Daily Cost (USD)",
        "Interest Match",
        "Budget Match",
        "Crowd Match",
        "Overall Score",
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader(
        "Recommendation Details"
    )

    st.caption(
        "Open a destination below to see its score "
        "breakdown, recommendation reasons, and "
        "possible trade-offs."
    )

    for _, destination in (
        recommendations
        .head(5)
        .iterrows()
    ):
        explanation = explain_destination(
            destination,
            profile,
        )

        with st.expander(
            f"#{int(destination['recommendation_rank'])} "
            f"{destination['name']} "
            f"— {destination['current_stage_score']:.2f}%"
        ):
            col1, col2, col3, col4 = (
                st.columns(4)
            )

            col1.metric(
                "Interest Match",
                f"{destination['preference_score']:.1f}%",
            )

            col2.metric(
                "Budget Match",
                f"{destination['budget_score']:.1f}%",
            )

            col3.metric(
                "Crowd Match",
                f"{destination['crowd_score']:.1f}%",
            )

            col4.metric(
                "Current Score",
                f"{destination['current_stage_score']:.1f}%",
            )

            st.divider()

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
                f"${destination['estimated_daily_cost_usd']:.0f}"
            )

            st.write(
                f"**Recommended Visit Duration:** "
                f"{destination['recommended_duration_hours']:.0f} "
                f"hours"
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

            if explanation["tradeoffs"]:
                st.markdown(
                    "### Trade-offs to consider"
                )

                for tradeoff in explanation[
                    "tradeoffs"
                ]:
                    st.write(
                        f"- {tradeoff}"
                    )
            else:
                st.success(
                    "No major trade-offs were identified "
                    "for your current traveller profile."
                )

    return recommendations


def display_budget_breakdown(
    profile: TravellerProfile,
    itinerary,
) -> None:
    """
    Display the estimated trip budget for the
    scheduled itinerary.
    """

    budget = estimate_trip_budget(
        itinerary=itinerary,
        total_budget_usd=profile.budget_usd,
        travel_style=profile.travel_style,
        transport=profile.transport,
    )

    st.divider()

    st.header(
        "Estimated Trip Budget"
    )

    budget_col1, budget_col2, budget_col3, budget_col4 = (
        st.columns(4)
    )

    budget_col1.metric(
        "Available Budget",
        f"${budget['total_budget_usd']:.2f}",
    )

    budget_col2.metric(
        "Destination Cost",
        f"${budget['destination_cost_usd']:.2f}",
    )

    budget_col3.metric(
        "Transport Cost",
        f"${budget['transport_cost_usd']:.2f}",
    )

    budget_col4.metric(
        "Estimated Total",
        f"${budget['estimated_total_cost_usd']:.2f}",
    )

    budget_used_percent = (
        budget["estimated_total_cost_usd"]
        / budget["total_budget_usd"]
        * 100
    )

    st.write(
        f"**Estimated Budget Used:** "
        f"{budget_used_percent:.1f}%"
    )

    progress_value = min(
        budget_used_percent / 100,
        1.0,
    )

    st.progress(
        progress_value
    )

    if budget["within_budget"]:
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
            f"Estimated trip cost exceeds the selected "
            f"budget by approximately "
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
            f"**Transport Preference:** "
            f"{profile.transport}"
        )

        st.write(
            f"**Transport Cost Assumption:** "
            f"${transport_rate:.2f} per km"
        )

        st.write(
            """
            Destination costs are estimated using each
            destination's daily cost, the recommended
            visit duration, and the selected travel-style
            factor.
            """
        )

        st.write(
            """
            Transport cost is currently estimated using
            the Haversine geographic route-distance proxy
            multiplied by the selected transport-rate
            assumption.
            """
        )

        st.warning(
            "These values are transparent V1 modelling "
            "assumptions rather than guaranteed market "
            "prices. The estimate does not currently "
            "include international flights, visas, "
            "shopping, insurance, or other personal "
            "expenses."
        )


def display_route_and_itinerary(
    profile: TravellerProfile,
    recommendations,
) -> None:
    """
    Optimize the top recommended destinations, create
    a feasible itinerary, and display its budget.
    """

    st.divider()

    st.header(
        "Optimized Trip Route"
    )

    route_candidates = (
        recommendations
        .head(ROUTE_CANDIDATE_COUNT)
        .copy()
    )

    optimized_route = optimize_route(
        route_candidates,
        profile.starting_point,
    )

    optimized_distance = (
        calculate_optimized_route_distance(
            optimized_route
        )
    )

    itinerary = generate_itinerary(
        optimized_route,
        profile.trip_days,
    )

    summary = itinerary_summary(
        itinerary
    )

    route_col1, route_col2, route_col3, route_col4 = (
        st.columns(4)
    )

    route_col1.metric(
        "Route Candidates",
        len(optimized_route),
    )

    route_col2.metric(
        "Route Distance",
        f"{optimized_distance:.1f} km",
    )

    route_col3.metric(
        "Scheduled Places",
        summary["scheduled_destinations"],
    )

    route_col4.metric(
        "Days Used",
        summary["days_used"],
    )

    st.caption(
        "Route distance currently uses Haversine "
        "great-circle distance between geographic "
        "coordinates. It is a geographic distance "
        "proxy, not driving-road distance."
    )

    route_names = (
        optimized_route["name"]
        .tolist()
    )

    route_text = (
        profile.starting_point
        + " → "
        + " → ".join(route_names)
    )

    st.markdown(
        "### Recommended Visit Order"
    )

    st.write(
        route_text
    )

    route_display = optimized_route[
        [
            "route_order",
            "name",
            "district",
            "category",
            "distance_from_previous_km",
        ]
    ].copy()

    route_display.columns = [
        "Route Order",
        "Destination",
        "District",
        "Category",
        "Distance From Previous (km)",
    ]

    st.dataframe(
        route_display,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.header(
        "Day-by-Day Itinerary"
    )

    itinerary_col1, itinerary_col2, itinerary_col3 = (
        st.columns(3)
    )

    itinerary_col1.metric(
        "Scheduled Destinations",
        summary[
            "scheduled_destinations"
        ],
    )

    itinerary_col2.metric(
        "Total Activity Time",
        (
            f"{summary['total_activity_hours']:.1f} "
            f"hours"
        ),
    )

    itinerary_col3.metric(
        "Unscheduled Destinations",
        summary[
            "unscheduled_destinations"
        ],
    )

    scheduled_itinerary = itinerary[
        itinerary["scheduled"]
    ].copy()

    if scheduled_itinerary.empty:
        st.warning(
            "No destinations could be scheduled "
            "within the selected trip duration."
        )
    else:
        for day in sorted(
            scheduled_itinerary[
                "itinerary_day"
            ].dropna().unique()
        ):
            day_number = int(day)

            day_plan = (
                scheduled_itinerary[
                    scheduled_itinerary[
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
                f"Day {day_number} "
                f"— {day_hours:.1f} activity hours",
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
                        f"{destination['recommended_duration_hours']:.0f} "
                        f"hours"
                    )

                    detail_col3.write(
                        f"**Travel Distance:** "
                        f"{destination['distance_from_previous_km']:.1f} "
                        f"km"
                    )

                    st.write(
                        f"**Location:** "
                        f"{destination['district']} District, "
                        f"{destination['province']} Province"
                    )

                    st.divider()

    unscheduled = itinerary[
        ~itinerary["scheduled"]
    ].copy()

    if not unscheduled.empty:
        st.warning(
            f"{len(unscheduled)} recommended "
            f"destination(s) could not fit within "
            f"the selected {profile.trip_days}-day "
            f"trip while respecting the current "
            f"8-hour daily activity limit."
        )

        unscheduled_display = unscheduled[
            [
                "name",
                "category",
                "recommended_duration_hours",
                "current_stage_score",
            ]
        ].copy()

        unscheduled_display.columns = [
            "Destination",
            "Category",
            "Required Activity Hours",
            "Recommendation Score",
        ]

        st.dataframe(
            unscheduled_display,
            use_container_width=True,
            hide_index=True,
        )

    display_budget_breakdown(
        profile,
        itinerary,
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
        Plan a personalized Sri Lankan journey based
        on your interests, budget, trip duration,
        travel style, and preferred destinations.
        """
    )

    st.info(
        "CeylonCompass V1 currently provides "
        "explainable destination recommendations, "
        "geospatial route optimization, "
        "day-by-day itinerary scheduling, and "
        "transparent trip budget estimation. "
        "Weather intelligence and interactive maps "
        "will be added in the next development stages."
    )

    st.divider()

    st.header(
        "Plan Your Trip"
    )

    col1, col2 = st.columns(2)

    with col1:
        starting_point = st.selectbox(
            "Starting Point",
            [
                "Colombo",
                "Kandy",
                "Galle",
                "Jaffna",
                "Negombo",
            ],
        )

        trip_days = st.slider(
            "Trip Duration (Days)",
            min_value=1,
            max_value=14,
            value=5,
        )

        budget = st.number_input(
            "Total Budget (USD)",
            min_value=50,
            max_value=5000,
            value=500,
            step=50,
        )

    with col2:
        travel_style = st.selectbox(
            "Travel Style",
            [
                "Budget",
                "Balanced",
                "Comfort",
            ],
        )

        crowd_preference = st.selectbox(
            "Crowd Preference",
            [
                "No Preference",
                "Prefer Less Crowded Places",
                "Popular Tourist Places",
            ],
        )

        transport = st.selectbox(
            "Preferred Transport",
            [
                "Public Transport",
                "Mixed Transport",
                "Private Vehicle",
            ],
        )

    st.subheader(
        "Your Interests"
    )

    interests = st.multiselect(
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
            profile = TravellerProfile(
                starting_point=starting_point,
                trip_days=trip_days,
                budget_usd=float(budget),
                travel_style=travel_style,
                crowd_preference=crowd_preference,
                transport=transport,
                interests=tuple(interests),
            )

            st.success(
                "Traveller profile processed "
                "successfully."
            )

            st.subheader(
                "Current Traveller Profile"
            )

            profile_col1, profile_col2, profile_col3 = (
                st.columns(3)
            )

            profile_col1.metric(
                "Trip Duration",
                f"{profile.trip_days} days",
            )

            profile_col2.metric(
                "Total Budget",
                f"${profile.budget_usd:.0f}",
            )

            profile_col3.metric(
                "Daily Budget",
                f"${profile.daily_budget():.2f}",
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

            recommendations = (
                display_recommendations(
                    profile
                )
            )

            display_route_and_itinerary(
                profile,
                recommendations,
            )

        except (
            ValueError,
            RuntimeError,
        ) as error:
            st.error(
                str(error)
            )

    st.divider()

    st.caption(
        "CeylonCompass V1 • Explainable Travel "
        "Recommendation, Route Optimization, "
        "Itinerary Planning, and Budget Estimation "
        "for Sri Lanka"
    )


if __name__ == "__main__":
    main()