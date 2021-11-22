import tkinter as tk
from tkinter import font

bg_col: str = "dark grey"
fg_col: str = "white"

root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.title("Monty Pythons")
root.config(bg=bg_col)


def underline(label):
    f = font.Font(label, label.cget("font"))
    f.configure(underline=True)
    label.configure(font=f)


def main_screen():
    welcoming = tk.Label(root, text="Welcome", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    welcoming.place(relx=0.45, rely=0.05)
    underline(welcoming)


if __name__ == "__main__":
    main_screen()
    root.mainloop()
