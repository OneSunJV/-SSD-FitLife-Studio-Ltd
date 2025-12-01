import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo

class LoginLayout:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")

        self.root.rowconfigure(0, weight = 1)
        self.root.rowconfigure(1, weight = 5)
        self.root.rowconfigure(2, weight = 1)

        self.root.columnconfigure(0, weight = 1)

        self.init_header()
        self.init_page_container()
        self.init_header()
    
    # ---------------- Header ---------------- #
    def init_header(self):
        frame = tk.Frame(self.root, bg="red", width=1280, height=100)
        frame.grid(row=0, column=0)

    # ------------ Page Container ------------ #
    def init_page_container(self):
        self.page_container = tk.Frame(self.root, bg="blue", width=1280, height=540)
        self.page_container.grid(row=1, column=0)

    # ---------------- Footer ---------------- #
    def get_page_container(self):
        frame = tk.Frame(self.root, bg="red", width=1280, height=100)
        frame.grid(row=2, column=0)