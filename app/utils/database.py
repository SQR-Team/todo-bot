def init_database(cur, conn):
    cur.execute('''CREATE TABLE IF NOT EXISTS tasks (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   task TEXT,
                   category TEXT,
                   deadline TEXT,
                   completed INTEGER DEFAULT 0
                )''')
    conn.commit()
