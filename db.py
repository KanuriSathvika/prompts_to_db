import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sathvika@310",
        database="prompts_db"
    )
    return conn
