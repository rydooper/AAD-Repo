from fridge_db import add_items
import random


def add_fridge_content():
    item_names = ["carrots", "milk", "cake", "bread"]
    add_items(random.choice(item_names), f"2022-03-{random.randint(1,31)}", random.randint(1, 150),
              random.randint(1, 150), "allergy_info", "recycling_info")


if __name__ == "__main__":
    add_fridge_content()
