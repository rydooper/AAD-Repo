import tkinter as tk
from tkinter import font

bg_col: str = "dark grey"
fg_col: str = "white"
button_col: str = "grey"
root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.title("Monty Pythons")
root.config(bg=bg_col)


def underline(label):
    f = font.Font(label, label.cget("font"))  # Create custom font
    f.configure(underline=True)  # Underline font
    label.configure(font=f)  # Apply font to the given label


def login():
    pass


def signup():
    pass


def main_screen():
    welcoming = tk.Label(root, text="Welcome", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    welcoming.place(relx=0.45, rely=0.05)
    underline(welcoming)

    login_button = tk.Button(root, text="login", font=("arial", 10, "bold"),
                             bg=button_col, command=lambda: login())
    login_button.place(relx=0.25, rely=0.35, relwidth=0.2, relheight=0.1)

    signup_button = tk.Button(root, text="signup", font=("arial", 10, "bold"),
                              bg=button_col, command=lambda: signup())
    signup_button.place(relx=0.55, rely=0.35, relwidth=0.2, relheight=0.1)


if __name__ == "__main__":
    main_screen()
    root.mainloop()
