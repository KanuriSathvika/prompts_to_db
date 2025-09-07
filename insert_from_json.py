import sqlite3
import json
import os

# File path
file_path = "prompts_chat.json"
file_name = os.path.basename(file_path)

# Load JSON
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

system_prompt = data["chat_prompt"]["system_prompt"]
user_prompt = data["chat_prompt"].get("user_prompt", {})

# Connect to SQLite DB
conn = sqlite3.connect("prompts.db")
cursor = conn.cursor()

# Create table (if not exists)
cursor.execute("""
CREATE TABLE IF NOT EXISTS prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api TEXT NOT NULL,
    purpose TEXT NOT NULL,
    sub_purpose TEXT NOT NULL,
    main_prompt TEXT,
    do TEXT,
    donts TEXT,
    examples TEXT,
    user_prompt TEXT
)
""")

# Insert prompt
cursor.execute("""
INSERT INTO prompts (api, purpose, sub_purpose, main_prompt, do, donts, examples, user_prompt)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (
    file_name,
    "chat_prompt",
    "system_prompt",
    system_prompt["main_prompt"],
    system_prompt["do"],
    system_prompt["donts"],
    system_prompt["examples"],
    json.dumps(user_prompt)   # store as JSON string
))

conn.commit()
conn.close()
print("Prompt inserted into SQL database")
