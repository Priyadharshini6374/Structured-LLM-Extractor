
import json
from pathlib import Path

from resume_extractor import extract_resume

PROJECT_ROOT = Path(__file__).resolve().parent.parent

input_file = PROJECT_ROOT / "input" / "resume1.txt"
output_file = PROJECT_ROOT / "output" / "resume1.json"


def main():
    try:
        resume_text = input_file.read_text(encoding="utf-8")

        resume = extract_resume(resume_text)

        resume_data = resume.model_dump(mode="json")

        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(
            json.dumps(resume_data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        print("Resume extraction successful!")
        print(json.dumps(resume_data, indent=2, ensure_ascii=False))
        print(f"\nJSON saved to: {output_file}")

    except Exception as error:
        print(f"Resume extraction failed: {error}")


if __name__ == "__main__":
    main()
