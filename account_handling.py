from hashlib import sha512


class Account:

    def __init__(self, username: str, password: str, role: str = "", restaurant: str = ""):
        self.username: str = username
        self.password: str = password
        self.role: str = role
        self.restaurant: str = restaurant


def hash_string(string_to_hash: str) -> str:
    salt = "A?5J/b8-fe+w8b42,9B_J743dl"
    hashing_string = sha512((string_to_hash + salt).encode())
    return hashing_string.hexdigest()


def login(account):
    hashed_username: str = hash_string(account.username)
    hashed_password: str = hash_string(account.password)

    # Search Database for account with these details


def signup(account: Account):
    hashed_username: str = hash_string(account.username)
    hashed_password: str = hash_string(account.password)
    hashed_role: str = hash_string(account.role)
    hashed_restaurant: str = hash_string(account.restaurant)

    # Write these details to database
