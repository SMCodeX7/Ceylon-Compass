import streamlit as st


st.set_page_config(
    page_title="CeylonCompass",
    page_icon="\U0001F1F1\U0001F1F0",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    st.title("\U0001F1F1\U0001F1F0 CeylonCompass")
    st.subheader("Smart Sri Lanka Travel Recommendation & Route Optimization")

    st.write(
        """
        Plan a personalized Sri Lankan journey based on your interests,
        budget, trip duration, travel style, and preferred destinations.
        """
    )

    st.info(
        "CeylonCompass V1 will combine destination recommendation, "
        "route optimization, budget planning, weather intelligence, "
        "and interactive travel maps."
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

    if st.button("Generate Smart Trip", type="primary", use_container_width=True):
        if not interests:
            st.warning("Please select at least one travel interest.")
            return

        st.success("Traveller profile captured successfully.")

        st.subheader("Current Traveller Profile")

        profile_col1, profile_col2, profile_col3 = st.columns(3)

        profile_col1.metric("Trip Duration", f"{trip_days} days")
        profile_col2.metric("Budget", f"${budget}")
        profile_col3.metric("Starting Point", starting_point)

        st.write(f"**Travel Style:** {travel_style}")
        st.write(f"**Crowd Preference:** {crowd_preference}")
        st.write(f"**Transport:** {transport}")
        st.write(f"**Interests:** {', '.join(interests)}")

        st.info(
            "Destination recommendations will be connected here "
            "after the recommendation engine is implemented."
        )

    st.divider()

    st.caption(
        "CeylonCompass V1 \u2022 Explainable Travel Recommendation "
        "and Route Optimization for Sri Lanka"
    )


if __name__ == "__main__":
    main()
