import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from pages import login_ui

class LoginLayout:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.title("Login Page")
        self.page_container = login_ui.LoginUI(self.root)
        self.page_container.grid(sticky = tk.NSEW)