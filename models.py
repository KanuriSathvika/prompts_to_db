from db import get_connection

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prompts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        level VARCHAR(50) NOT NULL,
        feature VARCHAR(100) NOT NULL,
        purpose VARCHAR(100) NOT NULL,
        section VARCHAR(100) NOT NULL,
        sub_section VARCHAR(100) NOT NULL,
        prompt TEXT NOT NULL,
        version INT DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()


def add_prompt(level, feature, purpose, section, sub_section, prompt):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prompts (level, feature, purpose, section, sub_section, prompt)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (level, feature, purpose, section, sub_section, prompt))
    conn.commit()
    cursor.close()
    conn.close()


def get_prompt(level, feature, purpose, section, sub_section):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT prompt FROM prompts
        WHERE level=%s AND feature=%s AND purpose=%s AND section=%s AND sub_section=%s
        ORDER BY version DESC LIMIT 1
    """, (level, feature, purpose, section, sub_section))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row[0] if row else None


def update_prompt(level, feature, purpose, section, sub_section, new_prompt):
    conn = get_connection()
    cursor = conn.cursor()

    # get latest version
    cursor.execute("""
        SELECT COALESCE(MAX(version), 0) FROM prompts
        WHERE level=%s AND feature=%s AND purpose=%s AND section=%s AND sub_section=%s
    """, (level, feature, purpose, section, sub_section))
    latest_version = cursor.fetchone()[0]

    # insert new version
    cursor.execute("""
        INSERT INTO prompts (level, feature, purpose, section, sub_section, prompt, version)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (level, feature, purpose, section, sub_section, new_prompt, latest_version + 1))
    conn.commit()
    cursor.close()
    conn.close()


def list_prompts():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM prompts ORDER BY created_at DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
