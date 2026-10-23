# Structured LLM Prompt Pipeline & JSON Extractor

A Python-based information extraction system that uses Google's Gemini API and Pydantic to transform unstructured invoices and resumes into structured, validated JSON data.

## Features

- **LLM Integration:** Uses the Google Gemini API to extract information from unstructured text.
- **Reusable Prompt Templates:** Stores invoice and resume prompts separately in text files.
- **Invoice Extraction:** Extracts invoice number, supplier, invoice date, total amount, and currency.
- **Resume Extraction:** Extracts candidate name, email, phone, education, skills, work experience, and projects.
- **Structured JSON Output:** Saves extracted information as readable JSON files.
- **Pydantic Validation:** Validates data types, required structures, dates, amounts, and currency formats.
- **Error Handling:** Handles empty API responses, invalid JSON, and validation failures.
- **Retry Configuration:** Configures retries for selected temporary API errors.

## Tech Stack

- Python
- Google Gemini API
- Pydantic
- python-dotenv
- JSON

## Project Structure

```text
Structured-LLM-Extractor/
├── input/
│   ├── invoice1.txt
│   ├── invoice2.txt
│   └── resume1.txt
├── output/
│   ├── invoice2.json
│   └── resume1.json
├── src/
│   ├── prompts/
│   │   ├── invoice_prompt.txt
│   │   └── resume_prompt.txt
│   ├── extractor.py
│   ├── main.py
│   ├── resume_extractor.py
│   ├── resume_schema.py
│   ├── run_extractor.py
│   ├── run_resume.py
│   └── schemas.py
├── test_schema.py
├── test_resume_schema.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd Structured-LLM-Extractor
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own Gemini API key. Never commit your actual API key to GitHub.

## Usage

Run the unified extraction program:

```powershell
python src\run_extractor.py
```

Select an option when prompted:

- Enter `1` to extract invoice information.
- Enter `2` to extract resume information.

The program reads the corresponding input file, calls the Gemini API, validates the extracted data, and saves the resulting JSON file in the `output/` folder.

## Example Output

Example invoice JSON:

```json
{
  "invoice_number": "INV-2026-002",
  "supplier": "Bright Star Services",
  "invoice_date": null,
  "total_amount": 8500.0,
  "currency": null
}
```

Missing values are represented as `null` rather than guessed.

## Running Schema Tests

Run the invoice validation tests:

```powershell
python test_schema.py
```

Run the resume validation tests:

```powershell
python test_resume_schema.py
```

The tests cover valid data, missing fields, negative invoice amounts, invalid currencies, invalid dates, and empty resume names.

## Security Notes

- Keep API keys in `.env` rather than in source code.
- Ensure `.env` is excluded through `.gitignore`.
- Do not upload personal resumes or confidential invoices without authorization.
- Review extracted information before using it in business-critical workflows.

## Future Enhancements

- Support PDF and DOCX document uploads.
- Add automated tests for extraction functions.
- Introduce batch processing for multiple documents.
- Add stricter handling of unexpected or malformed LLM responses.
- Support configurable extraction schemas for additional document types.

## Author

Priyadharshini

</