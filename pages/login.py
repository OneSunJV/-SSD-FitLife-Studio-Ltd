import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

import bcrypt
from PIL import Image, ImageTk
from tkinter.messagebox import showerror, showinfo
from layouts.system_layout import SystemLayout
import sqlite3

class LoginUI(ttk.Frame):
    def __init__(self, root):
        super().__init__(width=1280, height=720)
        self.grid_propagate(True)

        self.root = root

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)

        self.init_bg()
        self.init_login_frame()
        self.setup_images()
        self.setup_fonts()
        self.setup_labels()
        self.setup_entries()
        self.setup_button()

    def init_bg(self):
        self.login_ui_bg = Image.open(r'images\login_ui_bg.jpg')
        self.login_ui_bg = self.login_ui_bg.resize((1276,716))
        self.tkinter_login_ui_bg = ImageTk.PhotoImage(self.login_ui_bg)
        self.show_login_ui_bg = ttk.Label(self, image=self.tkinter_login_ui_bg)
        self.show_login_ui_bg.grid(column = 0, row = 0, columnspan = 3, rowspan = 3, sticky=tk.NSEW)

    def init_login_frame(self):
        # Frame
        self.login_box = ttk.Frame(self, width = 350, height = 630)
        self.login_box.grid(column = 1, row = 1)
        self.login_box.grid_propagate(True)

        self.login_box.columnconfigure(0, weight = 1)

        self.rowconfigure(0, weight = 1) # Logo
        self.rowconfigure(1, weight = 1) # Space for 'Welcome' text in image
        self.rowconfigure(2, weight = 1) # Space for 'enter log in details' text in image
        self.rowconfigure(3, weight = 1) # Username Text 
        self.rowconfigure(4, weight = 1) # Username Entry
        self.rowconfigure(5, weight = 1) # Password Text
        self.rowconfigure(6, weight = 1) # Password Entry
        self.rowconfigure(7, weight = 1) # Login

    def setup_images(self):
        self.login_box_bg = Image.open(r'images/login_box_bg.jpg')
        self.login_box_bg = self.login_box_bg.resize((350,630))
        self.tkinter_login_box_bg = ImageTk.PhotoImage(self.login_box_bg)
        self.show_login_box_bg = ttk.Label(self.login_box, image=self.tkinter_login_box_bg, background = "black")
        self.show_login_box_bg.grid(column = 0, row = 0, rowspan = 8)

        self.system_logo_label = Image.open(r'images/system_logo.png')
        self.system_logo_label = self.system_logo_label.resize((270,230))
        self.tkinter_system_logo_label = ImageTk.PhotoImage(self.system_logo_label)
        self.show_system_logo_label = ttk.Label(self.login_box, image=self.tkinter_system_logo_label, background = "black")
        self.show_system_logo_label.grid(column = 0, row = 0, pady = 25)

    def setup_fonts(self):
        self.welcome_label_font = tkFont.Font(family="Arial", size = 23, weight = "bold")
        self.login_label_font = tkFont.Font(family="Arial", size = 18, weight = "bold")
        self.other_element_fonts = tkFont.Font(family="Eras Bold ITC", size = 13, weight = "bold")

    def setup_labels(self):
        self.username_label = ttk.Label(self.login_box, text = 'Username:', font = self.other_element_fonts, foreground = "white", background = "#6B7278")
        self.username_label.grid(column = 0, row = 3, sticky = tk.W, padx = 10, pady = 3)
        self.password_label = ttk.Label(self.login_box, text = 'Password:', font = self.other_element_fonts, foreground = "white", background = "#686E73")
        self.password_label.grid(column = 0, row = 5, sticky = tk.W, padx = 10, pady = 3)

    def setup_entries(self):
        self.username_data = tk.StringVar()
        self.username_entry = ttk.Entry(self.login_box, textvariable = self.username_data)
        self.username_entry.grid(column = 0, row = 4, ipadx = 100, ipady = 5, pady = 3)

        self.password_data = tk.StringVar()
        self.password_entry = ttk.Entry(self.login_box, textvariable = self.password_data, show = "*")
        self.password_entry.grid(column = 0, row = 6, ipadx = 100, ipady = 5, pady = 3)

    def setup_button(self):
        self.login_button = ttk.Button(self.login_box, text = 'Login', command = lambda: validate_login_credentials(self.root, self.username_data.get(), self.password_data.get()))
        self.login_button.grid(column = 0, row = 7, ipadx = 50, ipady = 20, padx = 10, pady = 15)


def validate_login_credentials(root, username, password):
    connection = sqlite3.connect('SystemDatabase.db')
    cursor = connection.cursor()

    cursor.execute('SELECT PasswordHash, FirstName, LastName FROM Employees WHERE username = ?', (username,))

    row = cursor.fetchone()

    if row is None or not bcrypt.checkpw(password.encode('utf-8'), row[0]):
        showerror(title = "Login Failed!", message = "Fail! An account with these credentials does not exist in our system! If you believe this is a mistake, please contact your organisation's administrator(s) or our IT Service Desk.")
    else:
        display_name = f"{row[1]} {row[2]}"
        showinfo(title="Login Successful!",
                 message=f"Success! The login details you have entered are valid. Welcome {display_name} to SportsDev!")
        root.destroy()  # Destroy the login window
        SystemLayout()
