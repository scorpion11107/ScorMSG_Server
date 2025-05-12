def time():
    import time

    return time.time()

def execute(query):
    import sqlite3

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(query)
    res = cur.fetchall()

    conn.commit()

    cur.close()
    conn.close()

    return res

def create_session(username, token, expiration):
    if username and token and expiration > time():
        execute(f"INSERT INTO Sessions (Username, Token, Expiration) VALUES ('{username}', '{token}', '{expiration}')")
        return True
    return False

def delete_session(username):
    if username:
        execute(f"DELETE FROM Sessions WHERE Username = '{username}'")
        return True

    return False

def check_session(token):
    if token:
        res = execute(f"SELECT Username FROM Sessions WHERE Token = '{token}' AND Expiration > '{time()}'")
        if res:
            return res[0][0]

    return False

def get_info_from_username(username):
    if username:
        res = execute(f"SELECT Username, CreationDate FROM Accounts WHERE Username = '{username}'")
        if res:
            return res[0]

    return False

def get_hash_data_from_username(username):
    if username:
        res = execute(f"SELECT PasswordSalt, PasswordHash FROM Accounts WHERE Username = '{username}'")
        if res:
            return res

    return False

def check_username(username):
    if username:
        res = execute(f"SELECT COUNT(*) FROM Accounts WHERE Username = '{username}'")[0][0]
        if res:
            return res == 1

    return False

def create_account(username, password_hash, password_salt, creation_date):
    if username and password_hash and password_salt and creation_date:
        execute(f"INSERT INTO Accounts (Username, PasswordHash, PasswordSalt, CreationDate) VALUES ('{username}', '{password_hash}', '{password_salt}', '{creation_date}')")
        return True

    return False