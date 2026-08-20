import pandas as pd
import pytest
import requests

from src.weather.client import (
    fetch_weather_forecast,
)
from src.weather.scoring import (
    calculate_condition_score,
    calculate_daily_weather_score,
    calculate_precipitation_score,
    calculate_rain_probability_score,
    calculate_temperature_score,
    score_weather_forecast,
    weather_code_description,
    weather_forecast_summary,
    weather_suitability_label,
)


def make_forecast() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.to_datetime(
                [
                    "2026-08-20",
                    "2026-08-21",
                ]
            ),
            "weather_code": [
                0,
                95,
            ],
            "temperature_max_c": [
                29.0,
                34.0,
            ],
            "temperature_min_c": [
                23.0,
                25.0,
            ],
            "precipitation_probability_max": [
                10.0,
                90.0,
            ],
            "precipitation_sum_mm": [
                0.0,
                12.0,
            ],
        }
    )


def test_clear_weather_description() -> None:
    assert (
        weather_code_description(
            0
        )
        == "Clear sky"
    )


def test_cloudy_weather_description() -> None:
    assert (
        weather_code_description(
            3
        )
        == "Overcast"
    )


def test_thunderstorm_weather_description() -> None:
    assert (
        weather_code_description(
            95
        )
        == "Thunderstorm"
    )


def test_unknown_weather_code_description() -> None:
    assert (
        weather_code_description(
            999
        )
        == "Unknown weather condition"
    )


def test_clear_condition_scores_high() -> None:
    assert (
        calculate_condition_score(
            0
        )
        == 100.0
    )


def test_thunderstorm_scores_lower_than_clear() -> None:
    assert (
        calculate_condition_score(
            95
        )
        < calculate_condition_score(
            0
        )
    )


def test_rain_probability_score() -> None:
    assert (
        calculate_rain_probability_score(
            20
        )
        == 80.0
    )


def test_negative_rain_probability_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="between 0 and 100",
    ):
        calculate_rain_probability_score(
            -1
        )


def test_rain_probability_above_100_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="between 0 and 100",
    ):
        calculate_rain_probability_score(
            101
        )


def test_zero_precipitation_scores_highest() -> None:
    assert (
        calculate_precipitation_score(
            0
        )
        == 100.0
    )


def test_moderate_precipitation_score() -> None:
    assert (
        calculate_precipitation_score(
            4
        )
        == 70.0
    )


def test_heavy_precipitation_scores_lower() -> None:
    assert (
        calculate_precipitation_score(
            25
        )
        == 10.0
    )


def test_negative_precipitation_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="cannot be negative",
    ):
        calculate_precipitation_score(
            -1
        )


def test_comfortable_temperature_scores_high() -> None:
    assert (
        calculate_temperature_score(
            30,
            24,
        )
        == 100.0
    )


def test_very_hot_temperature_scores_lower() -> None:
    assert (
        calculate_temperature_score(
            43,
            31,
        )
        == 40.0
    )


def test_invalid_temperature_range_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="cannot be lower",
    ):
        calculate_temperature_score(
            20,
            25,
        )


def test_suitability_labels() -> None:
    assert (
        weather_suitability_label(
            90
        )
        == "Excellent"
    )

    assert (
        weather_suitability_label(
            70
        )
        == "Good"
    )

    assert (
        weather_suitability_label(
            55
        )
        == "Fair"
    )

    assert (
        weather_suitability_label(
            40
        )
        == "Poor"
    )


def test_clear_dry_weather_scores_better_than_storm() -> None:
    forecast = make_forecast()

    good = (
        calculate_daily_weather_score(
            forecast.iloc[0]
        )
    )

    bad = (
        calculate_daily_weather_score(
            forecast.iloc[1]
        )
    )

    assert (
        good["weather_score"]
        > bad["weather_score"]
    )


def test_score_forecast_adds_weather_columns() -> None:
    scored = score_weather_forecast(
        make_forecast()
    )

    expected_columns = {
        "weather_description",
        "condition_score",
        "rain_probability_score",
        "precipitation_score",
        "temperature_score",
        "weather_score",
        "weather_suitability",
    }

    assert expected_columns.issubset(
        scored.columns
    )


def test_score_forecast_preserves_row_count() -> None:
    forecast = make_forecast()

    scored = score_weather_forecast(
        forecast
    )

    assert len(scored) == len(
        forecast
    )


def test_weather_forecast_summary() -> None:
    scored = score_weather_forecast(
        make_forecast()
    )

    summary = weather_forecast_summary(
        scored
    )

    assert (
        0
        <= summary[
            "average_weather_score"
        ]
        <= 100
    )

    assert (
        summary["best_day_score"]
        >= summary["worst_day_score"]
    )


def test_missing_scoring_columns_are_rejected() -> None:
    forecast = pd.DataFrame(
        {
            "date": [
                "2026-08-20",
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="missing scoring columns",
    ):
        score_weather_forecast(
            forecast
        )


def test_invalid_latitude_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Latitude",
    ):
        fetch_weather_forecast(
            100,
            80,
        )


def test_invalid_longitude_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Longitude",
    ):
        fetch_weather_forecast(
            7,
            200,
        )


def test_invalid_forecast_days_are_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="between 1 and 16",
    ):
        fetch_weather_forecast(
            7,
            80,
            forecast_days=17,
        )


def test_successful_weather_api_response(
    monkeypatch,
) -> None:
    payload = {
        "daily": {
            "time": [
                "2026-08-20",
            ],
            "weather_code": [
                3,
            ],
            "temperature_2m_max": [
                30.0,
            ],
            "temperature_2m_min": [
                24.0,
            ],
            "precipitation_probability_max": [
                20,
            ],
            "precipitation_sum": [
                0.5,
            ],
        }
    }

    class MockResponse:
        def raise_for_status(
            self,
        ) -> None:
            return None

        def json(
            self,
        ) -> dict:
            return payload

    def mock_get(
        *args,
        **kwargs,
    ):
        return MockResponse()

    monkeypatch.setattr(
        "src.weather.client.requests.get",
        mock_get,
    )

    result = fetch_weather_forecast(
        7.957,
        80.7603,
        forecast_days=1,
    )

    assert len(result) == 1

    assert (
        result.iloc[0][
            "weather_code"
        ]
        == 3
    )


def test_weather_network_failure(
    monkeypatch,
) -> None:
    def mock_get(
        *args,
        **kwargs,
    ):
        raise requests.RequestException(
            "Network failure"
        )

    monkeypatch.setattr(
        "src.weather.client.requests.get",
        mock_get,
    )

    with pytest.raises(
        RuntimeError,
        match="Unable to retrieve",
    ):
        fetch_weather_forecast(
            7.957,
            80.7603,
            forecast_days=1,
        )


def test_missing_daily_response_is_rejected(
    monkeypatch,
) -> None:
    class MockResponse:
        def raise_for_status(
            self,
        ) -> None:
            return None

        def json(
            self,
        ) -> dict:
            return {}

    monkeypatch.setattr(
        "src.weather.client.requests.get",
        lambda *args, **kwargs: MockResponse(),
    )

    with pytest.raises(
        RuntimeError,
        match="does not contain daily",
    ):
        fetch_weather_forecast(
            7.957,
            80.7603,
            forecast_days=1,
        )


def test_inconsistent_daily_lengths_are_rejected(
    monkeypatch,
) -> None:
    payload = {
        "daily": {
            "time": [
                "2026-08-20",
                "2026-08-21",
            ],
            "weather_code": [
                3,
            ],
            "temperature_2m_max": [
                30,
                31,
            ],
            "temperature_2m_min": [
                24,
                24,
            ],
            "precipitation_probability_max": [
                20,
                30,
            ],
            "precipitation_sum": [
                0,
                1,
            ],
        }
    }

    class MockResponse:
        def raise_for_status(
            self,
        ) -> None:
            return None

        def json(
            self,
        ) -> dict:
            return payload

    monkeypatch.setattr(
        "src.weather.client.requests.get",
        lambda *args, **kwargs: MockResponse(),
    )

    with pytest.raises(
        RuntimeError,
        match="inconsistent",
    ):
        fetch_weather_forecast(
            7.957,
            80.7603,
            forecast_days=2,
        )