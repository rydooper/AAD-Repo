from hashlib import sha512


def hash_string(string_to_hash: str) -> str:
    salt = "A?5J/b8-fe+w8b42,9B_J743dl"
    hashing_string = sha512((string_to_hash + salt).encode())
    return hashing_string.hexdigest()


def login(username: str, password: str):
    hashed_username: str = hash_string(username)
    hashed_password: str = hash_string(password)


def signup(username: str, password: str, role: str, restaurant: str):
    hashed_username: str = hash_string(username)
    hashed_password: str = hash_string(password)
    hashed_role: str = hash_string(role)
    hashed_restaurant: str = hash_string(restaurant)
