
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ResumeData(BaseModel):
    """Structured information extracted from a resume."""

    model_config = ConfigDict(extra="forbid")

    full_name: Optional[str] = Field(
        default=None,
        description="Candidate's full name",
    )

    email: Optional[str] = Field(
        default=None,
        description="Candidate's email address",
    )

    phone: Optional[str] = Field(
        default=None,
        description="Candidate's phone number",
    )

    education: list[str] = Field(
        default_factory=list,
        description="Education qualifications and institutions",
    )

    skills: list[str] = Field(
        default_factory=list,
        description="Technical and professional skills",
    )

    work_experience: list[str] = Field(
        default_factory=list,
        description="Jobs, internships, and responsibilities",
    )

    projects: list[str] = Field(
        default_factory=list,
        description="Projects completed by the candidate",
    )

    @field_validator("full_name", "email", "phone")
    @classmethod
    def reject_empty_strings(cls, value):
        if value is not None and not value.strip():
            raise ValueError("Field must not be empty")
        return value
