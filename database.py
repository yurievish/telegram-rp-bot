import sqlite3

def init_db():
    conn = sqlite3.connect("nicknames.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nicknames (
            user_id INTEGER PRIMARY KEY,
            nickname TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def set_nickname(user_id, nickname):
    conn = sqlite3.connect("nicknames.db")
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO nicknames (user_id, nickname) VALUES (?, ?)", (user_id, nickname))
    conn.commit()
    conn.close()

def get_nickname(user_id):
    conn = sqlite3.connect("nicknames.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nickname FROM nicknames WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
