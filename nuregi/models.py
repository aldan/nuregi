"""Models for Registrar objects."""

from datetime import datetime
from typing import Self

from pydantic import BaseModel, Field, model_validator


class Semester(BaseModel):
    """Model for Semester."""

    id: str
    name: str


class SectionPeriod(BaseModel):
    """Model for SectionPeriod.

    Period is calculated in minutes in a week (7*24*60).
    """

    start: int | None = Field(ge=0, lt=10080)
    end: int | None = Field(ge=0, lt=10080)
    room: str | None
    distant: bool = False

    @model_validator(mode="after")
    def check_required_if_not_distant(self) -> Self:
        """Validate start, end, room fields are required when distant is False."""
        if not self.distant and (self.start is None or self.end is None or self.room is None):
            msg = "All fields are required for non-distant sections"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def check_start_before_end(self) -> Self:
        """Validate start time must be earlier than end."""
        if self.start and self.end and self.start >= self.end:
            msg = "Period start must be earlier than end"
            raise ValueError(msg)
        return self


class Section(BaseModel):
    """Model for Course Section."""

    code: str
    periods: list[SectionPeriod]
    instructors: str | None = "N/A"


class Course(BaseModel):
    """Model for Course."""

    school: str
    level: str
    code: str
    title: str
    credits_us: float = Field(ge=0.0)
    credits_eu: int = Field(ge=0)
    start_date: datetime
    end_date: datetime
    enrolled: int = Field(ge=0)
    capacity: int = Field(ge=0)
    sections: list[Section]
