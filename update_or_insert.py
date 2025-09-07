from db import get_connection

def upsert_prompt(level, feature, purpose, section, sub_section, prompt):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO prompts (level, feature, purpose, section, sub_section, prompt)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE prompt = VALUES(prompt)
    """
    cursor.execute(query, (level, feature, purpose, section, sub_section, prompt))
    conn.commit()

    cursor.close()
    conn.close()
    print("✅ Prompt inserted/updated successfully.")



# Case 1: If row exists → it will update the prompt
# Case 2: If row does not exist → it will insert new row
upsert_prompt(
    level="Organization",
    feature="Chat",
    purpose="Generate_questions",
    section="System_prompt",
    sub_section="do",
    prompt="Always generate 5 relevant questions for the document"
)