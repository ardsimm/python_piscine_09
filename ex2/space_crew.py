from datetime import date
from enum import StrEnum
import sys as sus  # :rire:
from typing import List
from pydantic import BaseModel, Field, ValidationError, model_validator


class SpaceCrewModel(BaseModel):

    class ERank(StrEnum):
        CADET = "cadet"
        OFFICER = "officer"
        LIEUTENANT = "lieutenant"
        CAPTAIN = "captain"
        COMMANDER = "commander"

    member_id: str = Field(
        min_length=3,
        max_length=10
    )

    name: str = Field(
        min_length=2,
        max_length=50
    )

    rank: ERank = Field()

    age: int = Field(
        le=80,
        ge=18
    )

    specialization: str = Field(
        min_length=3,
        max_length=30
    )

    years_experience: int = Field(
        le=50,
        ge=0
    )

    is_active: bool = Field(
        default=True
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.rank.value}) - {self.specialization}"


class SpaceMissionModel(BaseModel):

    mission_id: str = Field(
        min_length=5,
        max_length=15
    )

    mission_name: str = Field(
        min_length=3,
        max_length=100
    )

    destination: str = Field(
        min_length=3,
        max_length=50
    )

    launch_date: date = Field()

    duration_days: int = Field(
        le=3650,  # 10 years
        ge=1
    )

    crew: List[SpaceCrewModel] = Field(
        min_length=1,
        max_length=12
    )

    mission_status: str = Field(
        default="planned"
    )

    budget_millions: float = Field(
        ge=1.0,
        le=10000.0
    )

    @model_validator(mode="after")
    def validate_model(self) -> "SpaceMissionModel":
        #  RULE: Mission id must start with an M
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission id must start with an M")

        # RULE: A mission must have at least one commander or captain
        if all(
            member.rank != SpaceCrewModel.ERank.COMMANDER
            and member.rank != SpaceCrewModel.ERank.CAPTAIN
            for member in self.crew
        ):
            raise ValueError(
                "A mission must have at least one commander or captain"
            )

        # RULE: Long missions (at least 1 year) must have at least 50%
        # of experienced crew members (> 1 year)
        if (
            self.duration_days >= 365
            and len([
                member
                for member
                in self.crew
                if member.years_experience >= 5
            ]) < len(self.crew) // 2
        ):
            raise ValueError(
                "Long missions (>= 365) must have at least 50%" +
                " experienced crew (5+ years)"
            )

        # RULE: All crew members must be active
        if any(
            not member.is_active
            for member in self.crew
        ):
            raise ValueError("All crew members must ne active")
        return self

    def __str__(self) -> str:
        ret_str = "\n".join([
            f"Mission: {self.mission_name}",
            f"ID: {self.mission_id}",
            f"Destination: {self.destination}",
            f"Duration: {self.duration_days} days",
            f"Budget: ${self.budget_millions}M",
            f"Crew size: {len(self.crew)}",
            "Crew members:\n",
        ])
        return ret_str + "\n".join([
            f"- {crewmate.__str__()}"
            for crewmate in self.crew
        ])


def main() -> None:
    valid_space_crew = [
        SpaceCrewModel(
            member_id="COM_01",
            name="Sarah Connor",
            rank=SpaceCrewModel.ERank.COMMANDER,
            age=42,
            specialization="Mission Command",
            years_experience=21
        ),
        SpaceCrewModel(
            member_id="LIE_01",
            name="Jean-Phil Monslip",
            rank=SpaceCrewModel.ERank.LIEUTENANT,
            age=18,
            specialization="Navigation",
            years_experience=12
        ),
        SpaceCrewModel(
            member_id="COM_01",
            name="Kapinarc",
            rank=SpaceCrewModel.ERank.OFFICER,
            age=69,
            specialization="Engineering",
            years_experience=34,
        )
    ]

    valid_mission = SpaceMissionModel(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        duration_days=900,
        crew=valid_space_crew,
        budget_millions=2500.0,
        launch_date=date.today()
    )
    print("Space Mission Crew Validation")
    print("=========================================")
    print(valid_mission)

    print("\n=========================================")
    print("Expected validation error:")
    try:

        invalid_mission = SpaceMissionModel(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            duration_days=900,
            crew=[
                SpaceCrewModel(
                    member_id="LIE_01",
                    name="Jean-Phil Monslip",
                    rank=SpaceCrewModel.ERank.LIEUTENANT,
                    age=18,
                    specialization="Navigation",
                    years_experience=12
                ),
                SpaceCrewModel(
                    member_id="COM_01",
                    name="Kapinarc",
                    rank=SpaceCrewModel.ERank.OFFICER,
                    age=69,
                    specialization="Engineering",
                    years_experience=34,
                )
            ],
            budget_millions=2500.0,
            launch_date=date.today()
        )
        print(invalid_mission)
    except ValidationError as e:
        print(repr(e.errors()[0].get("msg")))
        sus.exit(1)
    except ValueError as e:
        print(e)
        sus.exit(1)


if __name__ == "__main__":
    main()
