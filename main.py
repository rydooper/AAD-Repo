import tkinter as tk
from tkinter import font

bg_col: str = "dark grey"
fg_col: str = "white"
button_col: str = "grey"

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


def create_account():
    pass


def login():
    login_title = tk.Label(root, text="login", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    login_title.place(relx=0.45, rely=0.05)
    underline(login_title)

    back_button = create_back_button()
    back_button.config(command=lambda: clear_root() or main_screen())


def signup():
    signup_title = tk.Label(root, text="signup", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    signup_title.place(relx=0.45, rely=0.05)
    underline(signup_title)

    back_button = create_back_button()
    back_button.config(command=lambda: clear_root() or main_screen())

    username_label = tk.Label(root, text="Username:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    username_label.place(relx=0.05, rely=0.25)
    password_label = tk.Label(root, text="Password:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    password_label.place(relx=0.05, rely=0.35)
    role_label = tk.Label(root, text="Username:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    role_label.place(relx=0.05, rely=0.45)
    password_label = tk.Label(root, text="Password:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    password_label.place(relx=0.05, rely=0.55)

    signup_username_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
    signup_username_entry.place(relx=0.20, rely=0.25, relwidth=0.2, relheight=0.05)
    signup_password_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13), show="*")
    signup_password_entry.place(relx=0.20, rely=0.35, relwidth=0.2, relheight=0.05)
    role_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
    role_entry.place(relx=0.20, rely=0.45, relwidth=0.2, relheight=0.05)
    restaurant_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13), show="*")
    restaurant_entry.place(relx=0.20, rely=0.55, relwidth=0.2, relheight=0.05)

    submit_details = tk.Button(root, text="signup", font=("arial", 10, "bold"),
                               bg=button_col, command=lambda: clear_root() or create_account())
    submit_details.place(relx=0.20, rely=0.65, relwidth=0.2, relheight=0.05)


def main_screen():
    welcoming = tk.Label(root, text="Welcome", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    welcoming.place(relx=0.45, rely=0.05)
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
