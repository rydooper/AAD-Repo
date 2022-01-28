import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from tkinter import colorchooser
import account_handling
from fridge import Fridge
import fridge_db as db

bg_col: str = "grey"
fg_col: str = "white"
button_col: str = "dark grey"

root = tk.Tk()
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+-5+0")
root.title("Monty Pythons")
root.config(bg=bg_col)


def change_background():
    global bg_col
    bg_col = colorchooser.askcolor()[1]
    root.config(bg=bg_col)


def change_foreground():
    global fg_col
    fg_col = colorchooser.askcolor()[1]


def close_app(event=None):
    root.destroy()


root.bind('<Escape>', close_app)


def clear_root():
    for ele in root.winfo_children():
        ele.destroy()


def underline(label):
    f = font.Font(label, label.cget("font"))  # Create custom font
    f.configure(underline=True)  # Underline font
    label.configure(font=f)  # Apply font to the given label


def create_back_button() -> tk.Button:
    back_button = tk.Button(root, text="back", font=("arial", 10, "bold"), bg=button_col)
    back_button.place(relx=0.90, rely=0.05, relwidth=0.1, relheight=0.05, anchor=tk.CENTER)
    return back_button


def get_role(roles: list[bool]) -> str:
    valid: bool = True if sum(roles) == 1 else False
    if not valid:
        messagebox.showinfo(message="ERROR: One and only one role may be selected at once")
        return "Role Invalid"

    if roles[0]:
        return "Head Chef"
    elif roles[1]:
        return "Chef"
    else:
        return "Delivery Driver"


def create_account(username: str, password: str, name: str, restaurant: str, roles: list):
    role = get_role(roles)
    if role == "Role Invalid":
        return
    clear_root()
    account = account_handling.Account(username, password, name, role, restaurant)
    account_handling.signup(account)
    fridge_contents(account) if account.role == "Head Chef" else profile_screen(account)


def login_account(username: str, password: str):
    clear_root()
    account = account_handling.Account(username, password)
    user_details: tuple[str, str, str] = account_handling.login(account)
    account.name = user_details[0]
    account.role = user_details[1]
    account.restaurant = user_details[2]
    fridge_contents(account) if account.role == "Head Chef" else profile_screen(account)


def help_func(user_account: account_handling.Account):
    page_title = tk.Label(root, text="MontyFridges: Information Help Page",
                          font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    page_title.place(relx=0.4, rely=0.05, anchor=tk.CENTER)
    underline(page_title)

    back_button = create_back_button()
    back_button.place(relx=0.90, rely=0.05, relwidth=0.15, relheight=0.05, anchor=tk.CENTER)
    back_button.config(command=lambda: clear_root() or fridge_contents(user_account))

    page_information = tk.Label(root, text="MontyFridges: Don't blow up",
                                font=("arial", 12, "bold"), fg="black", bg="white")
    page_information.place(relx=0.5, rely=0.5, relwidth=0.90, relheight=0.80, anchor=tk.CENTER)


def change_name_func(user_account: account_handling.Account):
    messagebox.showinfo(message="Feature not yet implemented")
    profile_screen(user_account)


def profile_screen(user_account: account_handling.Account):
    page_title = tk.Label(root, text="MontyFridges: Profile", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    page_title.place(relx=0.4, rely=0.05, anchor=tk.CENTER)
    underline(page_title)

    change_name = tk.Button(root, text="Change username", font=("arial", 10, "bold"),
                            bg=button_col, command=lambda: clear_root() or change_name_func(user_account))
    change_name.place(relx=0.10, rely=0.05, relwidth=0.15, relheight=0.05, anchor=tk.CENTER)

    back_button = create_back_button()
    back_button.place(relx=0.70, rely=0.05, relwidth=0.15, relheight=0.05, anchor=tk.CENTER)
    back_button.config(command=lambda: clear_root() or fridge_contents(user_account))

    username = tk.Label(root, text="Username: " + user_account.username,
                        font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    username.place(relx=0.01, rely=0.2)

    role = tk.Label(root, text="Role: " + user_account.role,
                    font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    role.place(relx=0.01, rely=0.3)

    restaurant = tk.Label(root, text="Restaurant: " + user_account.restaurant,
                          font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    restaurant.place(relx=0.01, rely=0.4)


def get_safety_info(user: account_handling.Account):
    messagebox.showinfo(message="Feature not yet implemented")
    fridge_contents(user)


def fridge_contents(user: account_handling.Account):
    page_title = tk.Label(root, text="MontyFridges: Fridge Contents", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    page_title.place(relx=0.385, rely=0.05, anchor=tk.CENTER)
    underline(page_title)

    profile_button = tk.Button(root, text="Profile", font=("arial", 10, "bold"),
                               bg=button_col, command=lambda: clear_root() or profile_screen(user))
    profile_button.place(relx=0.175, rely=0.05, relwidth=0.15, relheight=0.05, anchor=tk.CENTER)

    home_button = tk.Button(root, text="Home", font=("arial", 10, "bold"),
                            bg=button_col, command=lambda: clear_root() or main_screen())
    home_button.place(relx=0.60, rely=0.05, relwidth=0.15, relheight=0.05, anchor=tk.CENTER)

    help_button = tk.Button(root, text="help", font=("arial", 10, "bold"),
                            bg=button_col, command=lambda: clear_root() or help_func(user))
    help_button.place(relx=0.75, rely=0.05, relwidth=0.10, relheight=0.05, anchor=tk.CENTER)

    safety_report = tk.Button(root, text="safety", font=("arial", 10, "bold"),
                              bg=button_col, command=lambda: clear_root() or get_safety_info(user))
    safety_report.place(relx=0.855, rely=0.05, relwidth=0.10, relheight=0.05, anchor=tk.CENTER)

    fridge_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
    fridge_entry.place(relx=0.10, rely=0.09, relwidth=0.805, relheight=0.05)

    table = ttk.Treeview(root, height="5")
    style = ttk.Style(table)
    style.configure('TreeView', rowheight=30)
    style.theme_use('clam')
    table['columns'] = [f'Col{x}' for x in range(1, 7)]
    headings = ("Item Name", "Stock", "Expiry Data", "Weight", "Allergy", "Recycling")
    table['show'] = 'headings'

    for column, heading in zip(table['columns'], headings):
        table.heading(column, text=heading)
        table.column(column, minwidth=0, width=100)
    table.place(relx=0.1, rely=0.15, relwidth=0.80, relheight=0.8)

    all_items: list[tuple] = db.display_fridge_contents()
    for list_item in all_items:
        table.insert(parent='', index='end', iid=x, text=x, values=[''.join(tuple_item) for tuple_item in list_item])

    scroll_bar_y = tk.Scrollbar(root, command=table.yview)
    scroll_bar_y.place(relx=0.9, rely=0.15, relheight=0.8)

    scroll_bar_x = tk.Scrollbar(root, command=table.xview, orient='horizontal')
    scroll_bar_x.place(relx=0.1, rely=0.95, relwidth=0.8)


def login():
    login_title = tk.Label(root, text="MontyFridges: login", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    login_title.place(relx=0.50, rely=0.05, anchor=tk.CENTER)
    underline(login_title)

    back_button = create_back_button()
    back_button.config(command=lambda: clear_root() or main_screen())

    username_label = tk.Label(root, text="Username:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    username_label.place(relx=0.20, rely=0.35)
    password_label = tk.Label(root, text="Password:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    password_label.place(relx=0.20, rely=0.45)

    username_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
    username_entry.place(relx=0.30, rely=0.35, relwidth=0.5, relheight=0.05)
    password_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13), show="*")
    password_entry.place(relx=0.30, rely=0.45, relwidth=0.5, relheight=0.05)

    login_submission = tk.Button(root, text="login", font=("arial", 10, "bold"),
                                 bg=button_col, command=lambda:
                                 login_account(username_entry.get(), password_entry.get()))
    login_submission.place(relx=0.20, rely=0.65, relwidth=0.28, relheight=0.1)

    help_button = tk.Button(root, text="help", font=("arial", 10, "bold"),
                            bg=button_col, command=lambda: clear_root() or help_func())
    help_button.place(relx=0.52, rely=0.65, relwidth=0.28, relheight=0.1)


def signup():
    signup_title = tk.Label(root, text="MontyFridges: signup", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    signup_title.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
    underline(signup_title)

    back_button = create_back_button()
    back_button.config(command=lambda: clear_root() or main_screen())

    username_label = tk.Label(root, text="Username:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    username_label.place(relx=0.05, rely=0.25)
    signup_username_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
    signup_username_entry.place(relx=0.20, rely=0.25, relwidth=0.2, relheight=0.05)

    password_label = tk.Label(root, text="Password:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    password_label.place(relx=0.05, rely=0.35)
    signup_password_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13), show="*")
    signup_password_entry.place(relx=0.20, rely=0.35, relwidth=0.2, relheight=0.05)

    name_label = tk.Label(root, text="Name:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    name_label.place(relx=0.05, rely=0.45)
    name_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
    name_entry.place(relx=0.20, rely=0.45, relwidth=0.2, relheight=0.05)

    role_label = tk.Label(root, text="Role:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    role_label.place(relx=0.05, rely=0.55)

    head_chef: bool = tk.BooleanVar()
    chef: bool = tk.BooleanVar()
    delivery_driver: bool = tk.BooleanVar()

    tk.Checkbutton(root, text="Head Chef", variable=head_chef).place(relx=0.20, rely=0.55)
    tk.Checkbutton(root, text="Chef", variable=chef).place(relx=0.28, rely=0.55)
    tk.Checkbutton(root, text="Delivery Driver", variable=delivery_driver).place(relx=0.33, rely=0.55, relwidth=0.07)

    restaurant_label = tk.Label(root, text="Restaurant:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    restaurant_label.place(relx=0.05, rely=0.65)
    restaurant_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
    restaurant_entry.place(relx=0.20, rely=0.65, relwidth=0.2, relheight=0.05)

    submit_details = tk.Button(root, text="signup", font=("arial", 10, "bold"),
                               bg=button_col, command=lambda:
                               create_account(signup_username_entry.get(), signup_password_entry.get(),
                                              name_entry.get(), restaurant_entry.get(),
                                              [head_chef.get(), chef.get(), delivery_driver.get()]))
    submit_details.place(relx=0.20, rely=0.75, relwidth=0.2, relheight=0.05)


def main_screen():
    welcoming = tk.Label(root, text="MontyFridges", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    welcoming.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
    underline(welcoming)

    login_button = tk.Button(root, text="login", font=("arial", 10, "bold"),
                             bg=button_col, command=lambda: clear_root() or login())
    login_button.place(relx=0.25, rely=0.35, relwidth=0.2, relheight=0.1)

    signup_button = tk.Button(root, text="signup", font=("arial", 10, "bold"),
                              bg=button_col, command=lambda: clear_root() or signup())
    signup_button.place(relx=0.55, rely=0.35, relwidth=0.2, relheight=0.1)

    colors = tk.Button(root, text="Background Color", font=("arial", 10, "bold"),
                       bg=button_col, command=change_background)
    colors.place(relx=0.75, rely=0.05, relwidth=0.1, relheight=0.05, anchor=tk.CENTER)

    colors = tk.Button(root, text="Foreground Color", font=("arial", 10, "bold"),
                       bg=button_col, command=change_foreground)
    colors.place(relx=0.90, rely=0.05, relwidth=0.1, relheight=0.05, anchor=tk.CENTER)


if __name__ == "__main__":
    main_screen()
    root.mainloop()
