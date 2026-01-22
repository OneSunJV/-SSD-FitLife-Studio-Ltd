import tkinter as tk
from pages import login

class LoginLayout:
    def __init__(self):
        root = tk.Tk()
        root.title('Login Page')
        root.geometry('1280x720')
        root.resizable(False, False)
        self.page_container = login.LoginUI(root)
        self.page_container.grid(sticky = tk.NSEW)
        root.mainloop()
