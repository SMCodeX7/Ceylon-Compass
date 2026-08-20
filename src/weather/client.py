from __future__ import annotations

import pandas as pd
import requests


OPEN_METEO_FORECAST_URL = (
    "https://api.open-meteo.com/v1/forecast"
)

DEFAULT_FORECAST_DAYS = 7
MAX_FORECAST_DAYS = 16
REQUEST_TIMEOUT_SECONDS = 10

DAILY_WEATHER_VARIABLES = (
    "weather_code",
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_probability_max",
    "precipitation_sum",
)


def _validate_coordinates(
    latitude: float,
    longitude: float,
) -> None:
    """
    Validate geographical coordinates.
    """

    if not -90 <= latitude <= 90:
        raise ValueError(
            "Latitude must be between -90 and 90."
        )

    if not -180 <= longitude <= 180:
        raise ValueError(
            "Longitude must be between -180 and 180."
        )


def _validate_forecast_days(
    forecast_days: int,
) -> None:
    """
    Validate the Open-Meteo forecast horizon.
    """

    if not isinstance(
        forecast_days,
        int,
    ):
        raise ValueError(
            "Forecast days must be an integer."
        )

    if not 1 <= forecast_days <= MAX_FORECAST_DAYS:
        raise ValueError(
            "Forecast days must be between 1 and 16."
        )


def _validate_daily_response(
    daily: dict,
) -> None:
    """
    Validate the required daily forecast arrays.
    """

    required_fields = {
        "time",
        *DAILY_WEATHER_VARIABLES,
    }

    missing_fields = (
        required_fields
        - set(daily.keys())
    )

    if missing_fields:
        raise RuntimeError(
            "Weather API response is missing fields: "
            + ", ".join(
                sorted(missing_fields)
            )
        )

    lengths = {
        len(daily[field])
        for field in required_fields
    }

    if len(lengths) != 1:
        raise RuntimeError(
            "Weather API returned inconsistent "
            "daily forecast lengths."
        )


def fetch_weather_forecast(
    latitude: float,
    longitude: float,
    forecast_days: int = DEFAULT_FORECAST_DAYS,
) -> pd.DataFrame:
    """
    Fetch daily weather forecast data from Open-Meteo.

    Returns one row per forecast day.

    Open-Meteo's free forecast endpoint does not
    require an API key for non-commercial use.
    """

    latitude = float(latitude)
    longitude = float(longitude)

    _validate_coordinates(
        latitude,
        longitude,
    )

    _validate_forecast_days(
        forecast_days,
    )

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ",".join(
            DAILY_WEATHER_VARIABLES
        ),
        "timezone": "auto",
        "forecast_days": forecast_days,
    }

    try:
        response = requests.get(
            OPEN_METEO_FORECAST_URL,
            params=params,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )

        response.raise_for_status()

    except requests.RequestException as error:
        raise RuntimeError(
            "Unable to retrieve weather forecast "
            "from Open-Meteo."
        ) from error

    try:
        payload = response.json()

    except ValueError as error:
        raise RuntimeError(
            "Weather API returned invalid JSON."
        ) from error

    if payload.get("error"):
        reason = payload.get(
            "reason",
            "Unknown weather API error.",
        )

        raise RuntimeError(
            f"Open-Meteo error: {reason}"
        )

    daily = payload.get(
        "daily"
    )

    if not isinstance(
        daily,
        dict,
    ):
        raise RuntimeError(
            "Weather API response does not contain "
            "daily forecast data."
        )

    _validate_daily_response(
        daily
    )

    forecast = pd.DataFrame(
        {
            "date": pd.to_datetime(
                daily["time"]
            ),
            "weather_code": pd.to_numeric(
                daily["weather_code"],
                errors="coerce",
            ),
            "temperature_max_c": pd.to_numeric(
                daily["temperature_2m_max"],
                errors="coerce",
            ),
            "temperature_min_c": pd.to_numeric(
                daily["temperature_2m_min"],
                errors="coerce",
            ),
            "precipitation_probability_max": (
                pd.to_numeric(
                    daily[
                        "precipitation_probability_max"
                    ],
                    errors="coerce",
                )
            ),
            "precipitation_sum_mm": pd.to_numeric(
                daily["precipitation_sum"],
                errors="coerce",
            ),
        }
    )

    if forecast.empty:
        raise RuntimeError(
            "Weather API returned an empty forecast."
        )

    required_numeric_columns = [
        "weather_code",
        "temperature_max_c",
        "temperature_min_c",
        "precipitation_probability_max",
        "precipitation_sum_mm",
    ]

    if forecast[
        required_numeric_columns
    ].isna().any().any():
        raise RuntimeError(
            "Weather API returned incomplete "
            "forecast values."
        )

    return forecast