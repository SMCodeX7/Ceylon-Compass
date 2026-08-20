from __future__ import annotations

import json

from src.evaluation.reporting import (
    generate_evaluation_artifacts,
)
from src.evaluation.runner import (
    run_evaluation,
    summarize_by_segment,
    summarize_evaluation,
)


def main() -> None:
    """
    Run the complete reproducible CeylonCompass
    quantitative evaluation.
    """

    print(
        "=" * 72
    )

    print(
        "CEYLONCOMPASS QUANTITATIVE EVALUATION"
    )

    print(
        "=" * 72
    )

    print(
        "\nRunning fixed evaluation scenarios..."
    )

    results = (
        run_evaluation()
    )

    overall_summary = (
        summarize_evaluation(
            results
        )
    )

    segment_summary = (
        summarize_by_segment(
            results
        )
    )

    artifact_paths = (
        generate_evaluation_artifacts(
            results=results,
            overall_summary=(
                overall_summary
            ),
            segment_summary=(
                segment_summary
            ),
        )
    )

    print(
        "\nOVERALL EVALUATION SUMMARY"
    )

    print(
        "-" * 72
    )

    print(
        json.dumps(
            overall_summary,
            indent=2,
        )
    )

    print(
        "\nSEGMENT SUMMARY"
    )

    print(
        "-" * 72
    )

    print(
        segment_summary.to_string(
            index=False
        )
    )

    print(
        "\nGENERATED ARTIFACTS"
    )

    print(
        "-" * 72
    )

    for name, path in (
        artifact_paths.items()
    ):
        print(
            f"{name}: {path}"
        )

    print(
        "\nImportant:"
    )

    print(
        "- Preference similarity is not "
        "human-labelled recommendation accuracy."
    )

    print(
        "- Weather in this evaluation is "
        "deterministic synthetic weather."
    )

    print(
        "- Route distances are Haversine proxies, "
        "not road-driving distances."
    )

    print(
        "\nEvaluation complete."
    )


if __name__ == "__main__":
    main()