from layouts import login_layout
import tkinter as tk

class LoginLayoutController:
    @staticmethod
    def load_login(root: tk.Tk):
        login_layout.LoginLayout(root)