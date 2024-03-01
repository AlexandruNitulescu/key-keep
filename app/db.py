import sqlite3
import bcrypt


def database_instance():
    with sqlite3.connect("data.db") as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password TEXT)""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS credentials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    password TEXT,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id))""")
        
        conn.commit()


def signup(username: str, password: str):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    
    if result:
        conn.close()
        return False
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        return True
    
def login(username, password):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    stored_password = c.fetchone()[0]
    conn.close()

    if bcrypt.checkpw(password.encode('utf-8'), stored_password):
        stored_password = c.fetchone()
        if stored_password is None:
            print("Incorrect username or password.")
        elif bcrypt.checkpw(password.encode('utf-8'), stored_password[0]):
            print("Login successful!")
        else:
            print("Incorrect username or password.")