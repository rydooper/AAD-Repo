import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
import account_handling

bg_col: str = "grey"
fg_col: str = "white"
button_col: str = "dark grey"

root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.title("Monty Pythons")
root.config(bg=bg_col)


def clear_root():
    for ele in root.winfo_children():
        ele.destroy()


def underline(label):
    f = font.Font(label, label.cget("font"))  # Create custom font
    f.configure(underline=True)  # Underline font
    label.configure(font=f)  # Apply font to the given label


def create_back_button() -> tk.Button:
    back_button = tk.Button(root, text="back", font=("arial", 10, "bold"), bg=button_col)
    back_button.place(relx=0.75, rely=0.05, relwidth=0.2, relheight=0.1)
    return back_button


def create_account(username: str, password: str, role: str, restaurant: str):
    clear_root()
    account = account_handling.Account(username, password, role, restaurant)
    account_handling.signup(account)
    if account.role == "Head Chef":
        fridge_contents(account)
    else:
        profile_screen(account)


def login_account(username: str, password: str):
    clear_root()
    account = account_handling.Account(username, password)
    account_handling.login(account)
    if account.role == "Head Chef":
        fridge_contents(account)
    else:
        profile_screen(account)


def help_func():
    pass


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


def fridge_contents(user: account_handling.Account):
    page_title = tk.Label(root, text="MontyFridges: Fridge Contents", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    page_title.place(relx=0.4, rely=0.05, anchor=tk.CENTER)
    underline(page_title)

    profile_button = tk.Button(root, text="Profile", font=("arial", 10, "bold"),
                               bg=button_col, command=lambda: clear_root() or profile_screen(user))
    profile_button.place(relx=0.10, rely=0.05, relwidth=0.15, relheight=0.05, anchor=tk.CENTER)

    home_button = tk.Button(root, text="Home", font=("arial", 10, "bold"),
                            bg=button_col, command=lambda: clear_root() or main_screen())
    home_button.place(relx=0.70, rely=0.05, relwidth=0.15, relheight=0.05, anchor=tk.CENTER)

    help_button = tk.Button(root, text="help", font=("arial", 10, "bold"),
                            bg=button_col, command=lambda: clear_root() or help_func())
    help_button.place(relx=0.87, rely=0.05, relwidth=0.15, relheight=0.05, anchor=tk.CENTER)

    table = ttk.Treeview(root, height="5")
    style = ttk.Style(table)
    style.configure('TreeView', rowheight=30)
    style.theme_use('clam')
    table['columns'] = ("Col1", "Col2", "Col3", "Col4", "Col5", "Col6", "Col7")
    headings = ("ItemID", "Item Name", "Stock", "Expiry Data", "Weight", "Allergy", "Recycling")

    data: list[list[str]] = [[test_data for test_data in headings], ["D", "E", "F"]]

    for column, heading in zip(table['columns'], headings):
        table.heading(column, text=heading)
        table.column(column, minwidth=0, width=100)
    table.place(relx=0.1, rely=0.15, relwidth=0.80, relheight=0.8)

    for x in range(1, 1000):
        table.insert(parent='', index='end', iid=x, text=x, values=data[0])

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
    password_label = tk.Label(root, text="Password:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    password_label.place(relx=0.05, rely=0.35)

    role_label = tk.Label(root, text="Role:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    role_label.place(relx=0.05, rely=0.45)
    restaurant_label = tk.Label(root, text="Restaurant:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    restaurant_label.place(relx=0.05, rely=0.55)

    signup_username_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
    signup_username_entry.place(relx=0.20, rely=0.25, relwidth=0.2, relheight=0.05)
    signup_password_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13), show="*")
    signup_password_entry.place(relx=0.20, rely=0.35, relwidth=0.2, relheight=0.05)
    role_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
    role_entry.place(relx=0.20, rely=0.45, relwidth=0.2, relheight=0.05)
    restaurant_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
    restaurant_entry.place(relx=0.20, rely=0.55, relwidth=0.2, relheight=0.05)

    submit_details = tk.Button(root, text="signup", font=("arial", 10, "bold"),
                               bg=button_col, command=lambda:
                               create_account(signup_username_entry.get(), signup_password_entry.get(),
                                              role_entry.get(), restaurant_entry.get()))
    submit_details.place(relx=0.20, rely=0.65, relwidth=0.2, relheight=0.05)


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


if __name__ == "__main__":
    main_screen()
    root.mainloop()
