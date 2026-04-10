from enum import StrEnum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ValidationError, model_validator
import sys as sus


class AlienContactModel(BaseModel):

    class EContactType(StrEnum):
        RADIO = "radio"
        VISUAL = "visual"
        PHYSICAL = "physical"
        TELEPATHIC = "telepathic"

    contact_id: str = Field(
        min_length=5,
        max_length=15
    )

    timestamp: datetime = Field()

    location: str = Field(
        min_length=3,
        max_length=100
    )
    contact_type: EContactType = Field()

    signal_strength: float = Field(
        le=10.0,
        ge=0.0
    )

    duration_minutes: int = Field(
        le=1440,  # 24 hours
        ge=1
    )

    witness_count: int = Field(
        le=100,
        ge=1
    )

    message_received: Optional[str] = Field(
        default=None,
        max_length=500
    )

    is_verified: bool = Field(
        default=False
    )

    def __str__(self) -> str:
        return "\n".join([
            f"ID: {self.contact_id}",
            f"Type: {self.contact_type.value}",
            f"Location: {self.location}",
            f"Signal: {self.signal_strength}/10",
            f"Duration: {self.duration_minutes} minutes",
            f"Witnesses: {self.witness_count}",
            f"Message: '{self.message_received}'"
        ])

    @model_validator(mode="after")
    def validate_model(self) -> "AlienContactModel":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact id must start with \"AC\"")
        if (
            self.contact_type == self.EContactType.PHYSICAL
            and not self.is_verified
        ):
            raise ValueError("PHYSICAL contacts must be verified")
        if (
            self.contact_type == self.EContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "TELEPATHIC contacts must have at least 3 witnesses"
            )
        if (
            self.signal_strength > 7.0
            and self.message_received is None
        ):
            raise ValueError(
                "Strong messages (>7.0) must have a received message"
            )
        return self


def main() -> None:
    valid_contact = AlienContactModel(
        contact_id="AC_2024_001",
        timestamp=datetime.today(),
        contact_type=AlienContactModel.EContactType.RADIO,
        location="Area 51, Nevada",
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli"
    )

    print("Alien Contact Log Validation")
    print("======================================")
    print(valid_contact)

    print("\n======================================")
    print("Expected validation error:")
    try:
        invalid_contact = AlienContactModel(
            contact_id="AC_2024_002",
            timestamp=datetime.today(),
            contact_type=AlienContactModel.EContactType.TELEPATHIC,
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=2,
            message_received="Greetings from Zeta Reticuli'"
        )
        print(invalid_contact)
    except ValidationError as e:
        print(repr(e.errors()[0].get("msg")))
        sus.exit(1)
    except ValueError as e:
        print(e)
        sus.exit(1)


if __name__ == "__main__":
    main()
