
import json
from pathlib import Path

from extractor import extract_invoice


# Find the project root directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Locate the input and output files.
input_file = PROJECT_ROOT / "input" / "invoice2.txt"
output_file = PROJECT_ROOT / "output" / "invoice2.json"


def main():
    try:
        # Read the invoice text.
        invoice_text = input_file.read_text(encoding="utf-8")

        # Extract and validate the invoice information.
        invoice = extract_invoice(invoice_text)

        # Convert the validated object to a dictionary.
        invoice_data = invoice.model_dump()

        # Save the structured data as a JSON file.
        output_file.parent.mkdir(parents=True, exist_ok=True)

        output_file.write_text(
            json.dumps(invoice_data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        print("Invoice extraction successful!")
        print(json.dumps(invoice_data, indent=2, ensure_ascii=False))
        print(f"\nJSON saved to: {output_file}")

    except Exception as error:
        print(f"Invoice extraction failed: {error}")


if __name__ == "__main__":
    main()
