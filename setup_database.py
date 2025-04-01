def create_database():
    import sqlite3

    # connects to database, creating it if it doesn't already exist
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # creates the Accounts table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Accounts (
        Id INTEGER PRIMARY KEY,
        Username TEXT,
        PasswordHash TEXT,
        PasswordSalt TEXT,
        CreationDate TEXT
    )
    """)

    # creates the Sessions table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Sessions (
        Username TEXT,
        Token TEXT,
        Expiration TEXT
    )
    """)

    conn.commit()

    cur.close()
    conn.close()

    print("Database created")