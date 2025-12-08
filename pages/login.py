import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from PIL import Image, ImageTk # Allows me to display images.

class LoginUI(ttk.Frame):
    def __init__(self):
        super().__init__(width=1280, height=720)
        self.grid_propagate(True)

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
        self.login_box = ttk.Frame(self, width = 350, height = 600, relief = 'solid')
        self.login_box.grid(column = 1, row = 1)
        self.login_box.grid_propagate(True)

        self.login_box.columnconfigure(0, weight = 1)

        self.rowconfigure(0, weight = 1) # Logo
        self.rowconfigure(1, weight = 1) # Welcome
        self.rowconfigure(2, weight = 1) # Enter your details
        self.rowconfigure(3, weight = 1) # Username Text 
        self.rowconfigure(4, weight = 1) # Username Entry
        self.rowconfigure(5, weight = 1) # Password Text
        self.rowconfigure(6, weight = 1) # Password Entry
        self.rowconfigure(7, weight = 1) # Login

    def setup_images(self):
        self.login_box_bg = Image.open(r'images/login_box_bg.jpg')
        self.login_box_bg = self.login_box_bg.resize((350,600))
        self.tkinter_login_box_bg = ImageTk.PhotoImage(self.login_box_bg)
        self.show_login_box_bg = ttk.Label(self.login_box, image=self.tkinter_login_box_bg)
        self.show_login_box_bg.grid(column = 0, row = 0, rowspan = 8)

        self.system_logo_label = Image.open(r'images/system_logo.png')
        self.system_logo_label = self.system_logo_label.resize((300,150))
        self.tkinter_system_logo_label = ImageTk.PhotoImage(self.system_logo_label)
        self.show_system_logo_label = ttk.Label(self.login_box, image=self.tkinter_system_logo_label)
        self.show_system_logo_label.grid(column = 0, row = 0, pady = 15)

    def setup_fonts(self):
        self.welcome_label_font = tkFont.Font(family="Arial", size = 23)
        self.login_label_font = tkFont.Font(family="Arial", size = 18)
        self.other_element_fonts = tkFont.Font(family="Arial", size = 12)

    def setup_labels(self):
        self.welcome_label = ttk.Label(self.login_box, text = 'Welcome back!', font = self.welcome_label_font)
        self.welcome_label.grid(column = 0, row = 1, pady = 5)
        self.login_label = ttk.Label(self.login_box, text = 'Enter your details to log in!', font = self.login_label_font)
        self.login_label.grid(column = 0, row = 2, pady = 5)

        self.username_label = ttk.Label(self.login_box, text = 'Username:', font = self.other_element_fonts)
        self.username_label.grid(column = 0, row = 3, sticky = tk.W, padx = 10, pady = 5)
        self.password_label = ttk.Label(self.login_box, text = 'Password:', font = self.other_element_fonts)
        self.password_label.grid(column = 0, row = 5, sticky = tk.W, padx = 10, pady = 5)

    def setup_entries(self):
        self.username_entry = ttk.Entry(self.login_box)
        self.username_entry.grid(column = 0, row = 4, ipadx = 100, ipady = 5, pady = 5)
        self.password_entry = ttk.Entry(self.login_box)
        self.password_entry.grid(column = 0, row = 6, ipadx = 100, ipady = 5, pady = 5)

    def setup_button(self):
        self.login_button = ttk.Button(self.login_box, text = 'Login')
        self.login_button.grid(column = 0, row = 7, ipadx = 50, ipady = 20, padx = 10, pady = 15)