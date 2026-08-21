"""Visual theme and reusable UI components for Ceylon Compass."""

from html import escape
from typing import Iterable

import streamlit as st


def apply_ceylon_compass_theme() -> None:
    """Apply the tropical light theme across the application."""

    st.markdown(
        """
<style>
:root {
    --cc-ocean: #087E8B;
    --cc-ocean-dark: #075A65;
    --cc-ocean-light: #DFF4F2;
    --cc-green: #24966D;
    --cc-green-dark: #147052;
    --cc-green-light: #E4F4EC;
    --cc-sand: #F7E7C6;
    --cc-sand-light: #FFF9EC;
    --cc-ink: #16323A;
    --cc-muted: #5E7479;
    --cc-border: #D7E7E4;
    --cc-white: #FFFFFF;
}

html,
body,
[class*="css"] {
    font-family:
        Inter,
        "Segoe UI",
        Arial,
        sans-serif;
}

[data-testid="stAppViewContainer"] {
    color: var(--cc-ink);
    background:
        radial-gradient(
            circle at 94% 3%,
            rgba(72, 188, 169, 0.16),
            transparent 24rem
        ),
        linear-gradient(
            180deg,
            #F7FCFB 0%,
            #FFFFFF 34%,
            #FFFDF8 100%
        );
}

[data-testid="stHeader"] {
    background: rgba(247, 252, 251, 0.88);
    backdrop-filter: blur(12px);
}

[data-testid="stMainBlockContainer"] {
    max-width: 1240px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] li,
[data-testid="stAppViewContainer"] label {
    color: var(--cc-muted);
}

h1,
h2,
h3,
h4,
h5,
h6 {
    color: var(--cc-ink) !important;
    font-weight: 750 !important;
    letter-spacing: -0.025em;
}

h2 {
    margin-top: 2.2rem !important;
    padding-bottom: 0.55rem;
    border-bottom: 2px solid var(--cc-sand);
}

[data-testid="stCaptionContainer"] {
    color: #809397 !important;
}

/* Sidebar */

[data-testid="stSidebar"] {
    border-right: 0;
    background:
        linear-gradient(
            180deg,
            #075A65 0%,
            #087E8B 52%,
            #24966D 100%
        );
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #FFFFFF;
}

[data-testid="stSidebar"] button {
    color: #FFFFFF !important;
}

[data-testid="stSidebarCollapseButton"] svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}

.cc-sidebar-brand {
    padding: 0.5rem 0 1rem;
}

.cc-sidebar-mark {
    display: inline-grid;
    place-items: center;
    width: 3rem;
    height: 3rem;
    margin-bottom: 0.8rem;
    border-radius: 1rem;
    background: rgba(255, 255, 255, 0.16);
    color: #FFFFFF;
    font-size: 1.45rem;
}

.cc-sidebar-brand h3 {
    margin: 0 !important;
    padding: 0 !important;
    border: 0 !important;
    color: #FFFFFF !important;
    font-size: 1.3rem !important;
}

.cc-sidebar-brand p {
    margin: 0.4rem 0 0;
    color: rgba(255, 255, 255, 0.78) !important;
    font-size: 0.9rem;
    line-height: 1.55;
}

.cc-sidebar-note {
    margin-top: 1rem;
    padding: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.22);
    border-radius: 1rem;
    background: rgba(255, 255, 255, 0.10);
    color: rgba(255, 255, 255, 0.90) !important;
    font-size: 0.85rem;
    line-height: 1.6;
}

.cc-sidebar-note strong {
    color: #FFFFFF !important;
}

/* Hero */

.cc-hero {
    position: relative;
    overflow: hidden;
    margin-bottom: 1.3rem;
    padding: clamp(2rem, 5vw, 4.2rem);
    border-radius: 1.7rem;
    background:
        radial-gradient(
            circle at 82% 22%,
            rgba(247, 231, 198, 0.46),
            transparent 16rem
        ),
        linear-gradient(
            125deg,
            #075A65 0%,
            #087E8B 54%,
            #24966D 100%
        );
    box-shadow:
        0 20px 50px rgba(7, 90, 101, 0.24);
}

.cc-hero::after {
    content: "";
    position: absolute;
    right: -4rem;
    bottom: -6rem;
    width: 18rem;
    height: 18rem;
    border: 2px solid rgba(255, 255, 255, 0.16);
    border-radius: 50%;
    box-shadow:
        0 0 0 2rem rgba(255, 255, 255, 0.05),
        0 0 0 5rem rgba(255, 255, 255, 0.035);
}

.cc-hero-eyebrow {
    position: relative;
    z-index: 1;
    display: inline-flex;
    align-items: center;
    margin-bottom: 1rem;
    padding: 0.5rem 0.8rem;
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.11);
    color: #FFFFFF !important;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.cc-hero h1 {
    position: relative;
    z-index: 1;
    max-width: 780px;
    margin: 0 0 0.9rem !important;
    padding: 0 !important;
    border: 0 !important;
    color: #FFFFFF !important;
    font-size: clamp(
        2.35rem,
        5vw,
        4.2rem
    ) !important;
    line-height: 1.04 !important;
}

.cc-hero p {
    position: relative;
    z-index: 1;
    max-width: 720px;
    margin: 0;
    color: rgba(255, 255, 255, 0.86) !important;
    font-size: 1.05rem;
    line-height: 1.7;
}

/* Feature cards */

.cc-feature-strip {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.8rem;
    margin: 1.1rem 0 2rem;
}

.cc-feature {
    padding: 1rem;
    border: 1px solid var(--cc-border);
    border-radius: 1rem;
    background: rgba(255, 255, 255, 0.90);
    box-shadow: 0 7px 20px rgba(25, 83, 84, 0.07);
    color: var(--cc-ink) !important;
    font-size: 0.9rem;
    font-weight: 750;
    text-align: center;
}

/* Section headings */

.cc-section-intro {
    margin: 2.1rem 0 0.9rem;
}

.cc-section-label {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    color: var(--cc-ocean) !important;
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.cc-section-intro h2 {
    margin: 0.25rem 0 !important;
    padding: 0 !important;
    border: 0 !important;
    color: var(--cc-ink) !important;
}

.cc-section-intro p {
    margin: 0;
    color: var(--cc-muted) !important;
}

/* Bordered containers */

[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--cc-border) !important;
    border-radius: 1.25rem !important;
    background: rgba(255, 255, 255, 0.88);
    box-shadow: 0 12px 30px rgba(20, 74, 78, 0.09);
}

/* Form fields */

[data-testid="stWidgetLabel"] p {
    color: #3F6269 !important;
    font-weight: 650 !important;
}

[data-baseweb="select"] > div,
[data-testid="stNumberInputContainer"],
[data-testid="stTextInputRootElement"] {
    border-color: var(--cc-border) !important;
    border-radius: 0.75rem !important;
    background: #F1F8F7 !important;
    color: var(--cc-ink) !important;
}

[data-baseweb="select"] input,
[data-baseweb="select"] span,
[data-testid="stNumberInputContainer"] input,
[data-testid="stTextInputRootElement"] input {
    color: var(--cc-ink) !important;
    -webkit-text-fill-color: var(--cc-ink) !important;
}

[data-baseweb="select"] svg,
[data-testid="stNumberInputContainer"] svg {
    color: var(--cc-ink) !important;
    fill: var(--cc-ink) !important;
}

[data-baseweb="tag"] {
    border-radius: 0.55rem !important;
    background: var(--cc-ocean) !important;
}

[data-baseweb="tag"] span,
[data-baseweb="tag"] svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}

[role="listbox"] {
    background: #FFFFFF !important;
}

[role="option"] {
    color: var(--cc-ink) !important;
    background: #FFFFFF !important;
}

[role="option"]:hover {
    background: var(--cc-ocean-light) !important;
}

[aria-selected="true"][role="option"] {
    background: var(--cc-green-light) !important;
}

/* Slider */

[data-testid="stSlider"] [role="slider"] {
    border-color: var(--cc-ocean) !important;
    background: var(--cc-ocean) !important;
}

[data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: var(--cc-ink) !important;
}

[data-testid="stSlider"] div[data-baseweb="slider"] > div > div {
    background-color: var(--cc-ocean) !important;
}

/* Buttons */

.stButton > button,
[data-testid="stFormSubmitButton"] > button {
    min-height: 3rem;
    border: 0 !important;
    border-radius: 0.9rem !important;
    background:
        linear-gradient(
            100deg,
            var(--cc-ocean-dark),
            var(--cc-ocean),
            var(--cc-green)
        ) !important;
    box-shadow: 0 10px 24px rgba(8, 126, 139, 0.22);
    color: #FFFFFF !important;
    font-weight: 800 !important;
    transition:
        transform 160ms ease,
        box-shadow 160ms ease;
}

.stButton > button *,
[data-testid="stFormSubmitButton"] > button * {
    color: #FFFFFF !important;
}

.stButton > button p,
[data-testid="stFormSubmitButton"] > button p {
    color: #FFFFFF !important;
}

.stButton > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {
    border: 0 !important;
    box-shadow: 0 13px 30px rgba(8, 126, 139, 0.30);
    color: #FFFFFF !important;
    transform: translateY(-1px);
}

/* Standard Streamlit metrics */

[data-testid="stMetric"] {
    min-height: 8.5rem;
    padding: 1.2rem 1.25rem;
    border: 1px solid var(--cc-border);
    border-radius: 1rem;
    background:
        linear-gradient(
            145deg,
            rgba(255, 255, 255, 0.96),
            rgba(234, 246, 243, 0.82)
        );
    box-shadow: 0 9px 24px rgba(17, 78, 81, 0.08);
}

[data-testid="stMetricLabel"] p {
    color: #49666C !important;
    font-weight: 700 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] > div {
    overflow: hidden;
    color: #526D73 !important;
    font-weight: 800 !important;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* Traveller profile */

.cc-profile {
    overflow: hidden;
    margin: 1rem 0 2.5rem;
    border: 1px solid var(--cc-border);
    border-radius: 1.4rem;
    background: rgba(255, 255, 255, 0.94);
    box-shadow: 0 16px 38px rgba(17, 78, 81, 0.11);
}

.cc-profile-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 1.2rem 1.35rem;
    background:
        linear-gradient(
            110deg,
            rgba(7, 90, 101, 0.08),
            rgba(36, 150, 109, 0.10),
            rgba(247, 231, 198, 0.24)
        );
    border-bottom: 1px solid var(--cc-border);
}

.cc-profile-heading {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.cc-profile-icon {
    display: grid;
    flex: 0 0 auto;
    place-items: center;
    width: 2.8rem;
    height: 2.8rem;
    border-radius: 0.9rem;
    background:
        linear-gradient(
            135deg,
            var(--cc-ocean),
            var(--cc-green)
        );
    color: #FFFFFF;
    font-size: 1.25rem;
    box-shadow: 0 8px 18px rgba(8, 126, 139, 0.20);
}

.cc-profile-heading h3 {
    margin: 0 !important;
    padding: 0 !important;
    border: 0 !important;
    color: var(--cc-ink) !important;
    font-size: 1.15rem !important;
}

.cc-profile-heading p {
    margin: 0.2rem 0 0;
    color: var(--cc-muted) !important;
    font-size: 0.84rem;
}

.cc-profile-status {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    flex: 0 0 auto;
    padding: 0.5rem 0.75rem;
    border: 1px solid rgba(36, 150, 109, 0.22);
    border-radius: 999px;
    background: var(--cc-green-light);
    color: var(--cc-green-dark) !important;
    font-size: 0.78rem;
    font-weight: 800;
}

.cc-profile-status-dot {
    width: 0.5rem;
    height: 0.5rem;
    border-radius: 50%;
    background: var(--cc-green);
    box-shadow: 0 0 0 0.2rem rgba(36, 150, 109, 0.13);
}

.cc-profile-stats {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1rem;
    padding: 1.25rem 1.35rem 0;
}

.cc-profile-stat {
    position: relative;
    overflow: hidden;
    min-height: 7.8rem;
    padding: 1.1rem;
    border: 1px solid var(--cc-border);
    border-radius: 1rem;
    background:
        linear-gradient(
            145deg,
            #FFFFFF,
            #F0F8F6
        );
}

.cc-profile-stat::after {
    content: "";
    position: absolute;
    right: -1.8rem;
    bottom: -2.2rem;
    width: 5rem;
    height: 5rem;
    border-radius: 50%;
    background: rgba(8, 126, 139, 0.07);
}

.cc-profile-stat-icon {
    margin-bottom: 0.55rem;
    font-size: 1.15rem;
}

.cc-profile-stat-label {
    color: var(--cc-muted) !important;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}

.cc-profile-stat-value {
    position: relative;
    z-index: 1;
    margin-top: 0.25rem;
    color: var(--cc-ink) !important;
    font-size: clamp(1.55rem, 3vw, 2rem);
    font-weight: 850;
    letter-spacing: -0.04em;
}

.cc-profile-details {
    margin: 1.25rem 1.35rem 1.35rem;
    padding: 1.25rem;
    border: 1px solid rgba(247, 231, 198, 0.95);
    border-radius: 1rem;
    background:
        linear-gradient(
            135deg,
            rgba(255, 249, 236, 0.92),
            rgba(255, 255, 255, 0.96)
        );
}

.cc-profile-details-title {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    margin-bottom: 1rem;
    color: var(--cc-ocean-dark) !important;
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.cc-profile-detail-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.75rem;
}

.cc-profile-detail {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    min-width: 0;
    padding: 0.85rem;
    border: 1px solid rgba(215, 231, 228, 0.9);
    border-radius: 0.85rem;
    background: rgba(255, 255, 255, 0.80);
}

.cc-profile-detail-icon {
    display: grid;
    flex: 0 0 auto;
    place-items: center;
    width: 2.35rem;
    height: 2.35rem;
    border-radius: 0.75rem;
    background: var(--cc-ocean-light);
    font-size: 1rem;
}

.cc-profile-detail-content {
    min-width: 0;
}

.cc-profile-detail-label {
    color: var(--cc-muted) !important;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
}

.cc-profile-detail-value {
    overflow: hidden;
    margin-top: 0.12rem;
    color: var(--cc-ink) !important;
    font-size: 0.92rem;
    font-weight: 750;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.cc-profile-interests {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--cc-border);
}

.cc-profile-interests-label {
    margin-bottom: 0.65rem;
    color: var(--cc-muted) !important;
    font-size: 0.75rem;
    font-weight: 750;
    text-transform: uppercase;
}

.cc-profile-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.cc-profile-chip {
    display: inline-flex;
    align-items: center;
    padding: 0.48rem 0.72rem;
    border: 1px solid rgba(8, 126, 139, 0.18);
    border-radius: 999px;
    background: var(--cc-ocean-light);
    color: var(--cc-ocean-dark) !important;
    font-size: 0.8rem;
    font-weight: 750;
}

/* Alerts */

[data-testid="stAlert"] {
    border-radius: 0.9rem !important;
    box-shadow: 0 8px 22px rgba(26, 77, 79, 0.07);
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] li,
[data-testid="stAlert"] div {
    color: #3F6269 !important;
}

/* Expanders */

[data-testid="stExpander"] {
    overflow: hidden;
    border: 1px solid var(--cc-border) !important;
    border-radius: 0.9rem !important;
    background: rgba(255, 255, 255, 0.90);
}

[data-testid="stExpander"] summary {
    color: var(--cc-ink) !important;
    font-weight: 700;
}

[data-testid="stExpander"] summary p {
    color: var(--cc-ink) !important;
}

/* Dataframes */

[data-testid="stDataFrame"],
[data-testid="stTable"] {
    overflow: hidden;
    border: 1px solid var(--cc-border);
    border-radius: 1rem;
    box-shadow: 0 8px 24px rgba(25, 83, 84, 0.06);
}

/* Progress bars */

[data-testid="stProgress"] > div > div > div > div {
    background:
        linear-gradient(
            90deg,
            var(--cc-ocean),
            var(--cc-green)
        ) !important;
}

hr {
    border-color: var(--cc-border) !important;
}

/* Footer */

.cc-footer {
    margin-top: 2.8rem;
    padding: 1.2rem;
    border: 1px solid var(--cc-sand);
    border-radius: 1rem;
    background: var(--cc-sand-light);
    color: var(--cc-muted) !important;
    font-size: 0.82rem;
    line-height: 1.6;
    text-align: center;
}

.cc-footer strong {
    color: var(--cc-ocean-dark) !important;
}

/* Responsive layout */

@media (max-width: 900px) {
    .cc-feature-strip {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 780px) {
    [data-testid="stMainBlockContainer"] {
        padding-right: 1rem;
        padding-left: 1rem;
    }

    .cc-hero {
        padding: 2rem 1.35rem;
        border-radius: 1.25rem;
    }

    .cc-hero h1 {
        font-size: 2.25rem !important;
    }

    .cc-hero p {
        font-size: 0.96rem;
    }

    .cc-profile-header {
        align-items: flex-start;
        flex-direction: column;
    }

    .cc-profile-stats {
        grid-template-columns: 1fr;
    }

    .cc-profile-stat {
        min-height: auto;
    }

    .cc-profile-detail-grid {
        grid-template-columns: 1fr;
    }

    [data-testid="stMetric"] {
        min-height: auto;
    }
}

@media (max-width: 520px) {
    .cc-feature-strip {
        grid-template-columns: 1fr;
    }

    .cc-hero {
        padding: 1.7rem 1.1rem;
    }

    .cc-hero h1 {
        font-size: 1.95rem !important;
    }

    .cc-profile-header,
    .cc-profile-stats {
        padding-right: 1rem;
        padding-left: 1rem;
    }

    .cc-profile-details {
        margin-right: 1rem;
        margin-left: 1rem;
    }
}
</style>
""",
        unsafe_allow_html=True,
    )


def render_sidebar_brand() -> None:
    """Display the Ceylon Compass identity in the sidebar."""

    sidebar_html = """
<div class="cc-sidebar-brand">
<div class="cc-sidebar-mark">🧭</div>
<h3>Ceylon Compass</h3>
<p>Your intelligent Sri Lanka journey planner</p>
</div>
<div class="cc-sidebar-note">
<strong>Free and explainable planning</strong>
<br>
Live weather • Smart ranking • Optimized routes
</div>
"""

    st.sidebar.markdown(
        sidebar_html,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    """Display the main Ceylon Compass hero section."""

    hero_html = """
<section class="cc-hero">
<div class="cc-hero-eyebrow">🇱🇰 Explore Sri Lanka intelligently</div>
<h1>Your island journey, planned around you.</h1>
<p>Discover destinations that match your interests, budget and travel style. Then turn them into a weather-aware, route-optimized Sri Lankan itinerary.</p>
</section>
<div class="cc-feature-strip">
<div class="cc-feature">✨ Personal ranking</div>
<div class="cc-feature">☀️ Live weather</div>
<div class="cc-feature">🗺️ Optimized route</div>
<div class="cc-feature">💰 Clear budget</div>
</div>
"""

    st.markdown(
        hero_html,
        unsafe_allow_html=True,
    )


def render_section_intro(
    title: str,
    description: str,
    icon: str,
) -> None:
    """Display a consistent introduction for an application section."""

    safe_title = escape(title)
    safe_description = escape(description)
    safe_icon = escape(icon)

    section_html = f"""
<div class="cc-section-intro">
<div class="cc-section-label"><span>{safe_icon}</span><span>Ceylon Compass</span></div>
<h2>{safe_title}</h2>
<p>{safe_description}</p>
</div>
"""

    st.markdown(
        section_html,
        unsafe_allow_html=True,
    )


def render_traveller_profile(
    *,
    starting_point: str,
    trip_days: int,
    budget_usd: float,
    daily_budget_usd: float,
    travel_style: str,
    crowd_preference: str,
    transport: str,
    interests: Iterable[str],
) -> None:
    """Render a polished traveller-profile summary."""

    safe_starting_point = escape(str(starting_point))
    safe_trip_days = int(trip_days)
    safe_budget = float(budget_usd)
    safe_daily_budget = float(daily_budget_usd)
    safe_travel_style = escape(str(travel_style))
    safe_crowd_preference = escape(str(crowd_preference))
    safe_transport = escape(str(transport))

    interest_chips = "".join(
        (
            '<span class="cc-profile-chip">'
            f"✨ {escape(str(interest))}"
            "</span>"
        )
        for interest in interests
    )

    profile_html = f"""
<section class="cc-profile">
<div class="cc-profile-header">
<div class="cc-profile-heading">
<div class="cc-profile-icon">🧳</div>
<div>
<h3>Your journey profile</h3>
<p>The travel preferences used to build your personalized itinerary.</p>
</div>
</div>
<div class="cc-profile-status">
<span class="cc-profile-status-dot"></span>
Profile ready
</div>
</div>
<div class="cc-profile-stats">
<div class="cc-profile-stat">
<div class="cc-profile-stat-icon">🗓️</div>
<div class="cc-profile-stat-label">Trip duration</div>
<div class="cc-profile-stat-value">{safe_trip_days} days</div>
</div>
<div class="cc-profile-stat">
<div class="cc-profile-stat-icon">💳</div>
<div class="cc-profile-stat-label">Total budget</div>
<div class="cc-profile-stat-value">${safe_budget:,.0f}</div>
</div>
<div class="cc-profile-stat">
<div class="cc-profile-stat-icon">☀️</div>
<div class="cc-profile-stat-label">Daily budget</div>
<div class="cc-profile-stat-value">${safe_daily_budget:,.2f}</div>
</div>
</div>
<div class="cc-profile-details">
<div class="cc-profile-details-title">🪪 Travel profile details</div>
<div class="cc-profile-detail-grid">
<div class="cc-profile-detail">
<div class="cc-profile-detail-icon">📍</div>
<div class="cc-profile-detail-content">
<div class="cc-profile-detail-label">Starting point</div>
<div class="cc-profile-detail-value">{safe_starting_point}</div>
</div>
</div>
<div class="cc-profile-detail">
<div class="cc-profile-detail-icon">🎒</div>
<div class="cc-profile-detail-content">
<div class="cc-profile-detail-label">Travel style</div>
<div class="cc-profile-detail-value">{safe_travel_style}</div>
</div>
</div>
<div class="cc-profile-detail">
<div class="cc-profile-detail-icon">👥</div>
<div class="cc-profile-detail-content">
<div class="cc-profile-detail-label">Crowd preference</div>
<div class="cc-profile-detail-value">{safe_crowd_preference}</div>
</div>
</div>
<div class="cc-profile-detail">
<div class="cc-profile-detail-icon">🚗</div>
<div class="cc-profile-detail-content">
<div class="cc-profile-detail-label">Preferred transport</div>
<div class="cc-profile-detail-value">{safe_transport}</div>
</div>
</div>
</div>
<div class="cc-profile-interests">
<div class="cc-profile-interests-label">Selected interests</div>
<div class="cc-profile-chips">{interest_chips}</div>
</div>
</div>
</section>
"""

    st.markdown(
        profile_html,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Display the application footer."""

    footer_html = """
<div class="cc-footer">
<strong>Ceylon Compass V1</strong>
&nbsp;•&nbsp;
Explainable recommendations
&nbsp;•&nbsp;
Weather-aware planning
&nbsp;•&nbsp;
Route optimization
&nbsp;•&nbsp;
Built for discovering Sri Lanka
</div>
"""

    st.markdown(
        footer_html,
        unsafe_allow_html=True,
    )