import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from PIL import Image, ImageTk # Allows me to display images.

class LoginUI(ttk.Frame):
    def __init__(self):
        super().__init__(width=1280, height=720)
        self.grid_propagate(False)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)

        self.init_bg()
        self.init_login_frame()

    def init_bg(self):
        self.big_logo = Image.open(r'images\login_image2.jpg')
        self.big_logo = self.big_logo.resize((1280,720))
        self.tkinter_system_logo = ImageTk.PhotoImage(self.big_logo)
        self.show_system_logo = ttk.Label(self, image=self.tkinter_system_logo)
        self.show_system_logo.grid(column = 0, row = 0, columnspan = 3, rowspan = 3, sticky=tk.NSEW)

    def init_login_frame(self):
        # Frame
        self.login_box = ttk.Frame(self, width = 350, height = 600, relief = 'raised')
        self.login_box.grid(column = 1, row = 1)
        self.login_box.grid_propagate(False)

        self.login_box.columnconfigure(0, weight = 1)

        self.rowconfigure(0, weight = 1) # Logo
        self.rowconfigure(1, weight = 1) # Welcome
        self.rowconfigure(2, weight = 1) # Enter your details
        self.rowconfigure(3, weight = 1) # Username Text 
        self.rowconfigure(4, weight = 1) # Username Entry
        self.rowconfigure(5, weight = 1) # Password Text
        self.rowconfigure(6, weight = 1) # Password Entry
        self.rowconfigure(7, weight = 1) # Login

        # Image
        self.small_logo = Image.open(r'images\Inventory_System_Logo.png')
        self.small_logo = self.small_logo.resize((200,200))
        self.tkinter_small_logo = ImageTk.PhotoImage(self.small_logo)
        self.show_small_logo = ttk.Label(self.login_box, image=self.tkinter_small_logo)
        self.show_small_logo.grid(column = 0, row = 0, sticky = tk.NS, pady = 15)

        # Labels
        welcome_label_font = tkFont.Font(family="Arial", size = 23)
        login_label_font = tkFont.Font(family="Arial", size = 18)
        other_element_fonts = tkFont.Font(family="Arial", size = 12)
        login_button_font = tkFont.Font(family="Arial", size = 15)

        self.welcome_label = ttk.Label(self.login_box, text = 'Welcome back!', font = welcome_label_font)
        self.welcome_label.grid(column = 0, row = 1, pady = 5)
        self.login_label = ttk.Label(self.login_box, text = 'Enter your details to log in!', font = login_label_font)
        self.login_label.grid(column = 0, row = 2, pady = 5)

        self.username_label = ttk.Label(self.login_box, text = 'Username:', font = other_element_fonts)
        self.username_label.grid(column = 0, row = 3, sticky = tk.W, padx = 10, pady = 5)
        self.password_label = ttk.Label(self.login_box, text = 'Password:', font = other_element_fonts)
        self.password_label.grid(column = 0, row = 5, sticky = tk.W, padx = 10, pady = 5)

        # Entries
        self.username_entry = ttk.Entry(self.login_box)
        self.username_entry.grid(column = 0, row = 4, ipadx = 100, ipady = 5, pady = 5)
        self.password_entry = ttk.Entry(self.login_box)
        self.password_entry.grid(column = 0, row = 6, ipadx = 100, ipady = 5, pady = 5)

        # Button
        self.login_button = ttk.Button(self.login_box, text = 'Login', )
        self.login_button.grid(column = 0, row = 7, ipadx = 50, ipady = 20, padx = 10, pady = 15)