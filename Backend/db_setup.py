import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Creating users table
c.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hashed TEXT,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

# Creating activity_logs table
c.execute('''CREATE TABLE IF NOT EXISTS activity_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)''')

conn.commit()
conn.close()
