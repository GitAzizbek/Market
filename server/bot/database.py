import sqlite3

# 🔹 DB ulanish
DB_NAME = "users.db"

def create_table():
    """Foydalanuvchilar jadvalini yaratish"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                phone TEXT,
                token TEXT
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Xatolik yuz berdi: {e}")
    finally:
        if conn:
            conn.close()

def save_user(telegram_id, phone, token):
    """Foydalanuvchini bazaga qo'shish yoki yangilash"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (telegram_id, phone, token) 
            VALUES (?, ?, ?) 
            ON CONFLICT(telegram_id) 
            DO UPDATE SET phone = excluded.phone, token = excluded.token
        """, (telegram_id, phone, token))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Xatolik yuz berdi: {e}")
    finally:
        if conn:
            conn.close()

def get_user(telegram_id):
    """Foydalanuvchini bazadan olish"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        user = cursor.fetchone()
        return user
    except sqlite3.Error as e:
        print(f"Xatolik yuz berdi: {e}")
        return None
    finally:
        if conn:
            conn.close()

# 🔹 Dastlab jadvalni yaratamiz
create_table()