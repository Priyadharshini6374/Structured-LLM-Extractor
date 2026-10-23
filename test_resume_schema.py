
from pydantic import ValidationError
from src.resume_schema import ResumeData

resume = ResumeData(
    full_name="Priyadharshini",
    email="priya.dharshini@example.com",
    phone="+91 9876543210",
    skills=["Python", "SQL"],
)

print("Valid resume test passed!")

incomplete = ResumeData()
assert incomplete.full_name is None
assert incomplete.skills == []
print("Missing-field test passed!")

try:
    ResumeData(full_name="   ")
except ValidationError:
    print("Empty-name test passed!")
else:
    raise AssertionError("Empty name was not rejected")

print("\nAll resume schema tests passed!")
