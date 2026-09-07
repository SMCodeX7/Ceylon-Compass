from html import escape

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
from src.ui.theme import (
    apply_ceylon_compass_theme,
    render_footer,
    render_hero,
    render_section_intro,
    render_sidebar_brand,
    render_traveller_profile,
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
    page_title="Ceylon Compass",
    page_icon="🇱🇰",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_ceylon_compass_theme()
render_sidebar_brand()


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
    Retrieve and temporarily cache Open-Meteo forecast data.

    The unified planning service receives this function
    as its weather provider.
    """

    return fetch_weather_forecast(
        latitude=latitude,
        longitude=longitude,
        forecast_days=forecast_days,
    )


def display_scoring_methodology() -> None:
    """Explain the final weighted recommendation model."""

    with st.expander(
        "How the Recommendation Score works"
    ):
        st.markdown(
            "### Final Ceylon Compass Ranking Model"
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
            "If Weather Information is unavailable for a "
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
            "from the starting location and relative "
            "proximity to the candidate cluster. "
            "It is not road-routing distance."
        )


def render_recommendation_card(
    destination,
    explanation,
) -> None:
    """Render one detailed destination recommendation card."""

    rank = int(destination["final_recommendation_rank"])
    final_score = float(destination["final_score"])
    score_progress = min(max(final_score, 0.0), 100.0)
    weather_available = bool(destination["weather_component_active"])
    crowd_available = bool(destination["crowd_component_active"])

    reasons_html = "".join(
        f"<li>{escape(str(reason))}</li>"
        for reason in explanation["reasons"]
    )

    tradeoffs_html = "".join(
        f"<li>{escape(str(tradeoff))}</li>"
        for tradeoff in explanation["tradeoffs"]
    )

    weather_score = (
        f"{float(destination['ranking_weather_score']):.1f}%"
        if weather_available
        else "Unavailable"
    )
    weather_label = (
        str(destination["ranking_weather_suitability"])
        if weather_available
        else "Weather Information unavailable"
    )
    crowd_value = (
        f"{float(destination['crowd_score']):.1f}%"
        if crowd_available
        else "Not included"
    )
    crowd_label = (
        "Crowd compatibility"
        if crowd_available
        else "No crowd preference selected"
    )

    supporting_factors_html = f"""
<div class="cc-explanation-factors">
    <div class="cc-explanation-factor">
        <span>Matching interests</span>
        <strong>{float(destination['preference_score']):.1f}%</strong>
    </div>
    <div class="cc-explanation-factor">
        <span>Budget compatibility</span>
        <strong>{float(destination['budget_score']):.1f}%</strong>
    </div>
    <div class="cc-explanation-factor">
        <span>Weather suitability</span>
        <strong>{weather_score}</strong>
        <small>{escape(weather_label)}</small>
    </div>
    <div class="cc-explanation-factor">
        <span>{crowd_label}</span>
        <strong>{crowd_value}</strong>
    </div>
    <div class="cc-explanation-factor">
        <span>Route efficiency</span>
        <strong>{float(destination['route_efficiency_score']):.1f}%</strong>
    </div>
</div>
"""

    tradeoffs_section = ""
    if tradeoffs_html:
        tradeoffs_section = f"""
<section class="cc-explanation-block cc-explanation-limitations">
    <h4>Possible limitations and trade-offs</h4>
    <ul>{tradeoffs_html}</ul>
</section>
"""

    card_html = f"""
<details class="cc-recommendation-card">
    <summary>
        <span class="cc-recommendation-rank">
            <span>Ranking position</span>
            <strong>{rank}</strong>
        </span>
        <span class="cc-recommendation-summary">
            <strong>{escape(str(destination['name']))}</strong>
            <span>Recommendation Score {final_score:.1f}%</span>
        </span>
    </summary>

    <div class="cc-recommendation-body">
        <div class="cc-recommendation-heading">
            <div>
                <h3>{escape(str(destination['name']))}</h3>
                <p>
                    {escape(str(destination['district']))} District,
                    {escape(str(destination['province']))} Province
                </p>
            </div>
            <div class="cc-recommendation-score">
                <div class="cc-recommendation-score-heading">
                    <span>Recommendation Score</span>
                    <strong>{final_score:.1f}%</strong>
                </div>
                <div
                    class="cc-recommendation-score-track"
                    role="progressbar"
                    aria-label="Recommendation Score"
                    aria-valuemin="0"
                    aria-valuemax="100"
                    aria-valuenow="{final_score:.1f}"
                >
                    <span style="width: {score_progress:.1f}%"></span>
                </div>
                <small>Score range: 0 to 100</small>
            </div>
        </div>

        <div class="cc-recommendation-facts">
            <div class="cc-recommendation-fact">
                <span>Category</span>
                <strong>{escape(str(destination['category']))}</strong>
            </div>
            <div class="cc-recommendation-fact">
                <span>Estimated daily cost</span>
                <strong>${float(destination['estimated_daily_cost_usd']):.0f}</strong>
            </div>
            <div class="cc-recommendation-fact">
                <span>Visit duration</span>
                <strong>{float(destination['recommended_duration_hours']):.0f} hours</strong>
            </div>
            <div class="cc-recommendation-fact">
                <span>Distance from start</span>
                <strong>{float(destination['distance_from_start_km']):.1f} km</strong>
            </div>
        </div>

        <section class="cc-recommendation-explanation">
            <div class="cc-explanation-block">
                <h4>Recommendation reason</h4>
                <p class="cc-explanation-lead">
                    This destination matches the preferences and constraints
                    in the current traveller profile.
                </p>
                <ul>{reasons_html}</ul>
            </div>
            <div class="cc-explanation-block">
                <h4>Supporting factors</h4>
                {supporting_factors_html}
            </div>
            {tradeoffs_section}
        </section>

        <details class="cc-recommendation-weights">
            <summary>Active score weights</summary>
            <div class="cc-recommendation-weight-grid">
                <span>Preference <strong>{float(destination['preference_weight_used']) * 100:.0f}%</strong></span>
                <span>Budget <strong>{float(destination['budget_weight_used']) * 100:.0f}%</strong></span>
                <span>Weather <strong>{float(destination['weather_weight_used']) * 100:.0f}%</strong></span>
                <span>Crowd <strong>{float(destination['crowd_weight_used']) * 100:.0f}%</strong></span>
                <span>Route efficiency <strong>{float(destination['route_efficiency_weight_used']) * 100:.0f}%</strong></span>
                <span>Active weight total <strong>{float(destination['active_weight_total']) * 100:.0f}%</strong></span>
            </div>
        </details>
    </div>
</details>
"""

    st.html(card_html.replace("    ", ""))


def display_recommendations(
    plan: TripPlan,
) -> None:
    """
    Display final destination recommendations produced
    by the unified planning service.
    """

    recommendations = plan.recommendations

    st.header(
        "Final Destination Recommendations"
    )

    st.caption(
        "Destinations are ranked using traveller "
        "preferences, budget compatibility, Weather Information, "
        "crowd preference when selected, and geographic "
        "route-efficiency information."
    )

    display_scoring_methodology()

    st.subheader(
        "Recommendation Details"
    )

    st.caption(
        "Each recommendation includes its rationale, the scoring factors "
        "that shaped its Recommendation Score, and relevant trade-offs."
    )

    if recommendations.empty:
        st.info(
            "No destinations matched the current travel settings. "
            "Try adjusting your interests, budget, or travel style."
        )
        return

    for _, destination in recommendations.head(5).iterrows():
        explanation = explain_destination(
            destination,
            plan.profile,
        )
        render_recommendation_card(
            destination,
            explanation,
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
        "Explore Your Optimized Route"
    )

    st.caption(
        "Use the map to see how your selected destinations "
        "connect from the starting location and follow the "
        "recommended visit sequence."
    )

    with st.container(border=True):
        st.subheader(
            "Route Overview"
        )

        overview_col1, overview_col2, overview_col3 = (
            st.columns(3)
        )

        overview_col1.metric(
            "Starting Location",
            plan.profile.starting_point,
        )

        overview_col2.metric(
            "Destinations",
            len(plan.optimized_route),
        )

        overview_col3.metric(
            "Route Distance",
            f"{plan.optimized_route_distance_km:.1f} km",
        )

        st.write(
            "**Route efficiency** is a geographic planning "
            "proxy used to select suitable route candidates. "
            "It considers distance from the starting location and "
            "relative proximity within the destination cluster; "
            "it is not driving-road distance."
        )

    st.markdown(
        "**Reading the map:** The green marker identifies the "
        "starting location. Numbered markers show the optimized "
        "visit order, and the connecting line follows that "
        "geographic sequence."
    )

    route_map = build_optimized_route_map(
        plan.optimized_route,
        plan.profile.starting_point,
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
    """Display optimized route information."""

    st.divider()

    st.header(
        "Optimized Trip Route"
    )

    summary = plan.itinerary_summary

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

    if not route_names:
        st.info(
            "No route destinations are available for these travel settings. "
            "Try adjusting your trip preferences and generate the journey again."
        )
        return

    if (
        route_names
        and route_names[
            0
        ].casefold()
        == plan.profile.starting_point.casefold()
    ):
        route_text = " → ".join(
            route_names
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

    with st.container(border=True):
        st.subheader(
            "Why This Route Was Selected"
        )

        st.caption(
            "The route combines destination quality with an "
            "efficient geographic sequence."
        )

        st.caption(
            "Technical note: route optimization selects an efficient visit "
            "order using geographic distance calculations based on Haversine "
            "great-circle distance between coordinates. It is not turn-by-turn "
            "navigation."
        )

        explanation_col1, explanation_col2 = (
            st.columns(2)
        )

        explanation_col1.markdown(
            "**Reduced unnecessary travel distance**\n\n"
            "The optimized sequence uses the existing segment "
            "distances from the starting location through each "
            "destination to limit avoidable geographic travel."
        )

        explanation_col2.markdown(
            "**Destination sequence optimization**\n\n"
            "Each numbered stop reflects the `route_order` "
            "selected for the trip, so the visit order is explicit "
            "from the first destination to the last."
        )

        explanation_col1.markdown(
            "**Geographic efficiency**\n\n"
            "Route efficiency uses the existing geographic "
            "distance information to favor destinations that are "
            "closer to the starting location and destination cluster."
        )

        explanation_col2.markdown(
            "**Preference-aware route planning**\n\n"
            "The route is built from destinations already ranked by "
            "the Recommendation Score, preserving the current "
            "traveller preference, budget, weather, crowd, and route "
            "efficiency signals."
        )

    route_stops = []

    for _, destination in (
        plan.optimized_route
        .sort_values("route_order")
        .iterrows()
    ):
        route_order = int(
            destination[
                "route_order"
            ]
        )

        route_stops.append(
            f"""
            <article class="cc-route-stop">
                <div class="cc-route-marker" aria-hidden="true">
                    {route_order}
                </div>
                <div class="cc-route-card">
                    <div class="cc-route-card-header">
                        <div>
                            <p class="cc-route-stop-order">
                                Stop {route_order}
                            </p>
                            <h3>{escape(str(destination['name']))}</h3>
                        </div>
                        <div class="cc-route-score">
                            <span>Recommendation Score</span>
                            <strong>{float(destination['final_score']):.1f}%</strong>
                        </div>
                    </div>
                    <div class="cc-route-details">
                        <div class="cc-route-detail">
                            <span>District</span>
                            <strong>{escape(str(destination['district']))}</strong>
                        </div>
                        <div class="cc-route-detail">
                            <span>Category</span>
                            <strong>{escape(str(destination['category']))}</strong>
                        </div>
                        <div class="cc-route-detail cc-route-distance">
                            <span>Distance from previous location</span>
                            <strong>{float(destination['distance_from_previous_km']):.1f} km</strong>
                        </div>
                    </div>
                </div>
            </article>
            """
        )

    route_timeline_html = f"""
    <div class="cc-route-timeline">
        {''.join(route_stops)}
    </div>
    """

    st.html(
        route_timeline_html.replace(
            "        ",
            "",
        )
    )

    display_interactive_route_map(
        plan
    )


def display_itinerary(
    plan: TripPlan,
) -> None:
    """Display the generated day-by-day itinerary."""

    st.divider()

    st.header(
        "Day-by-Day Itinerary"
    )

    itinerary = plan.itinerary
    summary = plan.itinerary_summary

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
            "No destinations fit within the selected trip duration. "
            "Try adding more trip days or choosing a shorter set of activities."
        )

    else:
        itinerary_days = sorted(
            scheduled[
                "itinerary_day"
            ]
            .dropna()
            .unique()
        )

        itinerary_html = [
            '<div class="cc-itinerary-container">'
        ]

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

            itinerary_html.append(
                f'<details class="cc-itinerary-card '
                f'cc-itinerary-day-card" open>'
                f'<summary class="cc-itinerary-header">'
                f'Day {day_number} | '
                f'{day_hours:.1f} activity hours'
                f'</summary>'
            )

            for _, destination in day_plan.iterrows():
                destination_name = escape(
                    str(destination["name"])
                )
                destination_location = escape(
                    f'{destination["district"]} District, '
                    f'{destination["province"]} Province'
                )
                category = escape(
                    str(destination["category"])
                )
                duration_hours = float(
                    destination[
                        "recommended_duration_hours"
                    ]
                )
                estimated_daily_cost = float(
                    destination[
                        "estimated_daily_cost_usd"
                    ]
                )
                travel_distance = float(
                    destination[
                        "distance_from_previous_km"
                    ]
                )

                itinerary_html.append(
                    '<article class="cc-itinerary-item '
                    'cc-itinerary-destination">'
                    '<div class="cc-itinerary-header">'
                    f'<h3>{int(destination["visit_order_in_day"])}. '
                    f'{destination_name}</h3>'
                    f'<p>{destination_location}</p>'
                    '</div>'
                    '<div class="cc-itinerary-details">'
                    '<div class="cc-itinerary-activity-list">'
                    '<strong>Activity</strong>'
                    f'<span>{category}</span>'
                    '</div>'
                    '<div>'
                    '<strong class="cc-itinerary-duration">'
                    'Duration</strong>'
                    f'<span>{duration_hours:.0f} hours</span>'
                    '</div>'
                    '<div>'
                    '<strong class="cc-itinerary-cost">'
                    'Estimated cost</strong>'
                    f'<span>${estimated_daily_cost:.0f} per day</span>'
                    '</div>'
                    '<div>'
                    '<strong>Travel from previous stop</strong>'
                    f'<span>{travel_distance:.1f} km</span>'
                    '</div>'
                    '</div>'
                )

                if bool(
                    destination[
                        "weather_available"
                    ]
                ):
                    weather_description = escape(
                        str(destination[
                            "weather_description"
                        ])
                    )
                    weather_date = escape(
                        str(destination[
                            "weather_date"
                        ])
                    )
                    weather_suitability = escape(
                        str(destination[
                            "weather_suitability"
                        ])
                    )
                    itinerary_html.append(
                        '<div class="cc-itinerary-details '
                        'cc-itinerary-weather">'
                        '<div>'
                        '<strong>Forecast</strong>'
                        f'<span>{weather_description}</span>'
                        f'<small>Forecast date: {weather_date}</small>'
                        '</div>'
                        '<div>'
                        '<strong>Weather suitability</strong>'
                        f'<span>{float(destination["weather_score"]):.1f}% '
                        f'{weather_suitability}</span>'
                        f'<small>Rain probability: '
                        f'{float(destination["weather_rain_probability"]):.0f}%'
                        '</small>'
                        '</div>'
                        '</div>'
                    )
                else:
                    itinerary_html.append(
                        '<p>Weather Information is unavailable '
                        'for this itinerary stop.</p>'
                    )

                itinerary_html.append(
                    '</article>'
                )

            itinerary_html.append(
                '</details>'
            )

        itinerary_html.append(
            '</div>'
        )
        st.html("".join(itinerary_html))

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

        for _, destination in unscheduled.iterrows():
            with st.container(border=True):
                destination_col, duration_col, score_col = st.columns(
                    [2, 1, 1]
                )

                destination_col.markdown(
                    f"#### {destination['name']}"
                )

                destination_col.caption(
                    f"{destination['category']} | "
                    f"{destination['district']} District, "
                    f"{destination['province']} Province"
                )

                duration_col.metric(
                    "Required time",
                    (
                        f"{float(destination['recommended_duration_hours']):.0f} "
                        f"hours"
                    ),
                )

                score_col.metric(
                    "Recommendation Score",
                    f"{float(destination['final_score']):.1f}%",
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
        "Weather Information"
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
            "Weather Information is unavailable for the scheduled destinations. "
            "Your recommendations and itinerary are still available without weather details."
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
        width="stretch",
        hide_index=True,
    )

    st.caption(
        "Weather data: Open-Meteo. Forecasts can "
        "change and should be rechecked close to "
        "travel time."
    )

    st.caption(
        "Ceylon Compass currently assumes the trip "
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

    budget = plan.budget
    profile = plan.profile

    st.divider()

    st.header(
        "Trip Budget"
    )

    if not plan.itinerary["scheduled"].any():
        st.info(
            "No destinations are scheduled, so this Trip Budget estimate currently "
            "contains no activity or transport costs."
        )

    daily_average_cost = (
        budget[
            "estimated_total_cost_usd"
        ]
        / max(
            int(
                profile.trip_days
            ),
            1,
        )
    )

    budget_html = [
        '<section class="cc-budget-container">',
        '<h3>Budget summary</h3>',
        '<div class="cc-budget-summary">',
        '<div class="cc-budget-summary-card '
        'cc-budget-total-cost cc-budget-total">',
        '<span>Total estimated cost</span>',
        f'<strong>${budget["estimated_total_cost_usd"]:.2f}'
        '</strong>',
        '</div>',
        '<div class="cc-budget-summary-card">',
        '<span>Daily average cost</span>',
        f'<strong>${daily_average_cost:.2f}</strong>',
        '</div>',
        '<div class="cc-budget-summary-card">',
        '<span>Available budget</span>',
        f'<strong>${budget["total_budget_usd"]:.2f}</strong>',
        '</div>',
        '</div>',
        '<h3>Cost breakdown</h3>',
        '<div class="cc-budget-breakdown">',
        '<div class="cc-budget-breakdown-row cc-budget-item">',
        '<span>Activity and destination cost</span>',
        f'<strong>${budget["destination_cost_usd"]:.2f}</strong>',
        '</div>',
        '<div class="cc-budget-breakdown-row cc-budget-item">',
        '<span>Transport cost</span>',
        f'<strong>${budget["transport_cost_usd"]:.2f}</strong>',
        '</div>',
        '<div class="cc-budget-expense-category '
        'cc-budget-item">',
        '<span>Accommodation cost</span>',
        '<strong>Not modelled</strong>',
        '</div>',
        '<div class="cc-budget-expense-category '
        'cc-budget-item">',
        '<span>Food cost</span>',
        '<strong>Not modelled</strong>',
        '</div>',
        '<div class="cc-budget-expense-category '
        'cc-budget-item">',
        '<span>Other expenses</span>',
        '<strong>Not modelled</strong>',
        '</div>',
        '</div>',
        '<p>Accommodation, food, and other expenses are not '
        'included in the current budget model.</p>',
        '</section>',
    ]

    st.html("".join(budget_html))

    st.subheader(
        "Spending overview"
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

    with st.container(border=True):
        st.write(
            f"**Estimated budget used:** "
            f"{budget_used_percent:.1f}%"
        )

        st.progress(
            min(
                budget_used_percent / 100.0,
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
        "How this Trip Budget estimate is calculated"
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


def display_trip_summary(
    plan: TripPlan,
) -> None:
    """Display a compact overview of the generated trip."""

    top_destination = "Unavailable"
    if not plan.recommendations.empty:
        top_destination = str(
            plan.recommendations.iloc[0]["name"]
        )

    scheduled = plan.itinerary[
        plan.itinerary["scheduled"]
    ]
    weather_available = int(
        scheduled["weather_available"].sum()
    )

    summary_html = f"""
<section class="cc-trip-summary" aria-label="Trip summary">
    <div class="cc-trip-summary-card">
        <span>Top recommendation</span>
        <strong>{escape(top_destination)}</strong>
    </div>
    <div class="cc-trip-summary-card">
        <span>Route distance</span>
        <strong>{plan.optimized_route_distance_km:.1f} km</strong>
    </div>
    <div class="cc-trip-summary-card">
        <span>Estimated cost</span>
        <strong>${plan.budget['estimated_total_cost_usd']:.2f}</strong>
    </div>
    <div class="cc-trip-summary-card">
        <span>Weather availability</span>
        <strong>{weather_available}/{len(scheduled)} places</strong>
    </div>
    <div class="cc-trip-summary-card">
        <span>Destinations</span>
        <strong>{len(plan.optimized_route)}</strong>
    </div>
</section>
"""

    st.html(summary_html.replace("    ", ""))


def display_trip_plan(
    plan: TripPlan,
) -> None:
    """Render all outputs from one unified TripPlan."""

    display_trip_summary(
        plan
    )

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
    """Render the complete Ceylon Compass application."""

    render_hero()

    render_section_intro(
        title="Plan your Sri Lankan trip with clear reasons",
        description=(
            "Get explainable destination recommendations, an optimized "
            "visit order, weather-aware planning, and a budget-aware "
            "itinerary from one traveller profile."
        ),
        icon="🧳",
    )

    with st.container(border=True):
        col1, col2 = st.columns(
            2,
            gap="large",
        )

        with col1:
            starting_point = st.selectbox(
                "Starting Location",
                [
                    "Colombo",
                    "Kandy",
                    "Galle",
                    "Jaffna",
                    "Negombo",
                ],
                help="Choose where your journey begins.",
            )

            trip_days = st.slider(
                "Trip Duration (Days)",
                min_value=1,
                max_value=14,
                value=5,
                help=(
                    "Choose a trip duration between "
                    "1 and 14 days."
                ),
            )

            budget = st.number_input(
                "Trip Budget (USD)",
                min_value=50,
                max_value=5000,
                value=500,
                step=50,
                help=(
                    "Enter the Trip Budget "
                    "for your trip."
                ),
            )

        with col2:
            travel_style = st.selectbox(
                "Travel Style",
                [
                    "Budget",
                    "Balanced",
                    "Comfort",
                ],
                help=(
                    "The travel style controls the cost "
                    "assumptions used by the budget model."
                ),
            )

            crowd_preference = st.selectbox(
                "Crowd Preference",
                [
                    "No Preference",
                    "Prefer Less Crowded Places",
                    "Popular Tourist Places",
                ],
                help=(
                    "Choose whether you prefer quieter "
                    "destinations or popular attractions."
                ),
            )

            transport = st.selectbox(
                "Transport Preference",
                [
                    "Public Transport",
                    "Mixed Transport",
                    "Private Vehicle",
                ],
                help=(
                    "Your transport choice is used when "
                    "estimating route costs."
                ),
            )

        st.markdown(
            "### What would you love to experience?"
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
            help=(
                "Select multiple interests to receive "
                "more personalized recommendations."
            ),
        )

    st.markdown("")

    generate_trip = st.button(
        "✨ Create My Smart Journey",
        type="primary",
        width="stretch",
    )

    if generate_trip:
        if not interests:
            st.warning(
                "Please select at least one travel interest."
            )

            render_footer()
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

            render_section_intro(
                title="Your traveller profile",
                description=(
                    "A clear summary of the preferences being "
                    "used to create your personalized journey."
                ),
                icon="👤",
            )

            render_traveller_profile(
                starting_point=profile.starting_point,
                trip_days=profile.trip_days,
                budget_usd=profile.budget_usd,
                daily_budget_usd=profile.daily_budget(),
                travel_style=profile.travel_style,
                crowd_preference=profile.crowd_preference,
                transport=profile.transport,
                interests=profile.interests,
            )

            with st.spinner(
                "Building your Sri Lankan journey: "
                "ranking destinations, retrieving weather, "
                "optimizing the route and preparing the "
                "itinerary..."
            ):
                plan = generate_trip_plan(
                    profile=profile,
                    weather_fetcher=(
                        get_cached_weather_forecast
                    ),
                )

            display_trip_plan(plan)

        except (
            TypeError,
            ValueError,
            RuntimeError,
        ) as error:
            st.error(
                "Unable to generate your journey with the current travel settings. "
                "Try adjusting your preferences and generating the journey again."
            )

            with st.expander(
                "Technical details"
            ):
                st.code(
                    f"{type(error).__name__}: {error}"
                )

    render_footer()


if __name__ == "__main__":
    main()