import os
import tkinter as tk
from tkinter import font
from tkinter import ttk
from datetime import datetime
from threading import Thread


def read_file(relative_path: str) -> str:
    current_path = os.path.dirname(__file__)
    file_path = os.path.relpath(relative_path, current_path)

    with open(file_path, "r") as f:
        help_text: str = f.read()
    return help_text


def underline(label):
    f = font.Font(label, label.cget("font"))  # Create custom font
    f.configure(underline=True)  # Underline font
    label.configure(font=f)  # Apply font to the given label


def generate_report(table):
    header = ["Item Name", "Stock", "Expiry Date", "Weight", "Allergy", "Recycling"]
    with open("report.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in table.get_children():
            data_in_row = table.item(row)['values']
            writer.writerow(data_in_row)


def set_fridge_table(table) -> tuple:
    table['columns'] = [f'Col{x}' for x in range(1, 7)]
    headings: tuple = ("Item Name", "Stock", "Expiry Date", "Weight", "Allergy", "Recycling")
    return headings


def insert_fridge_table(function, table):
    for x, food_details in enumerate(function()):
        table.insert(parent='', index='end', iid=x,
                     text=x, values=[''.join(str(tuple_item)) for tuple_item in food_details[0:]])


def set_user_table(table) -> tuple:
    table['columns'] = [f'Col{x}' for x in range(1, 5)]
    headings: tuple = ("Username", "Name", "Role", "Restaurant")
    return headings


def insert_user_table(function, table):
    for x, user_details in enumerate(function()):
        table.insert(parent='', index='end', iid=x,
                     text=x, values=[''.join(str(tuple_item)) for tuple_item in user_details])


def create_table(function, fridge_table, root) -> ttk.Treeview:
    table = ttk.Treeview(root, height="5")
    style = ttk.Style(table)
    style.configure('TreeView', rowheight=30)
    style.theme_use('clam')

    headings = set_fridge_table(table) if fridge_table else set_user_table(table)
    table['show'] = 'headings'

    for column, heading in zip(table['columns'], headings):
        table.heading(column, text=heading)
        table.column(column, minwidth=0, width=100)
    table.place(relx=0.1, rely=0.15, relwidth=0.80, relheight=0.8)

    insert_fridge_table(function, table) if fridge_table else insert_user_table(function, table)
    if not fridge_table:
        table["displaycolumns"] = ("Col2", "Col3", "Col4")
    return table


def select_item(table, event=None):
    cur_item = table.focus()
    row_data: dict = table.item(cur_item)
    item_values: list = row_data['values']
    item_name = item_values[0]
    quantity = item_values[1]
    expiry = item_values[2]

    date = datetime.strptime(expiry, '%d %B %Y').date()
    formatted_expiry = date.strftime("%Y-%m-%d")

    Thread(target=remove_items, args=(item_name, formatted_expiry, quantity,), daemon=True).start()
    refresh_fridge_table(table)


def refresh_fridge_table(table):
    cur_item = table.focus()
    table.delete(cur_item)


def get_role(roles: list[bool]) -> str:
    valid: bool = True if sum(roles) == 1 else False
    if not valid:
        messagebox.showinfo(message="ERROR: One and only one role may be selected at once")
        return "Role Invalid"
    role_vals = ("Head Chef", "Chef")
    return role_vals[roles.index(True)]
