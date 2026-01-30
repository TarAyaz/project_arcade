import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "record.db")


# === Инициализация БД ===
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            max_score INTEGER NOT NULL DEFAULT 0
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO records (id, max_score) VALUES (1, 0)")
    conn.commit()
    conn.close()


# === Получение рекорда ===
def get_max_score():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT max_score FROM records WHERE id = 1")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0


# === Функция обновления рекорда ===
def update_max_score(new_score):
    current = get_max_score()
    if new_score > current:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE records SET max_score = ? WHERE id = 1", (new_score,))
        conn.commit()
        conn.close()
        return True
    return False
