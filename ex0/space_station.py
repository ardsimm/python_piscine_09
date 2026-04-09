from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError


class SpaceStationModel(BaseModel):

    station_id: str = Field(
        min_length=3,
        max_length=10,
    )
    name: str = Field(
        min_length=1,
        max_length=50,
    )

    crew_size: int = Field(
        ge=1,
        le=20,
    )

    power_level: float = Field(
        ge=0.0,
        le=100.0,
    )

    oxygen_level: float = Field(
        ge=0.0,
        le=100.0,
    )

    last_maintenance: datetime = Field()

    is_operational: bool = Field(
        default=True
    )

    notes: Optional[str] = Field(
        default=None,
        max_length=200
    )

    def __str__(self) -> str:
        return "\n".join([
            f"ID: {self.is_operational})",
            f"Name: {self.name}",
            f"Crew: {self.crew_size} people",
            f"Power: {self.power_level}%",
            f"Oxygen: {self.oxygen_level}%",
            f"Status: {"Operational" if self.is_operational else "Inactive"}"
        ])


def main() -> None:
    print(
        "Space Station Data Validation",
        "========================================",
        sep="\n"
    )

    valid_space_station = SpaceStationModel(
        station_id="ISS0042",
        name="International Space Station",
        crew_size=8,
        power_level=98.42,
        oxygen_level=76.4,
        last_maintenance=datetime.today()
    )

    print("Valid station created:", valid_space_station, sep="\n")

    print("\n========================================")
    print("Expected validation error:")
    try:
        invalid_space_station = SpaceStationModel(
            station_id="ISS0042",
            name="International Space Station",
            crew_size=42,
            power_level=98.42,
            oxygen_level=76.4,
            last_maintenance=datetime.today()
        )
        print(invalid_space_station)
    except ValidationError as e:
        print(e)


if __name__ == "__main__":
    main()
