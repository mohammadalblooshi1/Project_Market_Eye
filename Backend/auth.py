import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password_hashed) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT user_id, password_hashed FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row and row[1] == hash_password(password):
        return row[0]
    return None

def log_activity(user_id, action):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO activity_logs (user_id, action) VALUES (?, ?)", (user_id, action))
    conn.commit()
    conn.close()
