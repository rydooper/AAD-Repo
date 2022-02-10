import os
from tkinter import font
from tkinter import messagebox
import csv


def read_file(relative_path: str) -> str:
    current_path = os.path.dirname(__file__)
    file_path = os.path.relpath(relative_path, current_path)

    with open(file_path, "r") as f:
        help_text: str = f.read()
    return help_text


def generate_report(table):
    header = ["Item Name", "Stock", "Expiry Date", "Weight", "Allergy", "Recycling"]
    with open("report.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in table.get_children():
            data_in_row = table.item(row)['values']
            writer.writerow(data_in_row)


def underline(label):
    f = font.Font(label, label.cget("font"))  # Create custom font
    f.configure(underline=True)  # Underline font
    label.configure(font=f)  # Apply font to the given label


def get_role(roles: list[bool]) -> str:
    valid: bool = True if sum(roles) == 1 else False
    if not valid:
        messagebox.showinfo(message="ERROR: One and only one role may be selected at once")
        return "Role Invalid"
    role_vals = ("Head Chef", "Chef")
    return role_vals[roles.index(True)]
