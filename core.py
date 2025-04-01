import connector as conn

try:
    res = conn.execute("SELECT COUNT(*) FROM Accounts")[0][0]
    print(f"{res} account(s) found")
except:
    from setup_database import create_database
    create_database()

# session lifetime, in seconds, set to one hour
SESSION_LIFETIME = 3600

def get_datetime():
    """returns the formated date and time"""
    from datetime import datetime

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_timestamp():
    """returns the current time stamp"""
    from time import time

    return time()

def hash_password(password, salt = None):
    """returns the hashed password with the salt used to hash it"""
    import hashlib, binascii, os

    # Hashing configuration
    hash_algorithm = 'sha256'
    hash_iterations = 100_000
    hash_length = 64  # bytes (512 bits)

    # Generates a random salt if none is provided
    if salt is None:
        salt = os.urandom(16)  # 128-bit salt
    else:
        salt = binascii.unhexlify(salt)

    # Uses the salt and the configuration
    # to hash the password
    key = hashlib.pbkdf2_hmac(hash_algorithm, password.encode(), salt, hash_iterations, dklen = hash_length)
    return {
        "salt": binascii.hexlify(salt).decode(),
        "hash": binascii.hexlify(key).decode()
    }

def create_session(username):
    """creates a session for the username provided
    returns the token and the expiration time"""
    import secrets

    token = secrets.token_hex(32)
    expiration = get_timestamp() + SESSION_LIFETIME
    if conn.create_session(username, token, expiration):
        return token, expiration
    return {"status": "error", "message": "Session creation failed"}

def get_username_from_token(token):
    res = conn.check_session(token)

    if res:
        return res

    return {"status": "error", "message": "Invalid or expired session"}

def get_user_info_from_username(username):
    res = conn.get_info_from_username(username)

    if res:
        return res

    return {"status": "error", "message": f"Invalid account '{username}'"}

def login(username, password):
    """Logs the user in
    returns session token and expiration time"""

    # Checks if user exists
    if not conn.check_username(username):
        return {"status": "error", "message": f"No user '{username}'"}

    # Get hashed_password and salt from database
    hash_data = conn.get_hash_data_from_username(username)
    if not hash_data:
        return {"status": "error", "message": f"No password for username '{username}'"}

    # Recreate hash with stored salt
    hashed_attempt = hash_password(password, salt = hash_data[0][1])

    # Checks if the password hash is the same as the one stored
    if hashed_attempt["hash"] != hash_data[0][0]:
        return {"status": "error", "message": f"Invalid password for User ID {username}"}

    # Creates user session if password is correct
    token, expiration = create_session(username)

    return {"status": "success", "message": "Login successful", "token": token, "expiration": expiration}

def logout(username):
    """Deletes all sessions for username"""

    res = conn.delete_session(username)

    if res:
        return {"status": "success", "message": "Logout successful"}

    return {"status": "error", "message": "Logout failed"}

def register(username, password):
    """Creates account with username and password"""

    # Checks if user already exists
    if conn.check_username(username):
        return {"status": "error", "message": "User already exists"}

    # Hash password
    hash_data = hash_password(password)

    # Create account
    res = conn.create_account(username, hash_data['salt'], hash_data['hash'], get_datetime())

    if res:
        return {"status": "success", "message": "Account creation successful"}

    return {"status": "error", "message": "Account creation failed"}