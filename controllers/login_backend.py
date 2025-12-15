import tkinter as tk
from tkinter.messagebox import showerror, showinfo
from controllers.system_layout import SystemLayoutController

def validate_login_credentials(root, username, password):
    if username == "JohnDoe" and password == "12345":
        showinfo(title = "Login Successful!", message = ("Success! The login details you have entered are valid. Welcome ", username, " to SportsDev!"))
        SystemLayoutController.load_main_system(root)
    else:
        showerror(title = "Login Failed!", message = ("Fail! An account with these credentials does not exist in our system! If you believe this is a mistake, please contact your organisation's administator(s) or our IT Service Desk. "))