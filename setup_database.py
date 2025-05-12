def create_database():
    import sqlite3

    # connects to database, creating it if it doesn't already exist
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # creates the Accounts table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Accounts (
            id INTEGER PRIMARY KEY,
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

    # creates the Conversations table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Conversations (
            id INTEGER PRIMARY KEY,
            user1_id INT,
            user2_id INT,
            DateLastMessage TEXT,
            CreationDate TEXT
        )
        """)

    # creates the Messages table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Messages (
            id INTEGER PRIMARY KEY,
            conversation_id INT,
            sender_id INT,
            content TEXT,
            SendDate TEXT,
            seen INT
        )
        """)

    conn.commit()

    cur.close()
    conn.close()

    print("Database created")