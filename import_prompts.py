import json
from pathlib import Path
from pymongo import MongoClient

# CONFIG (adjust if needed)
MONGO_URI = "mongodb+srv://kanurisathvika310_db_user:tender_db@prompts.nhy93fe.mongodb.net/"
DB_NAME = "PromptsDB_org"  # keep same as fetch_fields.py
COLLECTION_NAME = "Keyword"  # reuse existing indexed collection
PROMPTS_FILE = Path(__file__).parent / "prompts.json"

# Optional: mapping for nicer purpose strings (edit as you like)
PURPOSE_MAP = {
    "chat_query": "Chat query answering",
    "chat_generate_questions": "Generate contextual questions",
    "prompt_builder": "Question prompt templates",
    "chat_pdf_summary": "PDF summary assistant",
    "md_alternativ_prompt": "Markdown conversion variant",
    "pdf_to_markdown": "PDF to markdown extraction",
    "hyde_prompt": "Hypothetical document expansion",
    "custom_retrieval": "Custom retrieval QA"
}

client = MongoClient(MONGO_URI)
collection = client[DB_NAME][COLLECTION_NAME]


def key_to_purpose(key: str) -> str:
    return PURPOSE_MAP.get(key, key.replace('_', ' ').title())


def normalize_entry(api_key: str, value):
    """Yield one or more Mongo-ready documents for this top-level key."""
    purpose_base = key_to_purpose(api_key)

    # Case 1: object with system_prompt
    if isinstance(value, dict) and "system_prompt" in value:
        sp = value["system_prompt"]
        if isinstance(sp, list):
            main_prompt = "\n".join(line.strip() for line in sp)
        else:
            main_prompt = str(sp)
        yield {
            "api": api_key,
            "purpose": purpose_base,
            "main_prompt": main_prompt,
        }

    # Case 2: prompt_builder with two templates
    if api_key == "prompt_builder" and isinstance(value, dict):
        for template_field in ("part_question_template", "summary_question_template"):
            if template_field in value:
                yield {
                    "api": api_key,
                    "purpose": f"{purpose_base} - {template_field}",
                    "main_prompt": value[template_field]
                }

    # Case 3: md_alternativ_prompt is a list of variants
    if api_key == "md_alternativ_prompt" and isinstance(value, list):
        for idx, variant in enumerate(value, start=1):
            yield {
                "api": api_key,
                "purpose": f"{purpose_base} v{idx}",
                "main_prompt": variant
            }

    # Case 4: pdf_to_markdown simple object
    if api_key == "pdf_to_markdown" and isinstance(value, dict) and "system_prompt" in value:
        sp = value["system_prompt"]
        yield {
            "api": api_key,
            "purpose": purpose_base,
            "main_prompt": sp
        }

    # Case 5: hyde_prompt simple
    if api_key == "hyde_prompt" and isinstance(value, dict) and "system_prompt" in value:
        yield {
            "api": api_key,
            "purpose": purpose_base,
            "main_prompt": value["system_prompt"]
        }

    # Case 6: custom_retrieval
    if api_key == "custom_retrieval" and isinstance(value, dict) and "system_prompt" in value:
        yield {
            "api": api_key,
            "purpose": purpose_base,
            "main_prompt": value["system_prompt"]
        }


def load_prompts(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    data = load_prompts(PROMPTS_FILE)
    docs = []
    for api_key, value in data.items():
        for doc in normalize_entry(api_key, value):
            # basic deduplication key
            doc["_composite_key"] = f"{doc['api']}|{doc['purpose']}"
            docs.append(doc)

    # Remove existing docs with same composite keys to avoid duplicates
    if docs:
        keys = [d["_composite_key"] for d in docs]
        collection.delete_many({"_composite_key": {"$in": keys}})
        collection.insert_many(docs)
        print(f"Inserted {len(docs)} documents into {DB_NAME}.{COLLECTION_NAME}")
    else:
        print("No documents prepared.")


if __name__ == "__main__":
    main()
