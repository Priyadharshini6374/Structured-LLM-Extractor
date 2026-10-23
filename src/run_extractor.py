
import json
from pathlib import Path

from extractor import extract_invoice
from resume_extractor import extract_resume

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main():
    print("\n=== Structured LLM Extractor ===")
    print("1. Extract invoice data")
    print("2. Extract resume data")

    choice = input("Choose an option (1 or 2): ").strip()

    if choice == "1":
        input_file = PROJECT_ROOT / "input" / "invoice2.txt"
        output_file = PROJECT_ROOT / "output" / "invoice2.json"
        extract_function = extract_invoice

    elif choice == "2":
        input_file = PROJECT_ROOT / "input" / "resume1.txt"
        output_file = PROJECT_ROOT / "output" / "resume1.json"
        extract_function = extract_resume

    else:
        print("Invalid choice. Please enter 1 or 2.")
        return

    try:
        document_text = input_file.read_text(encoding="utf-8")
        extracted_data = extract_function(document_text)
        result = extracted_data.model_dump(mode="json")

        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(
            json.dumps(result, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        print("\nExtraction successful!")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"\nJSON saved to: {output_file}")

    except Exception as error:
        print(f"\nExtraction failed: {error}")


if __name__ == "__main__":
    main()
