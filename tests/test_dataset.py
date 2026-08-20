from pathlib import Path

import pandas as pd

from src.utils.data_validation import (
    INTEREST_COLUMNS,
    REQUIRED_COLUMNS,
    validate_dataset,
)


DATA_PATH = Path("data/destinations.csv")


def test_dataset_exists() -> None:
    assert DATA_PATH.exists()


def test_dataset_has_expected_shape() -> None:
    df = pd.read_csv(DATA_PATH)

    assert len(df) == 48
    assert len(df.columns) == 20


def test_dataset_has_required_columns() -> None:
    df = pd.read_csv(DATA_PATH)

    assert list(df.columns) == REQUIRED_COLUMNS


def test_dataset_has_no_missing_values() -> None:
    df = pd.read_csv(DATA_PATH)

    assert df.isnull().sum().sum() == 0


def test_destination_ids_are_unique() -> None:
    df = pd.read_csv(DATA_PATH)

    assert df["destination_id"].is_unique


def test_destination_names_are_unique() -> None:
    df = pd.read_csv(DATA_PATH)

    assert df["name"].is_unique


def test_interest_scores_are_valid() -> None:
    df = pd.read_csv(DATA_PATH)

    for column in INTEREST_COLUMNS:
        assert df[column].between(0, 5).all()


def test_suitability_scores_are_valid() -> None:
    df = pd.read_csv(DATA_PATH)

    scored_columns = [
        "crowd_level",
        "fitness_requirement",
        "family_suitability",
    ]

    for column in scored_columns:
        assert df[column].between(1, 5).all()


def test_coordinates_are_within_sri_lanka() -> None:
    df = pd.read_csv(DATA_PATH)

    assert df["latitude"].between(5.5, 10.0).all()
    assert df["longitude"].between(79.0, 82.5).all()


def test_costs_are_positive() -> None:
    df = pd.read_csv(DATA_PATH)

    assert (df["estimated_daily_cost_usd"] > 0).all()


def test_visit_durations_are_positive() -> None:
    df = pd.read_csv(DATA_PATH)

    assert (df["recommended_duration_hours"] > 0).all()


def test_full_dataset_validator() -> None:
    df = validate_dataset(DATA_PATH)

    assert len(df) == 48