import tkinter as tk
from tkinter.messagebox import showerror, showinfo

from layouts.system_layout import SystemLayout

def validate_login_credentials(root, username, password):
    if username == "1" and password == "1":
        showinfo(title = "Login Successful!", message = f"Success! The login details you have entered are valid. Welcome {username} to SportsDev!")
        root.destroy() # Destroy the login window
        SystemLayout()
    else:
        showerror(title = "Login Failed!", message = "Fail! An account with these credentials does not exist in our system! If you believe this is a mistake, please contact your organisation's administrator(s) or our IT Service Desk.")