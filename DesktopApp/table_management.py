from tkinter import ttk
from datetime import datetime
from threading import Thread


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
