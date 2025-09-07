import json
from db import get_connection

def upsert_prompts_from_json(json_file):
    conn = get_connection()
    cursor = conn.cursor()

    with open(json_file, "r") as f:
        prompts = json.load(f)

    for p in prompts:
        # Check if row exists
        cursor.execute("""
            SELECT id FROM prompts 
            WHERE level=%s AND feature=%s AND section=%s 
                  AND sub_section=%s AND purpose=%s
        """, (p["level"], p["feature"], p["section"], p["sub_section"], p["purpose"]))
        
        row = cursor.fetchone()

        if row:
            # Update existing row
            cursor.execute("""
                UPDATE prompts 
                SET prompt=%s
                WHERE id=%s
            """, (p["prompt"], row[0]))
            print(f"✅ Updated prompt for {p['level']} - {p['feature']} - {p['section']}")
        else:
            # Insert new row
            cursor.execute("""
                INSERT INTO prompts (level, feature, section, sub_section, purpose, prompt)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (p["level"], p["feature"], p["section"], p["sub_section"], p["purpose"], p["prompt"]))
            print(f"➕ Inserted new prompt for {p['level']} - {p['feature']} - {p['section']}")

    conn.commit()
    cursor.close()
    conn.close()
    print("✔️ All prompts processed.")

# Run
upsert_prompts_from_json("prompts.json")
