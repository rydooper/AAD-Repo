from hashlib import sha512
from datetime import datetime
from random import randint


class RoleError(Exception):
    print("Role could not be assigned")


class Deliveries:
    def __init__(self, address: str, date_time: datetime, name: str):
        self.address: str = address
        self.date_time: datetime = date_time
        self.driver: str = name
        self.door_code: int = randint(111_111, 999_999)


class Account:

    def __init__(self, username: str, password: str, role: str = "", restaurant: str = ""):
        self.username: str = hash_string(username)
        self.password: str = hash_string(password)
        self.role: str = hash_string(role)
        self.restaurant: str = hash_string(restaurant)


class Chef(Account):

    def __init__(self, username: str, password: str, role: str = "", restaurant: str = ""):
        Account.__init__(self, username, password, role, restaurant)
        self.front_door_access: bool = True


class HeadChef(Chef):

    def __init__(self, username: str, password: str, role: str = "", restaurant: str = ""):
        Chef.__init__(self, username, password, role, restaurant)
        self.staff_control: bool = True

    @staticmethod
    def manage_permissions(staff_account: Account):
        new_role = input("Enter role")  # Make GUI for this
        staff_account.role = new_role
        new_account = type_account(staff_account)
        # Update role on the database


class DeliveryDriver(Account):

    def __init__(self, username: str, password: str, role: str = "", restaurant: str = ""):
        Account.__init__(self, username, password, role, restaurant)
        self.back_door_access: bool = True
        self.deliveries: list[Deliveries] = []


def type_account(account: Account) -> Account:
    if account.role == "Head Chef":
        user: Account = HeadChef(account.username, account.password, account.role, account.restaurant)
    elif account.role == "Chef":
        user: Account = Chef(account.username, account.password, account.role, account.restaurant)
    elif account.role == "Delivery Driver":
        user: Account = Chef(account.username, account.password, account.role, account.restaurant)
    else:
        raise RoleError
    return user


def hash_string(string_to_hash: str) -> str:
    salt: str = "A?5J/b8-fe+w8b42,9B_J743dl"
    hashing_string = sha512((string_to_hash + salt).encode())
    return hashing_string.hexdigest()


def login(account: Account):
    # Search Database for account with these details
    pass


def signup(account: Account):
    # Write these details to database
    pass
