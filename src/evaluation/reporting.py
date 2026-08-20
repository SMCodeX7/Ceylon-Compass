from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go


DEFAULT_OUTPUT_ROOT = Path(
    "evaluation"
)


def build_evaluation_report(
    overall_summary: dict,
    segment_summary: pd.DataFrame,
) -> str:
    """
    Build a Markdown report from measured evaluation
    outputs.

    The generated report distinguishes internal
    system-quality indicators from external
    ground-truth accuracy.
    """

    if not overall_summary:
        raise ValueError(
            "Overall evaluation summary cannot be empty."
        )

    if segment_summary.empty:
        raise ValueError(
            "Segment summary cannot be empty."
        )

    required_summary_fields = {
        "scenario_count",
        "mean_preference_score",
        "mean_final_score",
        "mean_category_diversity_pct",
        "budget_compliance_rate_pct",
        "duration_compliance_rate_pct",
        "mean_scheduled_coverage_pct",
        "mean_weather_coverage_pct",
        "mean_weather_score",
        "route_validity_rate_pct",
        "mean_route_distance_saving_pct",
        "optimized_not_worse_rate_pct",
    }

    missing_fields = (
        required_summary_fields
        - set(
            overall_summary
        )
    )

    if missing_fields:
        raise ValueError(
            "Overall summary is missing fields: "
            + ", ".join(
                sorted(
                    missing_fields
                )
            )
        )

    lines = [
        "# CeylonCompass Quantitative Evaluation",
        "",
        "## Evaluation Scope",
        "",
        (
            f"The evaluation contains "
            f"**{overall_summary['scenario_count']} "
            f"fixed traveller scenarios** covering "
            f"different interests, budgets, trip lengths, "
            f"starting locations, crowd preferences, "
            f"travel styles and transport modes."
        ),
        "",
        (
            "Weather conditions in this benchmark are "
            "**deterministic synthetic forecasts**. "
            "They are used to evaluate the behaviour of "
            "the weather-aware planning pipeline "
            "reproducibly. They do not evaluate "
            "Open-Meteo forecast accuracy."
        ),
        "",
        (
            "Preference score is an internal cosine-"
            "similarity indicator derived from the "
            "curated destination feature vectors. "
            "It must not be interpreted as human-labelled "
            "recommendation accuracy."
        ),
        "",
        "## Overall Results",
        "",
        "| Metric | Result |",
        "| --- | ---: |",
        (
            "| Mean preference similarity | "
            f"{overall_summary['mean_preference_score']:.2f}% |"
        ),
        (
            "| Mean final recommendation score | "
            f"{overall_summary['mean_final_score']:.2f}% |"
        ),
        (
            "| Mean category diversity | "
            f"{overall_summary['mean_category_diversity_pct']:.2f}% |"
        ),
        (
            "| Budget compliance rate | "
            f"{overall_summary['budget_compliance_rate_pct']:.2f}% |"
        ),
        (
            "| Duration compliance rate | "
            f"{overall_summary['duration_compliance_rate_pct']:.2f}% |"
        ),
        (
            "| Mean scheduled-destination coverage | "
            f"{overall_summary['mean_scheduled_coverage_pct']:.2f}% |"
        ),
        (
            "| Controlled-weather coverage | "
            f"{overall_summary['mean_weather_coverage_pct']:.2f}% |"
        ),
        (
            "| Mean controlled-weather score | "
            f"{overall_summary['mean_weather_score']:.2f}% |"
        ),
        (
            "| Route structural validity rate | "
            f"{overall_summary['route_validity_rate_pct']:.2f}% |"
        ),
        (
            "| Mean OR-Tools distance saving vs "
            "nearest-neighbour | "
            f"{overall_summary['mean_route_distance_saving_pct']:.2f}% |"
        ),
        (
            "| OR-Tools not-worse-than-baseline rate | "
            f"{overall_summary['optimized_not_worse_rate_pct']:.2f}% |"
        ),
        "",
        "## Segment Results",
        "",
    ]

    segment_columns = [
        "segment",
        "scenario_count",
        "mean_preference_score",
        "mean_final_score",
        "budget_compliance_rate_pct",
        "scheduled_coverage_pct",
        "category_diversity_pct",
        "route_distance_saving_pct",
    ]

    available_segment_columns = [
        column
        for column in segment_columns
        if column in segment_summary.columns
    ]

    report_segment_summary = (
        segment_summary[
            available_segment_columns
        ].copy()
    )

    lines.append(
        report_segment_summary.to_markdown(
            index=False
        )
    )

    lines.extend(
        [
            "",
            "## Interpretation Rules",
            "",
            (
                "- **Preference similarity** measures "
                "alignment between a traveller interest "
                "vector and curated destination feature "
                "vectors."
            ),
            (
                "- **Final recommendation score** is the "
                "weighted CeylonCompass ranking score, "
                "not a probability."
            ),
            (
                "- **Budget compliance** is based on the "
                "current V1 cost model and its explicit "
                "cost assumptions."
            ),
            (
                "- **Duration compliance** checks the "
                "current 8-hour daily activity limit. "
                "Travel time is not included in that "
                "daily limit."
            ),
            (
                "- **Route distance** uses Haversine "
                "great-circle distance. It is not actual "
                "road-driving distance."
            ),
            (
                "- **Route saving** compares the OR-Tools "
                "result against the project's "
                "nearest-neighbour baseline using the "
                "same selected destinations."
            ),
            (
                "- **Controlled-weather score** measures "
                "planner behaviour under deterministic "
                "weather inputs rather than real forecast "
                "accuracy."
            ),
            "",
            "## Current Evaluation Limitations",
            "",
            (
                "1. The project does not yet contain "
                "human relevance labels, so metrics such "
                "as Precision@K, Recall@K or NDCG against "
                "human ground truth cannot be claimed."
            ),
            (
                "2. Destination interest features are "
                "curated modelling inputs and should not "
                "be treated as objective labels."
            ),
            (
                "3. The budget model contains transparent "
                "V1 assumptions rather than guaranteed "
                "current Sri Lankan market prices."
            ),
            (
                "4. Haversine distances can underestimate "
                "actual road travel."
            ),
            (
                "5. The itinerary activity-hour constraint "
                "does not yet include travel time."
            ),
            (
                "6. Controlled synthetic weather is used "
                "for reproducibility in this benchmark."
            ),
            "",
        ]
    )

    return "\n".join(
        lines
    )


def _write_score_chart(
    segment_summary: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    Create an interactive segment-level score chart.
    """

    figure = go.Figure()

    figure.add_trace(
        go.Bar(
            name="Preference Similarity",
            x=segment_summary[
                "segment"
            ],
            y=segment_summary[
                "mean_preference_score"
            ],
        )
    )

    figure.add_trace(
        go.Bar(
            name="Final Score",
            x=segment_summary[
                "segment"
            ],
            y=segment_summary[
                "mean_final_score"
            ],
        )
    )

    figure.update_layout(
        title=(
            "Mean Recommendation Scores "
            "by Evaluation Segment"
        ),
        xaxis_title="Traveller Segment",
        yaxis_title="Score (%)",
        barmode="group",
        yaxis_range=[
            0,
            100,
        ],
    )

    figure.write_html(
        output_path,
        include_plotlyjs="cdn",
    )


def _write_route_chart(
    results: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    Create an interactive scenario-level route saving
    chart.
    """

    figure = go.Figure(
        data=[
            go.Bar(
                x=results[
                    "scenario_id"
                ],
                y=results[
                    "route_distance_saving_pct"
                ],
                name="Route Distance Saving",
            )
        ]
    )

    figure.update_layout(
        title=(
            "OR-Tools Route Distance Saving "
            "vs Nearest-Neighbour Baseline"
        ),
        xaxis_title="Evaluation Scenario",
        yaxis_title="Distance Saving (%)",
    )

    figure.add_hline(
        y=0,
    )

    figure.write_html(
        output_path,
        include_plotlyjs="cdn",
    )


def _write_compliance_chart(
    overall_summary: dict,
    output_path: Path,
) -> None:
    """
    Create an interactive chart for system compliance
    and route-validity rates.
    """

    labels = [
        "Budget",
        "Duration",
        "Route Validity",
        "Optimizer Not Worse",
        "Weather Coverage",
    ]

    values = [
        overall_summary[
            "budget_compliance_rate_pct"
        ],
        overall_summary[
            "duration_compliance_rate_pct"
        ],
        overall_summary[
            "route_validity_rate_pct"
        ],
        overall_summary[
            "optimized_not_worse_rate_pct"
        ],
        overall_summary[
            "mean_weather_coverage_pct"
        ],
    ]

    figure = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=values,
                name="Rate",
            )
        ]
    )

    figure.update_layout(
        title=(
            "CeylonCompass Evaluation "
            "Compliance Rates"
        ),
        xaxis_title="Metric",
        yaxis_title="Rate (%)",
        yaxis_range=[
            0,
            100,
        ],
    )

    figure.write_html(
        output_path,
        include_plotlyjs="cdn",
    )


def generate_evaluation_artifacts(
    results: pd.DataFrame,
    overall_summary: dict,
    segment_summary: pd.DataFrame,
    output_root: Path = DEFAULT_OUTPUT_ROOT,
) -> dict[str, Path]:
    """
    Save reproducible evaluation results, summaries,
    report and interactive charts.
    """

    if results.empty:
        raise ValueError(
            "Evaluation results cannot be empty."
        )

    if segment_summary.empty:
        raise ValueError(
            "Segment summary cannot be empty."
        )

    output_root = Path(
        output_root
    )

    results_directory = (
        output_root
        / "results"
    )

    charts_directory = (
        output_root
        / "charts"
    )

    results_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    charts_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    scenario_results_path = (
        results_directory
        / "scenario_results.csv"
    )

    segment_summary_path = (
        results_directory
        / "segment_summary.csv"
    )

    overall_summary_path = (
        results_directory
        / "overall_summary.json"
    )

    report_path = (
        results_directory
        / "evaluation_report.md"
    )

    score_chart_path = (
        charts_directory
        / "segment_scores.html"
    )

    route_chart_path = (
        charts_directory
        / "route_savings.html"
    )

    compliance_chart_path = (
        charts_directory
        / "compliance_rates.html"
    )

    results.to_csv(
        scenario_results_path,
        index=False,
    )

    segment_summary.to_csv(
        segment_summary_path,
        index=False,
    )

    with overall_summary_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            overall_summary,
            file,
            indent=2,
        )

    report_text = (
        build_evaluation_report(
            overall_summary,
            segment_summary,
        )
    )

    report_path.write_text(
        report_text,
        encoding="utf-8",
    )

    _write_score_chart(
        segment_summary,
        score_chart_path,
    )

    _write_route_chart(
        results,
        route_chart_path,
    )

    _write_compliance_chart(
        overall_summary,
        compliance_chart_path,
    )

    return {
        "scenario_results": (
            scenario_results_path
        ),
        "segment_summary": (
            segment_summary_path
        ),
        "overall_summary": (
            overall_summary_path
        ),
        "evaluation_report": (
            report_path
        ),
        "segment_scores_chart": (
            score_chart_path
        ),
        "route_savings_chart": (
            route_chart_path
        ),
        "compliance_rates_chart": (
            compliance_chart_path
        ),
    }