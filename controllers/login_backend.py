import tkinter as tk
from tkinter.messagebox import showerror, showinfo
from controllers.system_layout import SystemLayoutController

def validate_login_credentials(root, username, password):
    if username == "JohnDoe" and password == "12345":
        showinfo(title = "Login Successful!", message = ("Welcome", username, "!"))
        SystemLayoutController.load_main_system(root)
    else:
        showerror(title = "Login Failed!", message = ("Sorry! An account with these credentials does not exist."))