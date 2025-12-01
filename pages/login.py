import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo

class Login(ttk.Frame):
    def __init__(self, root):
        super().__init__(height=820, width=1500, borderwidth=1, relief='sunken')

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        self.rowconfigure(0, weight = 3)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)
        self.rowconfigure(6, weight = 1)
        self.rowconfigure(7, weight = 3)

    def init_images(self):
        pass

    def init_labels(self):
        self.login_label = ttk.Label(self, text = 'Log In', background='#FFFFFF')
        self.login_label.grid()
        self.username_label = ttk.Label()
        self.username_label.grid()
        self.password_label = ttk.Label()
        self.password_label.grid()

    def init_entries():
        pass
            