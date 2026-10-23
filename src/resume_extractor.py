
import json

from google.genai import types
from pydantic import ValidationError

from schemas import InvoiceData
from resume_schema import ResumeData

# Reuse the Gemini client configured in extractor.py.
from extractor import client, load_prompt


def extract_resume(resume_text: str) -> ResumeData:
    """Extract structured resume information using a prompt template."""

    prompt = load_prompt(
        "resume_prompt.txt",
        resume_text=resume_text,
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    try:
        data = json.loads(response.text)
        return ResumeData.model_validate(data)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Gemini returned invalid JSON: {error}"
        ) from error
    except ValidationError as error:
        raise ValueError(
            f"Resume data failed validation: {error}"
        ) from error