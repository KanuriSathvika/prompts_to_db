from db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT * FROM prompts")
rows = cursor.fetchall()   # read all rows at once

cursor.close()
conn.close()

for row in rows:
    print(row)
