from hashlib import sha512


class AccountHandling:

    __slots__ = ["hash_string"]

    def __init__(self, username: str, password: str, role: str = "", restaurant: str = ""):
        self.username: str = self.hash_string(username)
        self.password: str = self.hash_string(password)
        self.role: str = self.hash_string(role)
        self.restaurant: str = self.hash_string(restaurant)

    @staticmethod
    def hash_string(string_to_hash: str) -> str:
        salt = "A?5J/b8-fe+w8b42,9B_J743dl"
        hashing_string = sha512((string_to_hash + salt).encode())
        return hashing_string.hexdigest()


def login(account: AccountHandling):
    # Search Database for account with these details
    pass


def signup(account: AccountHandling):
    # Write these details to database
    pass
