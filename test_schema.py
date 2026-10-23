
from pydantic import ValidationError
from src.schemas import InvoiceData

invoice = InvoiceData(
    invoice_number="INV-1001",
    supplier="ABC Technologies",
    invoice_date="2026-10-15",
    total_amount=12500.0,
    currency="INR",
)

print("Valid invoice test passed!")

incomplete = InvoiceData(
    invoice_number="INV-1002",
    supplier="Bright Star Services",
    total_amount=8500.0,
)

assert incomplete.invoice_date is None
assert incomplete.currency is None
print("Missing-field test passed!")

try:
    InvoiceData(invoice_number="INV-1003", total_amount=-500)
except ValidationError:
    print("Negative amount test passed!")
else:
    raise AssertionError("Negative amount was not rejected")

try:
    InvoiceData(currency="RUPEES")
except ValidationError:
    print("Invalid currency test passed!")
else:
    raise AssertionError("Invalid currency was not rejected")

try:
    InvoiceData(invoice_date="2026-02-30")
except ValidationError:
    print("Invalid date test passed!")
else:
    raise AssertionError("Invalid date was not rejected")

print("\nAll schema tests passed!")
