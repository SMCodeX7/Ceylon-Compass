import pandas as pd


DATA_PATH = "data/destinations.csv"

INTEREST_COLUMNS = [
    "beach",
    "wildlife",
    "hiking",
    "nature",
    "culture",
    "history",
    "adventure",
]


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    print("\nCEYLONCOMPASS DESTINATION DATASET ANALYSIS")
    print("=" * 55)

    # Dataset overview
    print("\n1. Dataset Shape")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    # Category distribution
    print("\n2. Category Distribution")
    print(df["category"].value_counts())

    # Province distribution
    print("\n3. Province Distribution")
    print(df["province"].value_counts())

    # Interest statistics
    print("\n4. Interest Feature Statistics")
    print(
        df[INTEREST_COLUMNS]
        .describe()
        .round(2)
        .T
    )

    # Average interest scores
    print("\n5. Average Interest Scores")
    print(
        df[INTEREST_COLUMNS]
        .mean()
        .sort_values(ascending=False)
        .round(2)
    )

    # Correlation between interests
    print("\n6. Interest Correlation Matrix")
    print(
        df[INTEREST_COLUMNS]
        .corr()
        .round(2)
    )

    # Highest scoring destinations by interest
    print("\n7. Top Destinations by Interest")

    for interest in INTEREST_COLUMNS:
        top = (
            df[["name", interest]]
            .sort_values(
                by=interest,
                ascending=False,
            )
            .head(5)
        )

        print(f"\n{interest.upper()}")
        print(top.to_string(index=False))

    # Cost information
    print("\n8. Cost Statistics")
    print(
        df["estimated_daily_cost_usd"]
        .describe()
        .round(2)
    )

    print("\n9. Cheapest Destinations")
    print(
        df[
            [
                "name",
                "estimated_daily_cost_usd",
            ]
        ]
        .sort_values(
            "estimated_daily_cost_usd"
        )
        .head(10)
        .to_string(index=False)
    )

    print("\n10. Dataset Ready for Recommendation Modelling")


if __name__ == "__main__":
    main()