from datetime import date
from enum import StrEnum
from typing import List
from pydantic import BaseModel, Field, model_validator


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
