
import os
import json
from pathlib import Path
from string import Template

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import ValidationError

from schemas import InvoiceData


# Locate the project and prompt template folders.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = PROJECT_ROOT / "src" / "prompts"


def load_prompt(template_name: str, **kwargs) -> str:
    """Load a prompt template and replace its placeholders."""
    template_path = PROMPTS_DIR / template_name
    prompt_text = template_path.read_text(encoding="utf-8")

    template = Template(
        prompt_text.replace("{{", "${").replace("}}", "}")
    )
    return template.substitute(**kwargs)


# Load the API key from the .env file.
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing. Check your .env file."
    )


# Create the Gemini client with retry settings.
client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        retry_options=types.HttpRetryOptions(
            attempts=5,
            initial_delay=1.0,
            max_delay=60.0,
            http_status_codes=[408, 429, 500, 502, 503, 504],
        )
    ),
)


def extract_invoice(invoice_text: str) -> InvoiceData:
    """
    Extract invoice information using a prompt template
    and validate the result with Pydantic.
    """

    # Load the external prompt and insert the invoice text.
    prompt = load_prompt(
        "invoice_prompt.txt",
        invoice_text=invoice_text,
    )

    # Ask Gemini to extract the invoice information.
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    raw_output = response.text.strip()

    # Remove optional Markdown code fences.
    if raw_output.startswith("```"):
        lines = raw_output.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        raw_output = "\n".join(lines).strip()

    # Parse the response as JSON.
    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Gemini returned invalid JSON: {error}"
        ) from error

    # Validate the extracted data using Pydantic.
    try:
        return InvoiceData.model_validate(data)
    except ValidationError as error:
        raise ValueError(
            f"Invoice data failed validation: {error}"
        ) from error
