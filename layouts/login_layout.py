import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from pages import login_ui

class LoginLayout:
    def __init__(self):
        root = tk.Tk()
        root.title('Login Page')
        root.geometry('1280x720')
        root.resizable(False, False)
        self.page_container = login_ui.LoginUI(root)
        self.page_container.grid(sticky = tk.NSEW)
        root.mainloop()
