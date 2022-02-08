from datetime import datetime
from hashlib import sha512
from random import randint
from custom_exceptions import RoleError
from fridge_db import update_user


class Deliveries:

    __slots__ = ["address", "date_time", "driver", "door_code"]

    def __init__(self, address: str, date_time: datetime, name: str):
        self.address: str = address
        self.date_time: datetime = date_time
        self.driver: str = name
        self.door_code: int = randint(100_000, 999_999)


class Account:

    __slots__ = ["username", "password", "name", "role", "restaurant"]

    def __init__(self, username: str, password: str, name: str = "", role: str = "", restaurant: str = ""):
        self.username: str = self.hash_string(username)
        self.password: str = self.hash_string(password)
        self.name: str = name
        self.role: str = role
        self.restaurant: str = restaurant

    @staticmethod
    def hash_string(string_to_hash: str) -> str:
        salt: str = "A?5J/b8-fe+w8b42,9B_J743dl"
        hashing_string = sha512((string_to_hash + salt).encode())
        return hashing_string.hexdigest()


class Chef(Account):

    __slots__ = "front_door_access"

    def __init__(self, username: str, password: str, name: str = "", role: str = "", restaurant: str = ""):
        Account.__init__(self, username, password, name, role, restaurant)
        self.front_door_access: bool = True


class HeadChef(Chef):

    __slots__ = "staff_control"

    def __init__(self, username: str, password: str, name: str = "", role: str = "", restaurant: str = ""):
        Chef.__init__(self, username, password, name, role, restaurant)
        self.staff_control: bool = True

    @staticmethod
    def manage_permissions(username, new_role):
        update_user(username, new_role)


class DeliveryDriver(Account):

    __slots__ = ["back_door_access", "deliveries"]

    def __init__(self, username: str, password: str, name: str = "", role: str = "", restaurant: str = ""):
        Account.__init__(self, username, password, name, role, restaurant)
        self.back_door_access: bool = True
        self.deliveries: list[Deliveries] = []


def type_account(username: str, password: str, account: Account) -> Account:
    print(account.role)
    if account.role == "Head Chef":
        user: Account = HeadChef(username, password, account.name, account.role, account.restaurant)
    elif account.role == "Chef":
        user: Account = Chef(username, password, account.name, account.role, account.restaurant)
    elif account.role == "Delivery Driver":
        user: Account = DeliveryDriver(username, password, account.name,
                                       account.role, account.restaurant)
    else:
        raise RoleError

    return user
