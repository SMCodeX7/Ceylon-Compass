from pathlib import Path

import pandas as pd


DATA_PATH = Path("data/destinations.csv")

REQUIRED_COLUMNS = [
    "destination_id",
    "name",
    "district",
    "province",
    "latitude",
    "longitude",
    "category",
    "estimated_daily_cost_usd",
    "recommended_duration_hours",
    "crowd_level",
    "beach",
    "wildlife",
    "hiking",
    "nature",
    "culture",
    "history",
    "adventure",
    "fitness_requirement",
    "family_suitability",
    "best_months",
]

INTEREST_COLUMNS = [
    "beach",
    "wildlife",
    "hiking",
    "nature",
    "culture",
    "history",
    "adventure",
]


def validate_dataset(path: Path = DATA_PATH) -> pd.DataFrame:
    """Validate the CeylonCompass destination dataset."""

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path)

    errors: list[str] = []

    # 1. Validate schema
    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in df.columns
    ]

    if missing_columns:
        errors.append(
            f"Missing required columns: {', '.join(missing_columns)}"
        )

    if len(df.columns) != len(REQUIRED_COLUMNS):
        errors.append(
            f"Expected {len(REQUIRED_COLUMNS)} columns, "
            f"found {len(df.columns)}."
        )

    # Stop deeper validation if schema is incomplete
    if missing_columns:
        raise ValueError("\n".join(errors))

    # 2. Missing values
    missing_values = int(df.isnull().sum().sum())

    if missing_values > 0:
        errors.append(
            f"Dataset contains {missing_values} missing value(s)."
        )

    # 3. Unique IDs
    duplicated_ids = df[
        df["destination_id"].duplicated(keep=False)
    ]["destination_id"].tolist()

    if duplicated_ids:
        errors.append(
            f"Duplicate destination IDs: {duplicated_ids}"
        )

    # 4. Unique destination names
    duplicated_names = df[
        df["name"].duplicated(keep=False)
    ]["name"].tolist()

    if duplicated_names:
        errors.append(
            f"Duplicate destination names: {duplicated_names}"
        )

    # 5. Latitude / longitude validation
    invalid_latitudes = df[
        ~df["latitude"].between(-90, 90)
    ]

    if not invalid_latitudes.empty:
        errors.append(
            "One or more latitude values are outside -90 to 90."
        )

    invalid_longitudes = df[
        ~df["longitude"].between(-180, 180)
    ]

    if not invalid_longitudes.empty:
        errors.append(
            "One or more longitude values are outside -180 to 180."
        )

    # Sri Lanka-specific geographic sanity check
    sri_lanka_bounds = df[
        ~(
            df["latitude"].between(5.5, 10.0)
            & df["longitude"].between(79.0, 82.5)
        )
    ]

    if not sri_lanka_bounds.empty:
        errors.append(
            "One or more destinations appear outside "
            "the expected Sri Lankan geographic bounds."
        )

    # 6. Interest features must be between 0 and 5
    for column in INTEREST_COLUMNS:
        invalid_scores = df[~df[column].between(0, 5)]

        if not invalid_scores.empty:
            errors.append(
                f"Column '{column}' contains values outside 0-5."
            )

    # 7. Other scored features
    for column in [
        "crowd_level",
        "fitness_requirement",
        "family_suitability",
    ]:
        invalid_scores = df[~df[column].between(1, 5)]

        if not invalid_scores.empty:
            errors.append(
                f"Column '{column}' contains values outside 1-5."
            )

    # 8. Positive cost and duration
    if (df["estimated_daily_cost_usd"] <= 0).any():
        errors.append(
            "Estimated daily cost must be greater than 0."
        )

    if (df["recommended_duration_hours"] <= 0).any():
        errors.append(
            "Recommended duration must be greater than 0."
        )

    if errors:
        error_message = "\n".join(
            f"- {error}" for error in errors
        )

        raise ValueError(
            f"CeylonCompass dataset validation failed:\n"
            f"{error_message}"
        )

    return df


def print_dataset_summary(df: pd.DataFrame) -> None:
    """Print a concise dataset quality summary."""

    print("CeylonCompass Destination Dataset")
    print("-" * 40)
    print(f"Destinations : {len(df)}")
    print(f"Features     : {len(df.columns)}")
    print(f"Missing      : {df.isnull().sum().sum()}")
    print(
        f"Duplicate IDs: "
        f"{df['destination_id'].duplicated().sum()}"
    )

    print("\nCategory Distribution")
    print(df["category"].value_counts().to_string())

    print("\nProvince Distribution")
    print(df["province"].value_counts().to_string())

    print("\nInterest Feature Averages")
    print(
        df[INTEREST_COLUMNS]
        .mean()
        .round(2)
        .to_string()
    )


if __name__ == "__main__":
    dataset = validate_dataset()
    print_dataset_summary(dataset)

    print("\nDataset validation passed.")