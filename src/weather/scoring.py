from __future__ import annotations

import pandas as pd


WEATHER_CODE_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


CONDITION_SCORES = {
    0: 100.0,
    1: 98.0,
    2: 94.0,
    3: 88.0,
    45: 65.0,
    48: 60.0,
    51: 82.0,
    53: 72.0,
    55: 60.0,
    56: 45.0,
    57: 35.0,
    61: 78.0,
    63: 62.0,
    65: 42.0,
    66: 40.0,
    67: 30.0,
    71: 45.0,
    73: 35.0,
    75: 25.0,
    77: 30.0,
    80: 72.0,
    81: 55.0,
    82: 35.0,
    85: 30.0,
    86: 20.0,
    95: 30.0,
    96: 20.0,
    99: 10.0,
}


CONDITION_WEIGHT = 0.40
RAIN_PROBABILITY_WEIGHT = 0.30
PRECIPITATION_WEIGHT = 0.20
TEMPERATURE_WEIGHT = 0.10


def _normalize_weather_code(
    weather_code: int | float,
) -> int:
    """
    Validate and normalize a WMO weather code.
    """

    try:
        numeric_code = float(
            weather_code
        )
    except (
        TypeError,
        ValueError,
    ) as error:
        raise ValueError(
            "Weather code must be numeric."
        ) from error

    if not numeric_code.is_integer():
        raise ValueError(
            "Weather code must be an integer value."
        )

    return int(
        numeric_code
    )


def weather_code_description(
    weather_code: int | float,
) -> str:
    """
    Return a readable WMO weather description.
    """

    code = _normalize_weather_code(
        weather_code
    )

    return WEATHER_CODE_DESCRIPTIONS.get(
        code,
        "Unknown weather condition",
    )


def calculate_condition_score(
    weather_code: int | float,
) -> float:
    """
    Score the general WMO weather condition.

    Unknown weather codes receive a neutral score
    rather than causing the application to fail.
    """

    code = _normalize_weather_code(
        weather_code
    )

    return CONDITION_SCORES.get(
        code,
        50.0,
    )


def calculate_rain_probability_score(
    precipitation_probability: float,
) -> float:
    """
    Convert precipitation probability into a
    0-100 travel suitability score.
    """

    probability = float(
        precipitation_probability
    )

    if not 0 <= probability <= 100:
        raise ValueError(
            "Precipitation probability must be "
            "between 0 and 100."
        )

    return round(
        100.0 - probability,
        2,
    )


def calculate_precipitation_score(
    precipitation_mm: float,
) -> float:
    """
    Score forecast precipitation amount.

    Lower rainfall receives a higher travel
    suitability score.
    """

    precipitation = float(
        precipitation_mm
    )

    if precipitation < 0:
        raise ValueError(
            "Precipitation amount cannot be negative."
        )

    if precipitation == 0:
        return 100.0

    if precipitation <= 1:
        return 90.0

    if precipitation <= 5:
        return 70.0

    if precipitation <= 10:
        return 50.0

    if precipitation <= 20:
        return 30.0

    return 10.0


def calculate_temperature_score(
    maximum_temperature_c: float,
    minimum_temperature_c: float,
) -> float:
    """
    Calculate a simple travel-comfort temperature
    score using the day's average temperature.
    """

    maximum = float(
        maximum_temperature_c
    )

    minimum = float(
        minimum_temperature_c
    )

    if maximum < minimum:
        raise ValueError(
            "Maximum temperature cannot be lower "
            "than minimum temperature."
        )

    average_temperature = (
        maximum
        + minimum
    ) / 2.0

    if 20 <= average_temperature <= 28:
        return 100.0

    if (
        18 <= average_temperature < 20
        or 28 < average_temperature <= 30
    ):
        return 90.0

    if (
        15 <= average_temperature < 18
        or 30 < average_temperature <= 32
    ):
        return 75.0

    if (
        10 <= average_temperature < 15
        or 32 < average_temperature <= 35
    ):
        return 60.0

    return 40.0


def weather_suitability_label(
    weather_score: float,
) -> str:
    """
    Convert a numeric weather score into a
    traveller-friendly suitability label.
    """

    score = float(
        weather_score
    )

    if not 0 <= score <= 100:
        raise ValueError(
            "Weather score must be between 0 and 100."
        )

    if score >= 80:
        return "Excellent"

    if score >= 65:
        return "Good"

    if score >= 50:
        return "Fair"

    return "Poor"


def calculate_daily_weather_score(
    weather_row: pd.Series,
) -> dict:
    """
    Calculate component scores and the final
    weather suitability score for one forecast day.
    """

    required_fields = {
        "weather_code",
        "temperature_max_c",
        "temperature_min_c",
        "precipitation_probability_max",
        "precipitation_sum_mm",
    }

    missing_fields = (
        required_fields
        - set(weather_row.index)
    )

    if missing_fields:
        raise ValueError(
            "Weather row is missing scoring fields: "
            + ", ".join(
                sorted(missing_fields)
            )
        )

    condition_score = (
        calculate_condition_score(
            weather_row[
                "weather_code"
            ]
        )
    )

    rain_probability_score = (
        calculate_rain_probability_score(
            weather_row[
                "precipitation_probability_max"
            ]
        )
    )

    precipitation_score = (
        calculate_precipitation_score(
            weather_row[
                "precipitation_sum_mm"
            ]
        )
    )

    temperature_score = (
        calculate_temperature_score(
            weather_row[
                "temperature_max_c"
            ],
            weather_row[
                "temperature_min_c"
            ],
        )
    )

    final_score = (
        condition_score
        * CONDITION_WEIGHT
        + rain_probability_score
        * RAIN_PROBABILITY_WEIGHT
        + precipitation_score
        * PRECIPITATION_WEIGHT
        + temperature_score
        * TEMPERATURE_WEIGHT
    )

    final_score = round(
        final_score,
        2,
    )

    return {
        "weather_description": (
            weather_code_description(
                weather_row[
                    "weather_code"
                ]
            )
        ),
        "condition_score": (
            condition_score
        ),
        "rain_probability_score": (
            rain_probability_score
        ),
        "precipitation_score": (
            precipitation_score
        ),
        "temperature_score": (
            temperature_score
        ),
        "weather_score": (
            final_score
        ),
        "weather_suitability": (
            weather_suitability_label(
                final_score
            )
        ),
    }


def score_weather_forecast(
    forecast: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add weather suitability scores to every
    forecast day.
    """

    required_columns = {
        "date",
        "weather_code",
        "temperature_max_c",
        "temperature_min_c",
        "precipitation_probability_max",
        "precipitation_sum_mm",
    }

    missing_columns = (
        required_columns
        - set(forecast.columns)
    )

    if missing_columns:
        raise ValueError(
            "Weather forecast is missing scoring columns: "
            + ", ".join(
                sorted(missing_columns)
            )
        )

    scored = forecast.copy()

    if scored.empty:
        return scored

    score_records = []

    for _, row in scored.iterrows():
        score_records.append(
            calculate_daily_weather_score(
                row
            )
        )

    scores_df = pd.DataFrame(
        score_records
    )

    for column in scores_df.columns:
        scored[column] = (
            scores_df[column].values
        )

    return scored


def weather_forecast_summary(
    scored_forecast: pd.DataFrame,
) -> dict:
    """
    Summarize weather suitability across a
    multi-day forecast.
    """

    required_columns = {
        "date",
        "weather_score",
        "weather_description",
        "weather_suitability",
    }

    missing_columns = (
        required_columns
        - set(scored_forecast.columns)
    )

    if missing_columns:
        raise ValueError(
            "Scored forecast is missing summary columns: "
            + ", ".join(
                sorted(missing_columns)
            )
        )

    if scored_forecast.empty:
        raise ValueError(
            "Cannot summarize an empty weather forecast."
        )

    best_index = (
        scored_forecast[
            "weather_score"
        ].idxmax()
    )

    worst_index = (
        scored_forecast[
            "weather_score"
        ].idxmin()
    )

    best_day = (
        scored_forecast.loc[
            best_index
        ]
    )

    worst_day = (
        scored_forecast.loc[
            worst_index
        ]
    )

    return {
        "average_weather_score": round(
            float(
                scored_forecast[
                    "weather_score"
                ].mean()
            ),
            2,
        ),
        "best_date": (
            best_day["date"]
        ),
        "best_day_score": float(
            best_day[
                "weather_score"
            ]
        ),
        "best_day_condition": (
            best_day[
                "weather_description"
            ]
        ),
        "worst_date": (
            worst_day["date"]
        ),
        "worst_day_score": float(
            worst_day[
                "weather_score"
            ]
        ),
        "worst_day_condition": (
            worst_day[
                "weather_description"
            ]
        ),
    }