import tkinter as tk
from tkinter import colorchooser
import account_handling
from fridge import Fridge
import fridge_db as db
from threading import Thread
import utility
import table_management

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
    clear_root()
    main_screen()


def close_app(event=None):
    root.destroy()


root.bind('<Escape>', close_app)


def clear_root():
    for ele in root.winfo_children():
        ele.destroy()


def create_back_button() -> tk.Button:
    back_button = tk.Button(root, text="back", font=("arial", 10, "bold"), bg=button_col)
    back_button.place(relx=0.90, rely=0.05, relwidth=0.1, relheight=0.05, anchor=tk.CENTER)
    return back_button


def create_account(username: str, password: str, name: str, restaurant: str, roles: list[bool]):
    role: str = utility.get_role(roles)
    if role == "Role Invalid":
        return

    general_account = account_handling.Account(username, password, name, role, restaurant)
    account = account_handling.type_account(username, password, general_account)
    submission = db.signup(account.username, account.password, account.name, account.role, account.restaurant)
    if submission != "Unsuccessful query.":
        clear_root()
        specific_fridge_info(account, db.display_item_alerts) if account.role == "Head Chef" else profile_screen(account)


def login_account(username: str, password: str):
    clear_root()
    general_account = account_handling.Account(username, password)
    user_details = db.login(general_account.username, general_account.password)
    if user_details == "Incorrect login details provided.":
        clear_root()
        main_screen()
    else:
        general_account.name = user_details[0][0]
        general_account.role = user_details[0][1]
        general_account.restaurant = user_details[0][2]
        account = account_handling.type_account(username, password, general_account)
        specific_fridge_info(account, db.display_item_alerts) if account.role == "Head Chef" else profile_screen(account)


def help_func(user_account: account_handling.Account, pageType: str):
    help_text: str = utility.read_file(pageType)

    page_title = tk.Label(root, text="MontyFridges: Information Help Page",
                          font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    page_title.place(relx=0.4, rely=0.05, anchor=tk.CENTER)
    utility.underline(page_title)

    back_button = create_back_button()
    back_button.place(relx=0.90, rely=0.05, relwidth=0.15, relheight=0.05, anchor=tk.CENTER)
    back_button.config(command=lambda: clear_root() or fridge_contents(user_account))

    page_information = tk.Label(root, text=help_text,
                                font=("arial", 12, "bold"), fg="black", bg="white")
    page_information.place(relx=0.5, rely=0.5, relwidth=0.90, relheight=0.80, anchor=tk.CENTER)


def help_func_signup(pageType: str):
    help_text: str = utility.read_file(pageType)

    page_title = tk.Label(root, text="MontyFridges: Information Help Page",
                          font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    page_title.place(relx=0.4, rely=0.05, anchor=tk.CENTER)
    utility.underline(page_title)

    back_button = create_back_button()
    back_button.place(relx=0.90, rely=0.05, relwidth=0.15, relheight=0.05, anchor=tk.CENTER)
    back_button.config(command=lambda: clear_root() or signup_screen())

    page_information = tk.Label(root, text=help_text,
                                font=("arial", 12, "bold"), fg="black", bg="white")
    page_information.place(relx=0.5, rely=0.5, relwidth=0.90, relheight=0.80, anchor=tk.CENTER)


def profile_screen(user_account: account_handling.Account):
    page_title = tk.Label(root, text="MontyFridges: Profile", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    page_title.place(relx=0.4, rely=0.05, anchor=tk.CENTER)
    utility.underline(page_title)

    back_button = create_back_button()
    back_button.place(relx=0.65, rely=0.05, relwidth=0.08, relheight=0.05, anchor=tk.CENTER)
    back_button.config(command=lambda: clear_root() or fridge_contents(user_account))
    help_button = tk.Button(root, text="help", font=("arial", 10, "bold"),
                            bg=button_col, command=lambda: clear_root()
                            or help_func(user_account, "textFilesForSupport\\profileSupport.txt"))
    help_button.place(relx=0.75, rely=0.05, relwidth=0.08, relheight=0.05, anchor=tk.CENTER)

    username = tk.Label(root, text="Name: " + user_account.name,
                        font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    username.place(relx=0.01, rely=0.2)

    role = tk.Label(root, text="Role: " + user_account.role,
                    font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    role.place(relx=0.01, rely=0.3)

    restaurant = tk.Label(root, text="Restaurant: " + user_account.restaurant,
                          font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    restaurant.place(relx=0.01, rely=0.4)


def specific_fridge_info(user: account_handling.Account, function_to_display):
    clear_root()
    page_title = tk.Label(root, text="MontyFridges: Safety report",
                          font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    page_title.place(relx=0.385, rely=0.05, anchor=tk.CENTER)
    utility.underline(page_title)

    back_button = create_back_button()
    back_button.config(command=lambda: clear_root() or fridge_contents(user))
    back_button.place(relx=0.85, rely=0.05, relwidth=0.10, relheight=0.05, anchor=tk.CENTER)

    return table_management.create_table(function_to_display, True, root)


def get_safety_info(user: account_handling.Account):
    table = specific_fridge_info(user, db.generate_health_report)
    utility.generate_report_button = tk.Button(root, text="Generate report", font=("arial", 10, "bold"),
                                               bg=button_col, command=lambda: utility.generate_report(table))
    utility.generate_report_button.place(relx=0.85, rely=0.115, relwidth=0.10, relheight=0.05, anchor=tk.CENTER)


def update_role(user: account_handling.Account, username: str, roles: list[str, str, str]):
    new_role: str = utility.get_role(roles)
    user.manage_permissions(username, new_role)
    clear_root()
    change_staff_role(user)


def update_role_ui(user: account_handling.Account, table, event=None):
    cur_item = table.focus()
    row_data: dict = table.item(cur_item)
    item_values: list = row_data['values']
    username: str = item_values[0]
    old_role: str = item_values[1]

    pop_up = tk.Toplevel(root, bg=bg_col)
    pop_up.title = "Change Role"
    pop_up.geometry("600x400")

    page_title = tk.Label(pop_up, text="MontyFridges: Change Role", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    page_title.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
    utility.underline(page_title)

    old_role_label = tk.Label(pop_up, text=f"Old Role: {old_role}", font=("arial", 12, "bold"), fg=fg_col, bg=bg_col)
    old_role_label.place(relx=0.1, rely=0.2)

    new_role_label = tk.Label(pop_up, text="New Role:", font=("arial", 12, "bold"), fg=fg_col, bg=bg_col)
    new_role_label.place(relx=0.1, rely=0.3)

    head_chef: bool = tk.BooleanVar()
    chef: bool = tk.BooleanVar()

    tk.Checkbutton(pop_up, text="Head Chef", variable=head_chef).place(relx=0.10, rely=0.45)
    tk.Checkbutton(pop_up, text="Chef", variable=chef).place(relx=0.10, rely=0.55)

    change_role_button = tk.Button(pop_up, text="Commit Change", font=("arial", 10, "bold"),
                                   bg=button_col, command=lambda:
                                   update_role(user, username, [head_chef.get(), chef.get()]))

    change_role_button.place(relx=0.1, rely=0.65, relwidth=0.2, relheight=0.05)

    delete_user_button = tk.Button(pop_up, text="Delete", font=("arial", 10, "bold"),
                                   bg=button_col,
                                   command=lambda: Thread(target=db.remove_user, args=(username,), daemon=True).start()
                                   or table.delete(cur_item))
    delete_user_button.place(relx=0.1, rely=0.75, relwidth=0.2, relheight=0.05)


def change_staff_role(user: account_handling.Account):
    page_title = tk.Label(root, text="MontyFridges: Staff Management", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    page_title.place(relx=0.385, rely=0.05, anchor=tk.CENTER)
    utility.underline(page_title)

    profile_button = tk.Button(root, text="Profile", font=("arial", 10, "bold"),
                               bg=button_col, command=lambda: clear_root() or profile_screen(user))
    profile_button.place(relx=0.175, rely=0.05, relwidth=0.15, relheight=0.05, anchor=tk.CENTER)

    back_button = create_back_button()
    back_button.place(relx=0.90, rely=0.05, relwidth=0.15, relheight=0.05, anchor=tk.CENTER)
    back_button.config(command=lambda: clear_root() or fridge_contents(user))

    help_button = tk.Button(root, text="help", font=("arial", 10, "bold"),
                            bg=button_col, command=lambda: clear_root()
                            or help_func(user, "textFilesForSupport\\staffManagementSupport.txt"))
    help_button.place(relx=0.75, rely=0.05, relwidth=0.10, relheight=0.05, anchor=tk.CENTER)

    table = table_management.create_table(db.display_users, False, root)
    table.bind('<ButtonRelease-1>', lambda event: update_role_ui(user, table, event))


def fridge_contents(user: account_handling.Account):
    page_title = tk.Label(root, text="MontyFridges: Fridge Contents", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    page_title.place(relx=0.385, rely=0.05, anchor=tk.CENTER)
    utility.underline(page_title)

    profile_button = tk.Button(root, text="Profile", font=("arial", 10, "bold"),
                               bg=button_col, command=lambda: clear_root() or profile_screen(user))
    profile_button.place(relx=0.136, rely=0.05, relwidth=0.0725, relheight=0.05, anchor=tk.CENTER)

    sign_out_button = tk.Button(root, text="Sign out", font=("arial", 10, "bold"),
                                bg=button_col, command=lambda: clear_root() or main_screen())
    sign_out_button.place(relx=0.65, rely=0.05, relwidth=0.08, relheight=0.05, anchor=tk.CENTER)

    help_button = tk.Button(root, text="help", font=("arial", 10, "bold"),
                            bg=button_col, command=lambda: clear_root()
                            or help_func(user, "textFilesForSupport\\fridgeContentsSupport.txt"))
    help_button.place(relx=0.75, rely=0.05, relwidth=0.08, relheight=0.05, anchor=tk.CENTER)

    search_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
    search_entry.place(relx=0.10, rely=0.09, relwidth=0.505, relheight=0.05)

    search_button = tk.Button(root, text="Search", font=("arial", 10, "bold"),
                              bg=button_col, command=lambda: table.destroy()
                              or table_management.create_table(lambda: db.search_fridge_contents(search_entry.get())
                                                               , True, root))
    search_button.place(relx=0.65, rely=0.115, relwidth=0.08, relheight=0.05, anchor=tk.CENTER)

    show_all_contents = tk.Button(root, text="Show all", font=("arial", 10, "bold"),
                                  bg=button_col, command=lambda: table.destroy()
                                  or table_management.create_table(db.display_fridge_contents, True, root))
    show_all_contents.place(relx=0.75, rely=0.115, relwidth=0.08, relheight=0.05, anchor=tk.CENTER)

    table = table_management.create_table(db.display_fridge_contents, True, root)
    table.bind('<Delete>', lambda event: table_management.select_item(table, event))

    scroll_bar_y = tk.Scrollbar(root, command=table.yview)
    scroll_bar_y.place(relx=0.9, rely=0.15, relheight=0.8)

    scroll_bar_x = tk.Scrollbar(root, command=table.xview, orient='horizontal')
    scroll_bar_x.place(relx=0.1, rely=0.95, relwidth=0.8)

    if user.role == "Head Chef":
        item_alert_button = tk.Button(root, text="Item alert", font=("arial", 10, "bold"),
                                      bg=button_col, command=lambda:
                                      specific_fridge_info(user, db.display_item_alerts))
        item_alert_button.place(relx=0.23, rely=0.05, relwidth=0.0725, relheight=0.05, anchor=tk.CENTER)

        staff_management_button = tk.Button(root, text="Staff management", font=("arial", 10, "bold"),
                                            bg=button_col, command=lambda: clear_root() or change_staff_role(user))
        staff_management_button.place(relx=0.855, rely=0.115, relwidth=0.10, relheight=0.05, anchor=tk.CENTER)

        safety_report = tk.Button(root, text="safety", font=("arial", 10, "bold"),
                                  bg=button_col, command=lambda: clear_root() or get_safety_info(user))
        safety_report.place(relx=0.855, rely=0.05, relwidth=0.10, relheight=0.05, anchor=tk.CENTER)


def login_screen():
    login_title = tk.Label(root, text="MontyFridges: login", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    login_title.place(relx=0.50, rely=0.05, anchor=tk.CENTER)
    utility.underline(login_title)

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


def signup_screen():
    signup_title = tk.Label(root, text="MontyFridges: signup", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    signup_title.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
    utility.underline(signup_title)

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

    tk.Checkbutton(root, text="Head Chef", font=("arial", 13), variable=head_chef).place(relx=0.20, rely=0.55,
                                                                                         relwidth=0.08)
    tk.Checkbutton(root, text="Chef", font=("arial", 13), variable=chef).place(relx=0.32, rely=0.55, relwidth=0.08)

    restaurant_label = tk.Label(root, text="Restaurant:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    restaurant_label.place(relx=0.05, rely=0.65)
    restaurant_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
    restaurant_entry.place(relx=0.20, rely=0.65, relwidth=0.2, relheight=0.05)

    help_button = tk.Button(root, text="help", font=("arial", 10, "bold"),
                            bg=button_col, command=lambda: clear_root()
                            or help_func_signup(pageType="textFilesForSupport\\signupSupport.txt"))
    help_button.place(relx=0.75, rely=0.05, relwidth=0.08, relheight=0.05, anchor=tk.CENTER)

    submit_details = tk.Button(root, text="signup", font=("arial", 10, "bold"),
                               bg=button_col, command=lambda:
                               create_account(signup_username_entry.get(), signup_password_entry.get(),
                               name_entry.get(), restaurant_entry.get(),
                               [head_chef.get(), chef.get()]))
    submit_details.place(relx=0.20, rely=0.75, relwidth=0.2, relheight=0.05)


def main_screen():
    welcoming = tk.Label(root, text="MontyFridges", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    welcoming.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
    utility.underline(welcoming)

    login_button = tk.Button(root, text="login", font=("arial", 10, "bold"),
                             bg=button_col, command=lambda: clear_root() or login_screen())
    login_button.place(relx=0.25, rely=0.35, relwidth=0.2, relheight=0.1)

    signup_button = tk.Button(root, text="signup", font=("arial", 10, "bold"),
                              bg=button_col, command=lambda: clear_root() or signup_screen())
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
