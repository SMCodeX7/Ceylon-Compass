"""Visual theme and reusable UI components for Ceylon Compass."""

from html import escape
from textwrap import dedent
from typing import Iterable

import streamlit as st


def apply_ceylon_compass_theme() -> None:
    """Apply the tropical light theme across the application."""

    st.markdown(
        """
<style>
:root {
    --cc-ocean: #176B87;
    --cc-ocean-dark: #124E63;
    --cc-ocean-light: #E8F3F7;

    --cc-green: #2F7D5A;
    --cc-green-dark: #256246;
    --cc-green-light: #EAF5EF;

    --cc-sand: #E8D8B5;
    --cc-sand-light: #FAF7EF;

    --cc-ink: #1F2933;
    --cc-muted: #52636F;
    --cc-border: #D9E2E7;

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
    background: #F8FAFB;
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
    font-weight: 700 !important;
    letter-spacing: -0.015em;
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
    border-right: 1px solid rgba(255,255,255,0.15);
    background: var(--cc-ocean-dark);
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
        linear-gradient(
            120deg,
            var(--cc-ocean-dark),
            var(--cc-ocean)
        );
    box-shadow:
        0 12px 30px rgba(31, 41, 51, 0.14);
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

/* Recommendation cards */

.cc-recommendation-card {
    margin: 0 0 1rem;
    border: 1px solid var(--cc-border);
    border-radius: 1rem;
    background: var(--cc-white);
    box-shadow: 0 10px 26px rgba(20, 74, 78, 0.08);
}

.cc-recommendation-card > summary {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.2rem;
    color: var(--cc-ink);
    cursor: pointer;
    list-style: none;
}

.cc-recommendation-card > summary::-webkit-details-marker,
.cc-recommendation-weights > summary::-webkit-details-marker {
    display: none;
}

.cc-recommendation-rank {
    display: flex;
    flex: 0 0 auto;
    min-width: 4.2rem;
    flex-direction: column;
    gap: 0.15rem;
    padding-right: 1rem;
    border-right: 1px solid var(--cc-border);
}

.cc-recommendation-rank span {
    color: var(--cc-muted);
    font-size: 0.7rem;
    font-weight: 700;
    line-height: 1.2;
}

.cc-recommendation-rank strong {
    color: var(--cc-ocean-dark);
    font-size: 1.35rem;
    line-height: 1;
}

.cc-recommendation-summary {
    display: flex;
    min-width: 0;
    flex-direction: column;
    gap: 0.15rem;
}

.cc-recommendation-summary strong {
    overflow: hidden;
    color: var(--cc-ink);
    font-size: 1rem;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.cc-recommendation-summary span {
    color: var(--cc-muted);
    font-size: 0.84rem;
}

.cc-recommendation-body {
    padding: 1.35rem 1.2rem 1.2rem;
    border-top: 1px solid var(--cc-border);
}

.cc-recommendation-heading {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1.5rem;
    margin-bottom: 1.25rem;
}

.cc-recommendation-heading h3 {
    margin: 0 !important;
    padding: 0 !important;
    border: 0 !important;
    color: var(--cc-ink) !important;
    font-size: 1.45rem !important;
    line-height: 1.2 !important;
}

.cc-recommendation-heading p {
    margin: 0.35rem 0 0;
    color: var(--cc-muted) !important;
    font-size: 0.92rem;
}

.cc-recommendation-score {
    flex: 0 0 auto;
    min-width: 13rem;
    padding-left: 1rem;
    border-left: 1px solid var(--cc-border);
}

.cc-recommendation-score-heading,
.cc-recommendation-score-heading span,
.cc-recommendation-fact span {
    display: block;
    color: var(--cc-muted);
    font-size: 0.76rem;
    font-weight: 700;
}

.cc-recommendation-score-heading {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 0.75rem;
}

.cc-recommendation-score-heading strong {
    display: block;
    color: var(--cc-ocean-dark);
    font-size: 1.65rem;
    line-height: 1.1;
}

.cc-recommendation-score-track {
    height: 0.45rem;
    margin-top: 0.65rem;
    overflow: hidden;
    border-radius: 999px;
    background: var(--cc-ocean-light);
}

.cc-recommendation-score-track span {
    display: block;
    height: 100%;
    border-radius: inherit;
    background: var(--cc-ocean);
}

.cc-recommendation-score small {
    display: block;
    margin-top: 0.35rem;
    color: var(--cc-muted);
    font-size: 0.7rem;
}

.cc-recommendation-facts {
    display: grid;
    gap: 0.75rem;
}

.cc-recommendation-facts {
    grid-template-columns: repeat(4, minmax(0, 1fr));
    margin-bottom: 0.85rem;
}

.cc-recommendation-fact {
    min-width: 0;
}

.cc-recommendation-fact strong {
    display: block;
    margin-top: 0.25rem;
    overflow: hidden;
    color: var(--cc-ink);
    font-size: 0.96rem;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.cc-recommendation-explanation {
    margin-top: 1.35rem;
    padding-top: 1.1rem;
    border-top: 1px solid var(--cc-border);
}

.cc-explanation-block {
    padding: 1rem;
    border: 1px solid var(--cc-border);
    background: var(--cc-sand-light);
}

.cc-explanation-block:first-child {
    border-radius: 0.8rem 0.8rem 0 0;
}

.cc-explanation-block + .cc-explanation-block {
    border-top: 0;
}

.cc-explanation-block:last-child {
    border-radius: 0 0 0.8rem 0.8rem;
}

.cc-explanation-block h4 {
    margin: 0 0 0.55rem;
    color: var(--cc-ink) !important;
    font-size: 1rem !important;
}

.cc-explanation-lead {
    margin: 0 0 0.65rem;
    color: var(--cc-muted) !important;
    font-size: 0.9rem;
    line-height: 1.5;
}

.cc-explanation-block ul {
    margin: 0;
    padding-left: 1.1rem;
}

.cc-explanation-block li {
    margin-bottom: 0.4rem;
    color: var(--cc-muted) !important;
    line-height: 1.5;
}

.cc-explanation-block li:last-child {
    margin-bottom: 0;
}

.cc-explanation-factors {
    border-top: 1px solid var(--cc-border);
}

.cc-explanation-factor {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    gap: 0.2rem 1rem;
    align-items: baseline;
    padding: 0.65rem 0;
    border-bottom: 1px solid var(--cc-border);
}

.cc-explanation-factor:last-child {
    border-bottom: 0;
    padding-bottom: 0;
}

.cc-explanation-factor span {
    color: var(--cc-muted);
    font-size: 0.86rem;
}

.cc-explanation-factor strong {
    color: var(--cc-ocean-dark);
    font-size: 0.95rem;
    text-align: right;
}

.cc-explanation-factor small {
    grid-column: 2;
    color: var(--cc-muted);
    font-size: 0.76rem;
    text-align: right;
}

.cc-explanation-limitations {
    background: var(--cc-white);
}

.cc-recommendation-weights {
    margin-top: 1.1rem;
    border-top: 1px solid var(--cc-border);
}

.cc-recommendation-weights > summary {
    padding: 0.85rem 0 0.35rem;
    color: var(--cc-ocean-dark);
    cursor: pointer;
    font-size: 0.86rem;
    font-weight: 750;
    list-style: none;
}

.cc-recommendation-weight-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.5rem 1rem;
    padding: 0.45rem 0 0.15rem;
    color: var(--cc-muted);
    font-size: 0.82rem;
}

.cc-recommendation-weight-grid strong {
    color: var(--cc-ink);
}

/* Route timeline */

.cc-route-timeline {
    position: relative;
    display: grid;
    gap: 1rem;
    margin: 1.2rem 0 1.5rem;
}

.cc-route-timeline::before {
    content: "";
    position: absolute;
    top: 1.25rem;
    bottom: 1.25rem;
    left: 1.25rem;
    width: 2px;
    background: var(--cc-border);
}

.cc-route-stop {
    position: relative;
    display: grid;
    grid-template-columns: 2.5rem minmax(0, 1fr);
    gap: 0.85rem;
    align-items: start;
}

.cc-route-marker {
    position: relative;
    z-index: 1;
    display: grid;
    place-items: center;
    width: 2.5rem;
    height: 2.5rem;
    border: 4px solid #F8FAFB;
    border-radius: 50%;
    background: var(--cc-ocean);
    color: #FFFFFF;
    font-size: 0.85rem;
    font-weight: 800;
    box-shadow: 0 0 0 1px var(--cc-ocean);
}

.cc-route-card {
    min-width: 0;
    padding: 1.1rem 1.2rem;
    border: 1px solid var(--cc-border);
    border-radius: 0.85rem;
    background: var(--cc-white);
    box-shadow: 0 7px 20px rgba(25, 83, 84, 0.06);
}

.cc-route-card-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
}

.cc-route-card h3 {
    margin: 0.15rem 0 0 !important;
    padding: 0 !important;
    border: 0 !important;
    color: var(--cc-ink) !important;
    font-size: 1.15rem !important;
}

.cc-route-stop-order,
.cc-route-detail span,
.cc-route-score span {
    margin: 0;
    color: var(--cc-muted);
    font-size: 0.76rem;
    font-weight: 750;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.cc-route-score {
    flex: 0 0 auto;
    text-align: right;
}

.cc-route-score strong {
    display: block;
    margin-top: 0.2rem;
    color: var(--cc-green);
    font-size: 1.15rem;
}

.cc-route-details {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.75rem;
    margin-top: 1rem;
    padding-top: 0.9rem;
    border-top: 1px solid var(--cc-border);
}

.cc-route-detail {
    min-width: 0;
}

.cc-route-detail strong {
    display: block;
    margin-top: 0.25rem;
    overflow: hidden;
    color: var(--cc-ink);
    font-size: 0.95rem;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.cc-route-distance {
    padding-left: 0.75rem;
    border-left: 2px solid var(--cc-green);
}

/* Itinerary */

.cc-itinerary-container {
    display: grid;
    gap: 1rem;
    margin: 1.2rem 0 1.5rem;
}

.cc-itinerary-day-card,
.cc-itinerary-card {
    min-width: 0;
    padding: 1.1rem 1.2rem;
    border: 1px solid var(--cc-border);
    border-radius: 1rem;
    background: var(--cc-white);
    box-shadow: 0 7px 20px rgba(25, 83, 84, 0.06);
}

.cc-itinerary-destination,
.cc-itinerary-item {
    min-width: 0;
    margin-top: 1rem;
    padding-top: 0.9rem;
    border-top: 1px solid var(--cc-border);
}

.cc-itinerary-destination h3 {
    margin: 0 !important;
    padding: 0 !important;
    border: 0 !important;
    color: var(--cc-ink) !important;
    font-size: 1.15rem !important;
    line-height: 1.25 !important;
}

.cc-itinerary-activity-list {
    margin: 0.75rem 0 0;
    padding-left: 1.1rem;
    color: var(--cc-muted);
    line-height: 1.5;
}

.cc-itinerary-header {
    color: inherit;
}

.cc-itinerary-details {
    min-width: 0;
}

.cc-itinerary-duration,
.cc-itinerary-cost {
    display: block;
    margin-top: 0.25rem;
    font-size: 0.95rem;
    font-weight: 750;
}

.cc-itinerary-duration {
    color: var(--cc-ocean);
}

.cc-itinerary-cost {
    color: var(--cc-green);
}

/* Budget presentation */

.cc-budget-container {
    min-width: 0;
}

.cc-budget-summary {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.8rem;
    margin: 1rem 0 1.5rem;
}

.cc-budget-summary-card {
    min-width: 0;
    padding: 1.1rem 1.2rem;
    border: 1px solid var(--cc-border);
    border-radius: 1rem;
    background: var(--cc-white);
    box-shadow: 0 7px 20px rgba(25, 83, 84, 0.06);
}

.cc-budget-summary-card span,
.cc-budget-breakdown-row span,
.cc-budget-expense-category span {
    color: var(--cc-muted);
    font-size: 0.76rem;
    font-weight: 700;
}

.cc-budget-summary-card strong {
    display: block;
    margin-top: 0.25rem;
    color: var(--cc-ink);
    font-size: 1.35rem;
    line-height: 1.2;
}

.cc-budget-total-cost,
.cc-budget-total {
    border-left: 3px solid var(--cc-ocean);
    background: var(--cc-ocean-light);
}

.cc-budget-total-cost strong,
.cc-budget-total strong {
    color: var(--cc-ocean);
}

.cc-budget-breakdown {
    display: grid;
    gap: 0.75rem;
    margin: 1rem 0 1.5rem;
}

.cc-budget-breakdown-row {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    gap: 1rem;
    align-items: baseline;
    padding: 0.85rem 1rem;
    border: 1px solid var(--cc-border);
    border-radius: 0.85rem;
    background: var(--cc-white);
}

.cc-budget-item {
    min-width: 0;
}

.cc-budget-breakdown-row strong {
    color: var(--cc-ink);
    font-size: 0.95rem;
    text-align: right;
}

.cc-budget-expense-category {
    display: grid;
    gap: 0.25rem;
    min-width: 0;
    padding: 0.85rem 1rem;
    border: 1px solid var(--cc-border);
    border-radius: 0.85rem;
    background: rgba(255, 255, 255, 0.88);
}

.cc-budget-expense-category strong {
    color: var(--cc-ink);
    font-size: 0.95rem;
}

@media (max-width: 640px) {
    .cc-route-card-header,
    .cc-route-details {
        grid-template-columns: 1fr;
    }

    .cc-route-card-header {
        display: grid;
    }

    .cc-route-score {
        text-align: left;
    }

    .cc-route-details {
        display: grid;
    }

    .cc-itinerary-day-card {
        padding: 1rem;
    }

    .cc-budget-summary {
        grid-template-columns: 1fr;
    }

    .cc-budget-breakdown-row {
        grid-template-columns: 1fr;
        gap: 0.25rem;
    }

    .cc-budget-breakdown-row strong {
        text-align: left;
    }
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
    gap: 1.5rem;
    padding: 1.5rem 1.6rem;
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

.cc-profile-heading h3 {
    margin: 0 !important;
    padding: 0 !important;
    border: 0 !important;
    color: var(--cc-ink) !important;
    font-size: 1.3rem !important;
}

.cc-profile-heading p {
    margin: 0.3rem 0 0;
    color: var(--cc-muted) !important;
    font-size: 0.9rem;
    line-height: 1.5;
}

.cc-profile-status {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    flex: 0 0 auto;
    padding: 0.55rem 0.9rem;
    border: 1px solid rgba(36, 150, 109, 0.22);
    border-radius: 999px;
    background: var(--cc-green-light);
    color: var(--cc-green-dark) !important;
    font-size: 0.82rem;
    font-weight: 750;
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
    min-height: 8.8rem;
    padding: 1.25rem  1.35rem;
    border: 1px solid var(--cc-border);
    border-radius: 1rem;
    background:
        linear-gradient(
            145deg,
            #FFFFFF,
            #F0F8F6
        );
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.cc-profile-stat-label {
    color: var(--cc-muted) !important;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0;
    text-transformation: none;
}

.cc-profile-stat-value {
    position: relative;
    z-index: 1;
    margin-top: 0.8rem;
    color: var(--cc-ink) !important;
    font-size: clamp(1.7rem, 3vw, 2.1rem);
    font-weight: 800;
    letter-spacing: -0.025em;
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
    gap: 1rem;
}

.cc-profile-detail {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    min-width: 0;
    padding: 1rem;
    border: 1px solid var(--cc-border);
    border-radius: 1rem;
    background: rgba(255, 255, 255, 0.92);
    transition:
        transform 160ms ease,
        box-shadow 160ms ease;
}

.cc-profile-detail-content {
    min-width: 0;
}

.cc-profile-detail-label {
    color: var(--cc-muted) !important;
    font-size: 0.82rem;
    font-weight: 650;
    letter-spacing: 0;
    text-transform: none;
}

.cc-profile-detail-value {
    overflow: hidden;
    margin-top: 0.25rem;
    color: var(--cc-ink) !important;
    font-size: 1rem;
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

    .cc-recommendation-facts {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .cc-recommendation-weight-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
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

    .cc-recommendation-card > summary {
        align-items: flex-start;
        flex-direction: column;
        gap: 0.35rem;
    }

    .cc-recommendation-body {
        padding: 1.1rem;
    }

    .cc-recommendation-heading {
        flex-direction: column;
        gap: 1rem;
    }

    .cc-recommendation-score {
        width: 100%;
        padding-top: 0.75rem;
        padding-left: 0;
        border-top: 1px solid var(--cc-border);
        border-left: 0;
    }

    .cc-recommendation-rank {
        padding-right: 0;
        border-right: 0;
    }

    .cc-recommendation-facts,
    .cc-recommendation-weight-grid {
        grid-template-columns: 1fr;
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

    hero_html = dedent(
        """
        <section class="cc-hero">
            <div class="cc-hero-eyebrow">
                Ceylon Compass
            </div>

            <h1>
                Intelligent travel planning for Sri Lanka.
            </h1>

            <p>
                Create personalized travel plans using destination recommendations,
                route optimization, weather information, and budget-aware planning.
            </p>
        </section>

        <div class="cc-feature-strip">

            <div class="cc-feature">
                Personalized recommendations
            </div>

            <div class="cc-feature">
                Weather-aware planning
            </div>

            <div class="cc-feature">
                Optimized travel routes
            </div>

            <div class="cc-feature">
                Budget estimation
            </div>

        </div>
        """
    )

    st.html(hero_html)


def render_section_intro(
    title: str,
    description: str,
    icon: str = "",
) -> None:
    """Display a consistent introduction for an application section."""

    safe_title = escape(title)
    safe_description = escape(description)

    section_html = f"""
<div class="cc-section-intro">
<div class="cc-section-label">
    <span>Ceylon Compass</span>
</div>

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
            f"{escape(str(interest))}"
            "</span>"
        )
        for interest in interests
    )

    profile_html = f"""
<section class="cc-profile">

<div class="cc-profile-header">

<div class="cc-profile-heading">

<div>
<h3>Traveller profile</h3>
<p>Your travel preferences and constraints used for recommendation generation.</p>
</div>

</div>

<div class="cc-profile-status">
<span class="cc-profile-status-dot"></span>
Ready for recommendations
</div>

</div>


<div class="cc-profile-stats">

<div class="cc-profile-stat">
<div class="cc-profile-stat-label">
Trip duration
</div>
<div class="cc-profile-stat-value">
{safe_trip_days} days
</div>
</div>


<div class="cc-profile-stat">
<div class="cc-profile-stat-label">
Total budget
</div>
<div class="cc-profile-stat-value">
${safe_budget:,.0f}
</div>
</div>


<div class="cc-profile-stat">
<div class="cc-profile-stat-label">
Daily budget
</div>
<div class="cc-profile-stat-value">
${safe_daily_budget:,.0f}/day
</div>
</div>

</div>


<div class="cc-profile-details">

<div class="cc-profile-details-title">
Journey preferences
</div>


<div class="cc-profile-detail-grid">


<div class="cc-profile-detail">

<div class="cc-profile-detail-content">

<div class="cc-profile-detail-label">
Starting point
</div>

<div class="cc-profile-detail-value">
{safe_starting_point}
</div>

</div>

</div>


<div class="cc-profile-detail">

<div class="cc-profile-detail-content">

<div class="cc-profile-detail-label">
Travel style
</div>

<div class="cc-profile-detail-value">
{safe_travel_style}
</div>

</div>

</div>


<div class="cc-profile-detail">

<div class="cc-profile-detail-content">

<div class="cc-profile-detail-label">
Crowd preference
</div>

<div class="cc-profile-detail-value">
{safe_crowd_preference}
</div>

</div>

</div>


<div class="cc-profile-detail">

<div class="cc-profile-detail-content">

<div class="cc-profile-detail-label">
Preferred transport
</div>

<div class="cc-profile-detail-value">
{safe_transport}
</div>

</div>

</div>


</div>


<div class="cc-profile-interests">

<div class="cc-profile-interests-label">
Selected interests
</div>

<div class="cc-profile-chips">
{interest_chips}
</div>

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