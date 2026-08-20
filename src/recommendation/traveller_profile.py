from dataclasses import dataclass

import numpy as np


INTERESTS = [
    "beach",
    "wildlife",
    "hiking",
    "nature",
    "culture",
    "history",
    "adventure",
]

TRAVEL_STYLES = {
    "Budget",
    "Balanced",
    "Comfort",
}

CROWD_PREFERENCES = {
    "No Preference",
    "Prefer Less Crowded Places",
    "Popular Tourist Places",
}

TRANSPORT_OPTIONS = {
    "Public Transport",
    "Mixed Transport",
    "Private Vehicle",
}


@dataclass(frozen=True)
class TravellerProfile:
    """Structured representation of a CeylonCompass traveller."""

    starting_point: str
    trip_days: int
    budget_usd: float
    travel_style: str
    crowd_preference: str
    transport: str
    interests: tuple[str, ...]

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        """Validate traveller input before recommendation modelling."""

        if not self.starting_point.strip():
            raise ValueError("Starting point cannot be empty.")

        if self.trip_days < 1:
            raise ValueError("Trip duration must be at least 1 day.")

        if self.budget_usd <= 0:
            raise ValueError("Budget must be greater than 0.")

        if self.travel_style not in TRAVEL_STYLES:
            raise ValueError(
                f"Invalid travel style: {self.travel_style}"
            )

        if self.crowd_preference not in CROWD_PREFERENCES:
            raise ValueError(
                f"Invalid crowd preference: {self.crowd_preference}"
            )

        if self.transport not in TRANSPORT_OPTIONS:
            raise ValueError(
                f"Invalid transport option: {self.transport}"
            )

        if not self.interests:
            raise ValueError(
                "At least one travel interest must be selected."
            )

        normalized_interests = {
            interest.lower().strip()
            for interest in self.interests
        }

        unknown_interests = (
            normalized_interests - set(INTERESTS)
        )

        if unknown_interests:
            raise ValueError(
                "Unknown travel interests: "
                + ", ".join(sorted(unknown_interests))
            )

    @property
    def normalized_interests(self) -> tuple[str, ...]:
        """Return standardized lowercase interest names."""

        return tuple(
            interest.lower().strip()
            for interest in self.interests
        )

    def to_interest_vector(self) -> np.ndarray:
        """
        Convert selected interests into the same feature space
        used by destination data.

        Selected interest = 5
        Unselected interest = 0
        """

        selected = set(self.normalized_interests)

        return np.array(
            [
                5.0 if interest in selected else 0.0
                for interest in INTERESTS
            ],
            dtype=float,
        )

    def daily_budget(self) -> float:
        """Return the traveller's available budget per trip day."""

        return self.budget_usd / self.trip_days

    def to_dict(self) -> dict:
        """Convert the profile into a serializable dictionary."""

        return {
            "starting_point": self.starting_point,
            "trip_days": self.trip_days,
            "budget_usd": self.budget_usd,
            "daily_budget_usd": round(
                self.daily_budget(),
                2,
            ),
            "travel_style": self.travel_style,
            "crowd_preference": self.crowd_preference,
            "transport": self.transport,
            "interests": list(
                self.normalized_interests
            ),
        }