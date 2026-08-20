import json

import pandas as pd
import pytest

from src.evaluation.reporting import (
    build_evaluation_report,
    generate_evaluation_artifacts,
)


def make_results() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "scenario_id": [
                "E001",
                "E002",
            ],
            "segment": [
                "Beach",
                "Nature",
            ],
            "mean_preference_score": [
                80.0,
                85.0,
            ],
            "mean_final_score": [
                78.0,
                82.0,
            ],
            "route_distance_saving_pct": [
                5.0,
                12.0,
            ],
        }
    )


def make_segment_summary() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "segment": [
                "Beach",
                "Nature",
            ],
            "scenario_count": [
                1,
                1,
            ],
            "mean_preference_score": [
                80.0,
                85.0,
            ],
            "mean_final_score": [
                78.0,
                82.0,
            ],
            "scheduled_coverage_pct": [
                100.0,
                90.0,
            ],
            "category_diversity_pct": [
                60.0,
                80.0,
            ],
            "route_distance_saving_pct": [
                5.0,
                12.0,
            ],
            "budget_compliance_rate_pct": [
                100.0,
                100.0,
            ],
        }
    )


def make_overall_summary() -> dict:
    return {
        "scenario_count": 2,
        "mean_preference_score": 82.5,
        "mean_final_score": 80.0,
        "mean_category_diversity_pct": 70.0,
        "budget_compliance_rate_pct": 100.0,
        "duration_compliance_rate_pct": 100.0,
        "mean_scheduled_coverage_pct": 95.0,
        "mean_weather_coverage_pct": 100.0,
        "mean_weather_score": 76.0,
        "route_validity_rate_pct": 100.0,
        "mean_route_distance_saving_pct": 8.5,
        "optimized_not_worse_rate_pct": 100.0,
    }


def test_report_contains_measured_metrics() -> None:
    report = (
        build_evaluation_report(
            make_overall_summary(),
            make_segment_summary(),
        )
    )

    assert (
        "82.50%"
        in report
    )

    assert (
        "100.00%"
        in report
    )


def test_report_contains_methodology_limitations() -> None:
    report = (
        build_evaluation_report(
            make_overall_summary(),
            make_segment_summary(),
        )
    )

    assert (
        "human relevance labels"
        in report
    )

    assert (
        "synthetic weather"
        in report
    )

    assert (
        "Haversine"
        in report
    )


def test_generate_artifacts_creates_result_files(
    tmp_path,
) -> None:
    paths = (
        generate_evaluation_artifacts(
            results=make_results(),
            overall_summary=(
                make_overall_summary()
            ),
            segment_summary=(
                make_segment_summary()
            ),
            output_root=tmp_path,
        )
    )

    assert paths[
        "scenario_results"
    ].exists()

    assert paths[
        "segment_summary"
    ].exists()

    assert paths[
        "overall_summary"
    ].exists()

    assert paths[
        "evaluation_report"
    ].exists()


def test_saved_summary_contains_expected_values(
    tmp_path,
) -> None:
    paths = (
        generate_evaluation_artifacts(
            results=make_results(),
            overall_summary=(
                make_overall_summary()
            ),
            segment_summary=(
                make_segment_summary()
            ),
            output_root=tmp_path,
        )
    )

    with paths[
        "overall_summary"
    ].open(
        "r",
        encoding="utf-8",
    ) as file:
        summary = json.load(
            file
        )

    assert (
        summary[
            "scenario_count"
        ]
        == 2
    )

    assert (
        summary[
            "mean_final_score"
        ]
        == 80.0
    )


def test_generate_artifacts_creates_charts(
    tmp_path,
) -> None:
    paths = (
        generate_evaluation_artifacts(
            results=make_results(),
            overall_summary=(
                make_overall_summary()
            ),
            segment_summary=(
                make_segment_summary()
            ),
            output_root=tmp_path,
        )
    )

    assert paths[
        "segment_scores_chart"
    ].exists()

    assert paths[
        "route_savings_chart"
    ].exists()

    assert paths[
        "compliance_rates_chart"
    ].exists()


def test_empty_results_are_rejected(
    tmp_path,
) -> None:
    with pytest.raises(
        ValueError,
        match="cannot be empty",
    ):
        generate_evaluation_artifacts(
            results=pd.DataFrame(),
            overall_summary=(
                make_overall_summary()
            ),
            segment_summary=(
                make_segment_summary()
            ),
            output_root=tmp_path,
        )