import json
import re
from langfuse.decorators import observe, langfuse_context
from langfuse.openai import openai
import os
from typing import List, Optional
import uuid

# Konfiguracja Langfuse
os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LANGFUSE_PUBLIC_KEY")
os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LANGFUSE_SECRET_KEY")
os.environ["LANGFUSE_HOST"] = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

# Konfiguracja OpenAI
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Ścieżka do prompta
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_PATH = os.path.join(BASE_DIR, "..", "prompts", "recipe_prompt.txt")

def load_prompt(file_path: str) -> str:
    """Ładuje prompt z pliku tekstowego."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

PROMPT_TEMPLATE = load_prompt(PROMPT_PATH)

def clean_json_response(response_text: str) -> str:
    response_text = response_text.strip()
    response_text = re.sub(r"^```json\s*", "", response_text, flags=re.MULTILINE)
    response_text = re.sub(r"\s*```$", "", response_text, flags=re.MULTILINE)
    return response_text.strip()

@observe()
def process_single_pdf_part(part: str, session_id: str, previous_context: Optional[str] = None) -> List[dict]:
    langfuse_context.update_current_trace(session_id=session_id)

    messages = [{"role": "system", "content": PROMPT_TEMPLATE}]

    if previous_context:
        messages.append({"role": "user", "content": f"Previous context: {previous_context}"})

    messages.append({"role": "user", "content": f"Extract all recipes from this text:\n{part}"})

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )

        raw_content = response.choices[0].message.content.strip()
        print("\n🔹 [DEBUG] RAW OpenAI Response:")
        print(raw_content)

        if not raw_content:
            raise ValueError("OpenAI returned an empty response.")

        cleaned_json = clean_json_response(raw_content)
        print("\n🔹 [DEBUG] Cleaned JSON Response:")
        print(cleaned_json)

        try:
            parsed_data = json.loads(cleaned_json)
        except json.JSONDecodeError:
            print("\n[ERROR] Invalid JSON Format Received:")
            print(cleaned_json)
            raise ValueError(f"Invalid JSON format received: {cleaned_json}")

        if isinstance(parsed_data, dict):
            parsed_data = [parsed_data]

        return parsed_data

    except Exception as e:
        print("\n[ERROR] Exception occurred while processing OpenAI response:")
        print(str(e))
        return [{"error": f"Error processing part: {str(e)}"}]

def process_pdf_parts_with_gpt(pdf_parts: List[str]) -> List[dict]:
    """Przetwarza listę fragmentów PDF i zwraca **listę WSZYSTKICH przepisów**."""
    results = []
    session_id = str(uuid.uuid4())
    previous_context = None

    for part in pdf_parts:
        response = process_single_pdf_part(part, session_id, previous_context)

        if isinstance(response, list):
            results.extend(response)
        else:
            results.append(response)

        for recipe in response:
            if recipe.get("incomplete", False):
                previous_context = json.dumps(recipe, ensure_ascii=False, indent=2)
                break
        else:
            previous_context = None

    return results
