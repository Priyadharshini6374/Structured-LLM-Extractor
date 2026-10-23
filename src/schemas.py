
from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class InvoiceData(BaseModel):
    """Structured information extracted from an invoice."""

    model_config = ConfigDict(extra="forbid")

    invoice_number: Optional[str] = Field(
        default=None,
        description="The invoice identification number",
    )

    supplier: Optional[str] = Field(
        default=None,
        description="The name of the company issuing the invoice",
    )

    invoice_date: Optional[date] = Field(
        default=None,
        description="The invoice date in YYYY-MM-DD format",
    )

    total_amount: Optional[float] = Field(
        default=None,
        ge=0,
        allow_inf_nan=False,
        description="The final payable amount, which cannot be negative",
    )

    currency: Optional[str] = Field(
        default=None,
        pattern=r"^[A-Z]{3}$",
        description="Three-letter currency code, such as INR or USD",
    )

    @field_validator("invoice_number", "supplier", "currency")
    @classmethod
    def reject_empty_strings(cls, value):
        if value is not None and not value.strip():
            raise ValueError("Field must not be empty")
        return value

    @field_validator("invoice_date", mode="before")
    @classmethod
    def validate_date_format(cls, value):
        if value is None:
            return None

        if isinstance(value, date):
            return value

        if not isinstance(value, str):
            raise ValueError("Date must be a string")

        try:
            return date.fromisoformat(value)
        except ValueError as error:
            raise ValueError(
                "Date must be a valid calendar date in YYYY-MM-DD format"
            ) from error
