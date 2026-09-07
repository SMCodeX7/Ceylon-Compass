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
    /* Core palette */
    --cc-navy: #172B4D;
    --cc-navy-soft: #2D4366;
    --cc-teal: #168C87;
    --cc-teal-dark: #106B68;
    --cc-teal-soft: #E5F5F3;
    --cc-blue: #4F83CC;
    --cc-blue-soft: #EAF2FC;
    --cc-purple: #7667C7;
    --cc-purple-soft: #F0EEFC;
    --cc-green: #419B72;
    --cc-green-soft: #EAF7F0;
    --cc-yellow: #D29A32;
    --cc-yellow-soft: #FFF7DF;
    --cc-orange: #D8754D;
    --cc-orange-soft: #FFF0EA;
    --cc-slate: #6B7A90;
    --cc-slate-soft: #F1F4F8;

    /* Compatibility aliases used by existing components */
    --cc-ocean: var(--cc-teal);
    --cc-ocean-dark: var(--cc-navy);
    --cc-ocean-light: var(--cc-teal-soft);
    --cc-recommendation: var(--cc-teal);
    --cc-recommendation-soft: var(--cc-teal-soft);
    --cc-green-dark: #2F795A;
    --cc-green-light: var(--cc-green-soft);
    --cc-route: var(--cc-purple);
    --cc-route-soft: var(--cc-purple-soft);
    --cc-weather: var(--cc-blue);
    --cc-weather-soft: var(--cc-blue-soft);
    --cc-budget: var(--cc-green);
    --cc-budget-soft: #F1F8EF;
    --cc-information: var(--cc-slate);
    --cc-information-soft: var(--cc-slate-soft);
    --cc-sand: #E7D7B5;
    --cc-sand-light: #FFF9EE;

    /* Surfaces and text */
    --cc-ink: var(--cc-navy);
    --cc-muted: #687890;
    --cc-border: #DCE4ED;
    --cc-surface: #FFFFFF;
    --cc-white: var(--cc-surface);
    --cc-background: #F5F8FC;

    /* Layout rhythm */
    --cc-section-gap: 3.25rem;
    --cc-description-gap: 0.55rem;
    --cc-content-gap: 2rem;
    --cc-card-gap: 1rem;
    --cc-card-radius: 20px;
    --cc-card-padding: 1.35rem;
    --cc-shadow: 0 12px 30px rgba(31, 55, 89, 0.08);
    --cc-shadow-hover: 0 16px 36px rgba(31, 55, 89, 0.13);
}

html,
body,
[class*="css"] {
    font-family:
        "Plus Jakarta Sans",
        "Avenir Next",
        "Segoe UI",
        sans-serif;
    letter-spacing: 0;
}

[data-testid="stAppViewContainer"] {
    color: var(--cc-ink);
    background: var(--cc-background);
}

[data-testid="stHeader"] {
    background: rgba(247, 252, 251, 0.88);
    backdrop-filter: blur(12px);
}

[data-testid="stMainBlockContainer"] {
    max-width: 1240px;
    padding-top: 2.25rem;
    padding-bottom: 5.5rem;
}

[data-testid="stVerticalBlock"] {
    gap: 0.85rem;
}

[data-testid="stElementContainer"] {
    margin-bottom: 0.2rem;
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
    font-weight: 800 !important;
    letter-spacing: 0;
}

h2 {
    margin-top: var(--cc-section-gap) !important;
    padding-bottom: 0.85rem;
    border-bottom: 1px solid var(--cc-border);
}

h3 {
    margin-top: 1.75rem !important;
}

[data-testid="stCaptionContainer"] {
    margin-bottom: var(--cc-description-gap) !important;
    color: var(--cc-muted) !important;
    line-height: 1.55;
}

[data-testid="stMarkdownContainer"] {
    line-height: 1.6;
}

[data-testid="stAlert"] {
    margin: 0.7rem 0 1rem;
    border-radius: 0.85rem;
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
    border-radius: var(--cc-card-radius);
    background: rgba(255, 255, 255, 0.90);
    box-shadow: 0 7px 20px rgba(25, 83, 84, 0.07);
    color: var(--cc-ink) !important;
    font-size: 0.9rem;
    font-weight: 750;
    text-align: center;
}

/* Section headings */

.cc-section-intro {
    margin: var(--cc-section-gap) 0 var(--cc-content-gap);
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
    margin: 0.55rem 0 0;
    max-width: 760px;
    color: var(--cc-muted) !important;
    line-height: 1.65;
}

/* Bordered containers */

[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--cc-border) !important;
    border-radius: var(--cc-card-radius) !important;
    background: rgba(255, 255, 255, 0.78);
    box-shadow: var(--cc-shadow);
}

/* Form fields */

[data-testid="stWidgetLabel"] p {
    color: #3F6269 !important;
    font-weight: 650 !important;
}

[data-baseweb="select"] > div,
[data-testid="stNumberInputContainer"],
[data-testid="stTextInputRootElement"] {
    min-height: 3rem;
    border-color: var(--cc-border) !important;
    border-radius: 0.9rem !important;
    background: var(--cc-surface) !important;
    color: var(--cc-ink) !important;
    box-shadow: 0 3px 10px rgba(31, 55, 89, 0.04);
    transition: border-color 160ms ease, box-shadow 160ms ease;
}

[data-baseweb="select"] > div:focus-within,
[data-testid="stNumberInputContainer"]:focus-within,
[data-testid="stTextInputRootElement"]:focus-within {
    border-color: var(--cc-teal) !important;
    box-shadow: 0 0 0 3px rgba(22, 140, 135, 0.14) !important;
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
    border-radius: 0.6rem !important;
    background: var(--cc-teal) !important;
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
    width: 1.15rem;
    height: 1.15rem;
    border: 3px solid var(--cc-surface) !important;
    background: var(--cc-teal) !important;
    box-shadow: 0 2px 8px rgba(16, 107, 104, 0.28);
    transition: box-shadow 160ms ease, transform 160ms ease;
}

[data-testid="stSlider"] [role="slider"]:focus,
[data-testid="stSlider"] [role="slider"]:hover {
    box-shadow: 0 0 0 4px rgba(22, 140, 135, 0.16),
        0 3px 10px rgba(16, 107, 104, 0.28);
    transform: scale(1.05);
}

[data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: var(--cc-ink) !important;
}

[data-testid="stSlider"] div[data-baseweb="slider"] > div > div {
    background-color: var(--cc-teal) !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] > div:first-child {
    height: 0.35rem;
    border-radius: 999px;
    background: #DCEBEA !important;
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
    position: relative;
    overflow: hidden;
    min-height: 9rem;
    padding: 1.35rem 1.4rem 1.25rem;
    border: 1px solid var(--cc-border);
    border-radius: var(--cc-card-radius);
    background: var(--cc-surface);
    box-shadow: var(--cc-shadow);
    transition: transform 160ms ease, box-shadow 160ms ease;
}

[data-testid="stMetric"]::before {
    content: "";
    position: absolute;
    inset: 0 auto 0 0;
    width: 5px;
    background: var(--cc-teal);
}

[data-testid="stMetric"]:nth-child(2n)::before {
    background: var(--cc-blue);
}

[data-testid="stMetric"]:nth-child(3n)::before {
    background: var(--cc-green);
}

[data-testid="stMetric"]:hover {
    box-shadow: var(--cc-shadow-hover);
    transform: translateY(-2px);
}

[data-testid="stMetricLabel"] p {
    margin: 0 0 0.55rem !important;
    color: var(--cc-muted) !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.07em;
    text-transform: uppercase;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] > div {
    overflow: hidden;
    color: var(--cc-ink) !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    line-height: 1.15 !important;
    text-overflow: ellipsis;
    white-space: nowrap;
}

[data-testid="stMetricDelta"] {
    margin-top: 0.6rem;
    color: var(--cc-muted) !important;
    font-size: 0.78rem !important;
}

[data-testid="stMetricDelta"] svg {
    display: none;
}

/* Recommendation cards */

.cc-recommendation-card {
    position: relative;
    overflow: hidden;
    margin: 0.45rem 0 var(--cc-card-gap);
    border: 1px solid var(--cc-border);
    border-radius: var(--cc-card-radius);
    background: var(--cc-surface);
    box-shadow: var(--cc-shadow);
    transition: box-shadow 160ms ease, transform 160ms ease;
}

.cc-recommendation-card:hover {
    box-shadow: var(--cc-shadow-hover);
    transform: translateY(-1px);
}

.cc-recommendation-card::before {
    content: "";
    position: absolute;
    inset: 0 auto 0 0;
    width: 4px;
    background: var(--cc-recommendation);
}

.cc-recommendation-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.2rem 1.35rem 1.15rem 1.6rem;
    color: var(--cc-ink);
    cursor: pointer;
    list-style: none;
}

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
    padding: 1.35rem 1.35rem 1.45rem 1.6rem;
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
    gap: 0.65rem;
}

.cc-recommendation-facts {
    grid-template-columns: repeat(4, minmax(0, 1fr));
    margin-bottom: 0.85rem;
}

.cc-recommendation-fact {
    min-width: 0;
    padding: 0.75rem 0.85rem;
    border: 1px solid var(--cc-border);
    border-radius: 0.7rem;
    background: var(--cc-information-soft);
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
    padding: 1.1rem 1.15rem;
    border: 1px solid var(--cc-border);
    background: var(--cc-recommendation-soft);
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

.cc-explanation-empty {
    margin: 0;
    color: var(--cc-muted) !important;
    font-size: 0.9rem;
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
    background: var(--cc-information-soft);
}

.cc-recommendation-weights {
    margin-top: 1.3rem;
    padding-top: 0.15rem;
    border-top: 1px solid var(--cc-border);
}

.cc-recommendation-weights > summary {
    padding: 0.9rem 0 0.5rem;
    color: var(--cc-ocean-dark);
    cursor: pointer;
    font-size: 0.86rem;
    font-weight: 750;
    list-style: none;
}

.cc-recommendation-weight-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.55rem;
    padding: 0.55rem 0 0.2rem;
    color: var(--cc-muted);
    font-size: 0.82rem;
}

.cc-recommendation-weight-grid span {
    padding: 0.65rem 0.7rem;
    border: 1px solid var(--cc-border);
    border-radius: 0.7rem;
    background: var(--cc-information-soft);
}

.cc-recommendation-weight-grid strong {
    color: var(--cc-ink);
}

/* Route timeline */

.cc-route-timeline {
    position: relative;
    display: grid;
    gap: var(--cc-card-gap);
    margin: var(--cc-content-gap) 0 2.25rem;
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
    background: var(--cc-route);
    color: #FFFFFF;
    font-size: 0.85rem;
    font-weight: 800;
    box-shadow: 0 0 0 1px var(--cc-route);
}

.cc-route-card {
    min-width: 0;
    padding: 1.25rem 1.3rem;
    border: 1px solid var(--cc-border);
    border-left: 4px solid var(--cc-route);
    border-radius: var(--cc-card-radius);
    background: var(--cc-route-soft);
    box-shadow: var(--cc-shadow);
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

.cc-route-destination-label {
    display: block;
    margin-top: 0.7rem;
    color: var(--cc-muted);
    font-size: 0.76rem;
    font-weight: 750;
    letter-spacing: 0.04em;
    text-transform: uppercase;
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
    gap: var(--cc-card-gap);
    margin: var(--cc-content-gap) 0 2.25rem;
}

.cc-itinerary-day-card,
.cc-itinerary-card {
    min-width: 0;
    padding: 1.25rem 1.35rem;
    border: 1px solid var(--cc-border);
    border-radius: var(--cc-card-radius);
    background: var(--cc-surface);
    box-shadow: var(--cc-shadow);
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

.cc-itinerary-header {
    color: inherit;
}

.cc-itinerary-details {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 1rem;
    margin-top: 1rem;
    padding-top: 0.9rem;
    border-top: 1px solid var(--cc-border);
    min-width: 0;
}

.cc-itinerary-field {
    display: flex;
    min-width: 0;
    flex-direction: column;
    gap: 0.3rem;
}

.cc-itinerary-field strong {
    color: var(--cc-muted);
    font-size: 0.76rem;
    font-weight: 750;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.cc-itinerary-field > span {
    display: block;
    overflow: hidden;
    color: var(--cc-ink);
    font-size: 0.95rem;
    font-weight: 700;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.cc-itinerary-duration {
    color: var(--cc-ocean);
}

.cc-itinerary-cost {
    color: var(--cc-green);
}

.cc-itinerary-duration > span,
.cc-itinerary-cost > span {
    color: var(--cc-ink);
}

.cc-itinerary-field small {
    color: var(--cc-muted);
    font-size: 0.75rem;
}

.cc-itinerary-weather {
    grid-template-columns: repeat(2, minmax(0, 1fr));
}

/* Budget presentation */

/* Trip result summary */

.cc-trip-summary {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.65rem;
    margin: 0 0 var(--cc-content-gap);
}

.cc-trip-summary-card {
    position: relative;
    overflow: hidden;
    min-width: 0;
    padding: 1.15rem 1.2rem 1.1rem;
    border: 1px solid var(--cc-border);
    border-radius: var(--cc-card-radius);
    background: var(--cc-surface);
    box-shadow: var(--cc-shadow);
}

.cc-trip-summary-card::before {
    content: "";
    position: absolute;
    inset: 0 auto 0 0;
    width: 5px;
    background: var(--cc-teal);
}

.cc-trip-summary-card:nth-child(2)::before {
    background: var(--cc-blue);
}

.cc-trip-summary-card span {
    display: block;
    overflow: hidden;
    color: var(--cc-muted);
    font-size: 0.72rem;
    font-weight: 700;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.cc-trip-summary-card strong {
    display: block;
    overflow: hidden;
    margin-top: 0.25rem;
    color: var(--cc-ink);
    font-size: 1.45rem;
    font-weight: 800;
    line-height: 1.2;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.cc-trip-summary-card:first-child {
    border-left: 3px solid var(--cc-ocean);
}

.cc-trip-summary-card:nth-child(2) {
    border-left: 3px solid var(--cc-weather);
    background: var(--cc-weather-soft);
}

@media (max-width: 900px) {
    .cc-trip-summary {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 520px) {
    .cc-trip-summary {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

.cc-budget-container {
    min-width: 0;
    margin-top: var(--cc-content-gap);
    padding: 0.75rem 0 1rem;
    border-top: 4px solid var(--cc-budget);
}

.cc-budget-summary {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: var(--cc-card-gap);
    margin: 1.25rem 0 1.75rem;
}

.cc-budget-summary-card {
    position: relative;
    overflow: hidden;
    min-width: 0;
    padding: 1.3rem 1.35rem 1.25rem;
    border: 1px solid var(--cc-border);
    border-radius: var(--cc-card-radius);
    background: var(--cc-budget-soft);
    box-shadow: var(--cc-shadow);
}

.cc-budget-summary-card:nth-child(2)::before {
    background: var(--cc-yellow);
}

.cc-budget-summary-card:nth-child(3)::before {
    background: var(--cc-green);
}

.cc-budget-summary-card::before {
    content: "";
    position: absolute;
    inset: 0 auto 0 0;
    width: 5px;
    background: var(--cc-budget);
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
    font-size: 1.65rem;
    font-weight: 800;
    line-height: 1.2;
}

.cc-budget-total-cost,
.cc-budget-total {
    border-left: 3px solid var(--cc-budget);
    background: var(--cc-budget-soft);
}

.cc-budget-total-cost strong,
.cc-budget-total strong {
    color: var(--cc-budget);
}

.cc-budget-breakdown {
    display: grid;
    gap: 0.7rem;
    margin: 1.25rem 0 1.5rem;
}

.cc-budget-breakdown-row {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    gap: 1rem;
    align-items: baseline;
    padding: 1rem 1.15rem;
    border: 1px solid var(--cc-border);
    border-radius: 0.9rem;
    background: rgba(255, 255, 255, 0.96);
}

.cc-budget-activity {
    border-left: 4px solid var(--cc-teal);
}

.cc-budget-transport {
    border-left: 4px solid var(--cc-blue);
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
    padding: 0.7rem 0.85rem;
    border-bottom: 1px solid var(--cc-border);
    background: transparent;
}

.cc-budget-unmodelled {
    padding: 0.95rem 1.1rem 0.25rem;
    border: 1px solid var(--cc-border);
    border-radius: 0.9rem;
    background: var(--cc-information-soft);
}

.cc-budget-unmodelled-label {
    margin-bottom: 0.45rem;
    color: var(--cc-information);
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.07em;
    text-transform: uppercase;
}

.cc-budget-unmodelled .cc-budget-expense-category:last-child {
    border-bottom: 0;
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

    .cc-itinerary-details,
    .cc-itinerary-weather {
        grid-template-columns: repeat(2, minmax(0, 1fr));
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

    .cc-weather-fields {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

/* Traveller profile */

.cc-profile {
    overflow: hidden;
    margin: var(--cc-content-gap) 0 2.75rem;
    border: 1px solid var(--cc-border);
    border-radius: 1.4rem;
    background: rgba(255, 255, 255, 0.94);
    box-shadow: 0 16px 38px rgba(17, 78, 81, 0.11);
}

[data-testid="stDataFrame"] {
    overflow: hidden;
    margin: 1.4rem 0 1.75rem;
    border: 1px solid var(--cc-border);
    border-radius: 0.95rem;
    background: var(--cc-white);
    box-shadow: 0 8px 22px rgba(20, 74, 78, 0.07);
}

[data-testid="stDataFrame"] [role="columnheader"] {
    background: var(--cc-weather) !important;
    color: #FFFFFF !important;
    font-weight: 750 !important;
}

[data-testid="stDataFrame"] [role="gridcell"] {
    min-height: 2.35rem;
    border-bottom: 1px solid #E7EEF0 !important;
    color: var(--cc-ink) !important;
}

[data-testid="stDataFrame"] [role="row"]:nth-child(even) [role="gridcell"] {
    background: #F8FBFB !important;
}

.cc-weather-status-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.85rem 1.25rem;
    margin: 1.25rem 0 0.9rem;
}

.cc-weather-status-item {
    display: inline-flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.cc-weather-status-label {
    color: var(--cc-muted);
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.cc-status-badge {
    display: inline-flex;
    align-items: center;
    min-height: 1.85rem;
    padding: 0.35rem 0.7rem;
    border: 1px solid transparent;
    border-radius: 999px;
    font-size: 0.76rem;
    font-weight: 750;
    letter-spacing: 0.01em;
}

.cc-status-weather {
    border-color: #8DB7EA;
    background: var(--cc-blue);
    color: #FFFFFF;
}

.cc-status-weather-soft {
    border-color: #E8C66A;
    background: var(--cc-weather-soft);
    color: #7A5318;
}

.cc-weather-cards {
    display: grid;
    gap: var(--cc-card-gap);
    margin: 1.4rem 0 1.75rem;
}

.cc-weather-card {
    overflow: hidden;
    border: 1px solid var(--cc-border);
    border-left: 4px solid var(--cc-blue);
    border-radius: var(--cc-card-radius);
    background: var(--cc-surface);
    box-shadow: var(--cc-shadow);
}

.cc-weather-card-header {
    display: grid;
    grid-template-columns: auto minmax(0, 1fr);
    gap: 1rem;
    align-items: center;
    padding: 1rem 1.25rem;
    background: var(--cc-blue-soft);
}

.cc-weather-day {
    display: inline-flex;
    align-items: center;
    min-height: 2rem;
    padding: 0.35rem 0.65rem;
    border-radius: 999px;
    background: var(--cc-blue);
    color: #FFFFFF;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    white-space: nowrap;
}

.cc-weather-destination {
    min-width: 0;
}

.cc-weather-destination h3 {
    overflow: hidden;
    margin: 0 !important;
    color: var(--cc-navy) !important;
    font-size: 1.05rem !important;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.cc-weather-destination span {
    display: block;
    margin-top: 0.25rem;
    color: var(--cc-muted);
    font-size: 0.78rem;
}

.cc-weather-fields {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 0.75rem;
    padding: 1.05rem 1.25rem 1.15rem;
}

.cc-weather-field {
    display: flex;
    min-width: 0;
    flex-direction: column;
    gap: 0.35rem;
}

.cc-weather-field > span {
    color: var(--cc-muted);
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.cc-weather-field > strong {
    overflow: hidden;
    color: var(--cc-navy-soft);
    font-size: 0.92rem;
    line-height: 1.3;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.cc-weather-suitability {
    align-items: flex-start;
}

.cc-suitability-badge {
    display: inline-flex;
    align-items: center;
    min-height: 1.7rem;
    padding: 0.25rem 0.6rem;
    border: 1px solid transparent;
    border-radius: 999px;
    font-size: 0.76rem !important;
    font-weight: 800 !important;
    white-space: nowrap;
}

.cc-suitability-excellent {
    border-color: #B8E2C9;
    background: var(--cc-green-soft);
    color: #246B4A !important;
}

.cc-suitability-fair {
    border-color: #E8C66A;
    background: var(--cc-yellow-soft);
    color: #8A641D !important;
}

.cc-suitability-poor {
    border-color: #F0B49D;
    background: var(--cc-orange-soft);
    color: #A4472C !important;
}

.cc-suitability-neutral {
    border-color: var(--cc-border);
    background: var(--cc-information-soft);
    color: var(--cc-information) !important;
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
    padding: 1.35rem 1.4rem 1.25rem;
    border: 1px solid var(--cc-border);
    border-radius: var(--cc-card-radius);
    background:
        linear-gradient(
            145deg,
            #FFFFFF,
            #F0F8F6
        );
    box-shadow: var(--cc-shadow);
    transition: transform 160ms ease, box-shadow 160ms ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.cc-profile-stat::before {
    content: "";
    position: absolute;
    inset: 0 auto 0 0;
    width: 5px;
    background: var(--cc-teal);
}

.cc-profile-stat:nth-child(2)::before {
    background: var(--cc-green);
}

.cc-profile-stat:nth-child(3)::before {
    background: var(--cc-yellow);
}

.cc-profile-stat:hover {
    box-shadow: var(--cc-shadow-hover);
    transform: translateY(-2px);
}

.cc-profile-stat-label {
    color: var(--cc-muted) !important;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
}

.cc-profile-stat-value {
    position: relative;
    z-index: 1;
    margin-top: 0.8rem;
    color: var(--cc-ink) !important;
    font-size: clamp(1.8rem, 3vw, 2.25rem);
    font-weight: 800;
    letter-spacing: 0;
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
    margin: 1.4rem 0 1.75rem;
    padding: 0.35rem;
    border: 1px solid var(--cc-border);
    border-radius: var(--cc-card-radius);
    background: var(--cc-surface);
    box-shadow: var(--cc-shadow);
}

[data-testid="stDataFrame"] button {
    border: 1px solid transparent !important;
    border-radius: 0.6rem !important;
    color: var(--cc-muted) !important;
    background: transparent !important;
}

[data-testid="stDataFrame"] button:hover {
    border-color: var(--cc-border) !important;
    color: var(--cc-navy) !important;
    background: var(--cc-information-soft) !important;
}

[data-testid="stDataFrame"] [role="columnheader"] {
    min-height: 2.65rem;
    padding: 0.65rem 0.75rem !important;
    background: var(--cc-blue-soft) !important;
    color: var(--cc-navy) !important;
    font-size: 0.76rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.025em;
}

[data-testid="stDataFrame"] [role="columnheader"] {
    background: var(--cc-blue-soft) !important;
    color: var(--cc-navy) !important;
    font-weight: 800 !important;
}

[data-testid="stDataFrame"] [role="gridcell"] {
    min-height: 2.65rem;
    padding: 0.65rem 0.75rem !important;
    border-bottom: 1px solid #E6ECF3 !important;
    color: var(--cc-navy-soft) !important;
    font-size: 0.84rem !important;
}

[data-testid="stDataFrame"] [role="row"]:nth-child(even) [role="gridcell"] {
    background: #FAFCFE !important;
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

    .cc-recommendation-header {
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

    .cc-weather-card-header {
        align-items: flex-start;
        grid-template-columns: 1fr;
        gap: 0.65rem;
    }

    .cc-weather-fields {
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
    Weather Information • Smart ranking • Optimized routes
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
                route optimization, Weather Information, and budget-aware planning.
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
Trip Budget
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
Starting Location
</div>

<div class="cc-profile-detail-value">
{safe_starting_point}
</div>

</div>

</div>


<div class="cc-profile-detail">

<div class="cc-profile-detail-content">

<div class="cc-profile-detail-label">
Travel Style
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
Transport Preference
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