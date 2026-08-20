import streamlit as st

from src.recommendation.recommender import rank_destinations
from src.recommendation.traveller_profile import TravellerProfile


st.set_page_config(
    page_title="CeylonCompass",
    page_icon="\U0001F1F1\U0001F1F0",
    layout="wide",
    initial_sidebar_state="expanded",
)


def display_recommendations(profile: TravellerProfile) -> None:
    """Generate and display ranked destination recommendations."""

    recommendations = rank_destinations(
        profile,
        top_n=10,
    )

    st.subheader("Top Destination Recommendations")

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

    st.subheader("Recommendation Details")

    for _, destination in recommendations.head(5).iterrows():
        with st.expander(
            f"#{int(destination['recommendation_rank'])} "
            f"{destination['name']} "
            f"— {destination['current_stage_score']:.2f}%"
        ):
            col1, col2, col3, col4 = st.columns(4)

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

            st.write(
                f"**Category:** {destination['category']}"
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

            if destination["budget_compatible"]:
                st.success(
                    "This destination is within the traveller's "
                    "current daily budget."
                )
            else:
                st.warning(
                    "This destination is above the traveller's "
                    "current daily budget."
                )


def main() -> None:
    st.title("\U0001F1F1\U0001F1F0 CeylonCompass")

    st.subheader(
        "Smart Sri Lanka Travel Recommendation & Route Optimization"
    )

    st.write(
        """
        Plan a personalized Sri Lankan journey based on your interests,
        budget, trip duration, travel style, and preferred destinations.
        """
    )

    st.info(
        "CeylonCompass V1 combines explainable destination "
        "recommendation with budget-aware and crowd-aware ranking. "
        "Weather intelligence, route optimization, itinerary generation, "
        "and interactive maps will be added in the next stages."
    )

    st.divider()

    st.header("Plan Your Trip")

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

    st.subheader("Your Interests")

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
        default=["Nature"],
    )

    st.divider()

    if st.button(
        "Generate Smart Trip",
        type="primary",
        use_container_width=True,
    ):
        if not interests:
            st.warning(
                "Please select at least one travel interest."
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
                "Traveller profile processed successfully."
            )

            st.subheader("Current Traveller Profile")

            profile_col1, profile_col2, profile_col3 = st.columns(3)

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

            display_recommendations(profile)

        except ValueError as error:
            st.error(str(error))

    st.divider()

    st.caption(
        "CeylonCompass V1 \u2022 Explainable Travel Recommendation "
        "and Route Optimization for Sri Lanka"
    )


if __name__ == "__main__":
    main()