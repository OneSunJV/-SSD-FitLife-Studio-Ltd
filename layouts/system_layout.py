import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from config.pages import PAGES
from page_controller import PageController


class SystemLayout:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FitLife Studios - WBMS")

        self.page_container = None

        #(Columns) Sidebar, Main Area
        self.root.columnconfigure(0, weight = 0)
        self.root.columnconfigure(1, weight = 1)

        #(Rows) Header, Page Body
        self.root.rowconfigure(0, weight = 0)
        self.root.rowconfigure(1, weight = 1)

        #Initialise layout sections
        self.init_sidebar()
        self.init_header()
        self.init_page_container()

        self.page_controller = PageController(self.page_container)
        self.create_sidebar_buttons(PAGES)

        for page in PAGES:
            self.page_controller.register_page(page["className"])

        for idx, page in enumerate(PAGES):
            if page["default"]:
                self.page_controller.display_page(idx)
                break

    
  # ---------------- Sidebar ---------------- #
    def init_sidebar(self):
        frame = ttk.Frame(self.root, width=280, height=720)
        frame.grid(row=0, column=0, rowspan=2, sticky=tk.NSEW)
        #frame.grid_propagate(False)  # keep the width/height
        frame.columnconfigure(0, weight=1)

        # FitLife Logo
        system_logo_label = Image.open(r'images/system_logo.png')
        system_logo_label = system_logo_label.resize((270,230))
        self.tkinter_system_logo_label = ImageTk.PhotoImage(system_logo_label)
        show_system_logo_label = ttk.Label(frame, image=self.tkinter_system_logo_label, background = "black")
        show_system_logo_label.grid(column=0, row=0, padx=5, pady=5)

        # store reference so we can add buttons later
        self.sidebar_frame = frame

     # ---------------- Sidebar Buttons ---------------- #
    def create_sidebar_buttons(self, pages_list):
        """
        Create sidebar navigation buttons based on pages_list.

        pages_list example:
        [
            { "displayName": "Calendar", "className": CalendarPage, "default": True }
        ]
        """
        for idx, page in enumerate(pages_list):
            btn = ttk.Button(
                self.sidebar_frame,
                text=page["displayName"],
                command=lambda i=idx: self.page_controller.display_page(i)
            )
            btn.grid(row=idx+1, column=0, sticky="ew", padx=10, pady=5)
    
    # ---------------- Header ---------------- #
    def init_header(self):
        frame = tk.Frame(self.root, bg="red", width=1000, height=60)
        frame.grid(row=0, column=1, sticky="nsew")
        frame.grid_propagate(False)
        self.header_frame = frame

        # logo = tk.Label(
        #     frame,
        #     text="FitLife Studios",
        #     bg="green",
        #     fg="white",
        #     font=("Helvetica", 24, "bold"),
        #     justify="center"
        # )
        # logo.grid(row=0, column=0, padx=10, pady=(20, 30), sticky="n")

    # ---------------- Page Container ---------------- #
    def init_page_container(self):
        self.page_container = tk.Frame(self.root, bg="blue", width=1000, height=660)
        self.page_container.grid(row=1, column=1, sticky=tk.NSEW)


# Contain all common layout bits (navigation / header)