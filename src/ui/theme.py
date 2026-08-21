"""Visual theme and reusable UI components for Ceylon Compass."""

from html import escape

import streamlit as st


def apply_ceylon_compass_theme() -> None:
    """Apply the tropical light theme across the Streamlit application."""

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
    --cc-danger: #B42318;
}

/* ----------------------------------------------------
   Main application
---------------------------------------------------- */

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

[data-testid="stToolbar"] {
    color: var(--cc-ink);
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

/* ----------------------------------------------------
   Sidebar
---------------------------------------------------- */

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

[data-testid="stSidebarContent"] {
    padding-top: 1rem;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #FFFFFF;
}

[data-testid="stSidebar"] button {
    color: #FFFFFF !important;
}

[data-testid="stSidebarCollapseButton"] svg {
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
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

/* ----------------------------------------------------
   Hero
---------------------------------------------------- */

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

/* ----------------------------------------------------
   Feature cards
---------------------------------------------------- */

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

/* ----------------------------------------------------
   Section introduction
---------------------------------------------------- */

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

/* ----------------------------------------------------
   Streamlit bordered containers
---------------------------------------------------- */

[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--cc-border) !important;
    border-radius: 1.25rem !important;
    background: rgba(255, 255, 255, 0.88);
    box-shadow: 0 12px 30px rgba(20, 74, 78, 0.09);
}

/* ----------------------------------------------------
   Form fields
---------------------------------------------------- */

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

[data-baseweb="popover"] {
    color: var(--cc-ink) !important;
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

/* ----------------------------------------------------
   Slider
---------------------------------------------------- */

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

/* ----------------------------------------------------
   Buttons
---------------------------------------------------- */

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

.stButton > button:focus,
[data-testid="stFormSubmitButton"] > button:focus {
    color: #FFFFFF !important;
    box-shadow:
        0 0 0 0.2rem rgba(8, 126, 139, 0.18),
        0 13px 30px rgba(8, 126, 139, 0.24);
}

/* ----------------------------------------------------
   Metrics
---------------------------------------------------- */

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

[data-testid="stMetricValue"] {
    color: #526D73 !important;
    font-weight: 800 !important;
}

[data-testid="stMetricValue"] > div {
    overflow: hidden;
    color: #526D73 !important;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* ----------------------------------------------------
   Alerts
---------------------------------------------------- */

[data-testid="stAlert"] {
    border-radius: 0.9rem !important;
    box-shadow: 0 8px 22px rgba(26, 77, 79, 0.07);
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] li,
[data-testid="stAlert"] div {
    color: #3F6269 !important;
}

[data-testid="stNotificationContentInfo"] {
    background: #E8F3FF !important;
}

[data-testid="stNotificationContentSuccess"] {
    background: var(--cc-green-light) !important;
}

[data-testid="stNotificationContentWarning"] {
    background: #FFFCE4 !important;
}

[data-testid="stNotificationContentError"] {
    background: #FFF0EE !important;
}

/* ----------------------------------------------------
   Expanders
---------------------------------------------------- */

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

/* ----------------------------------------------------
   Dataframes and tables
---------------------------------------------------- */

[data-testid="stDataFrame"] {
    overflow: hidden;
    border: 1px solid var(--cc-border);
    border-radius: 1rem;
    box-shadow: 0 8px 24px rgba(25, 83, 84, 0.06);
}

[data-testid="stTable"] {
    overflow: hidden;
    border: 1px solid var(--cc-border);
    border-radius: 1rem;
}

/* ----------------------------------------------------
   Progress bar
---------------------------------------------------- */

[data-testid="stProgress"] > div > div > div > div {
    background:
        linear-gradient(
            90deg,
            var(--cc-ocean),
            var(--cc-green)
        ) !important;
}

/* ----------------------------------------------------
   Dividers
---------------------------------------------------- */

hr {
    border-color: var(--cc-border) !important;
}

/* ----------------------------------------------------
   Spinner
---------------------------------------------------- */

[data-testid="stSpinner"] {
    color: var(--cc-ocean) !important;
}

/* ----------------------------------------------------
   Footer
---------------------------------------------------- */

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

/* ----------------------------------------------------
   Responsive design
---------------------------------------------------- */

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

    .cc-footer span {
        display: block;
        height: 0;
        overflow: hidden;
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