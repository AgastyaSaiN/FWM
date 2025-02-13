import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

def create_user(email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_user(email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    return user

init_db()  # Ensure the database is created when running
