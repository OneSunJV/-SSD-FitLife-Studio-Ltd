import tkinter as tk
from tkinter import ttk
from calendar import monthrange, month_name
from datetime import datetime

DAYS_IN_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class CalendarPage:
    def __init__(self, frame):
        self.selectedYear = datetime.now().year
        self.selectedMonth = datetime.now().month
        self.currentDay = datetime.now().day

        self.frame = frame
        self.frame.grid_columnconfigure(0, weight=50)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=50)

        self.days_frame_initialised: bool = False
        self.days_frame = tk.Frame(self.frame)
        self.days_frame.grid(row=1, columnspan=4, sticky=tk.NSEW)
        self.days_frame.grid_rowconfigure(0, weight=1)
        self.days_frame.grid_rowconfigure(1, weight=8)
        self.days_frame.grid_rowconfigure(2, weight=8)
        self.days_frame.grid_rowconfigure(3, weight=8)
        self.days_frame.grid_rowconfigure(4, weight=8)
        self.days_frame.grid_rowconfigure(5, weight=8)
        self.days_frame.grid_columnconfigure(0, weight=1, uniform="equal")
        self.days_frame.grid_columnconfigure(1, weight=1, uniform="equal")
        self.days_frame.grid_columnconfigure(2, weight=1, uniform="equal")
        self.days_frame.grid_columnconfigure(3, weight=1, uniform="equal")
        self.days_frame.grid_columnconfigure(4, weight=1, uniform="equal")
        self.days_frame.grid_columnconfigure(5, weight=1, uniform="equal")
        self.days_frame.grid_columnconfigure(6, weight=1, uniform="equal")

        self.dateString: ttk.Label | None = None

        self.update_date_string()
        self.build_navigation_buttons()
        self.update_days_view()


    def update_date_string(self):

        month_str = CalendarPage.month_to_string(self.selectedMonth)
        new_string = f"{month_str} - {self.selectedYear}"

        # Update label if it already exists, or create a new one.
        if self.dateString is not None:
            self.dateString.config(text=new_string)
        else:
            self.dateString = ttk.Label(self.frame, text=new_string, font=("Verdana", 25))
            self.dateString.grid(row=0, column=0, sticky=tk.W)
            self.dateString.bind("<Button-1>", lambda e: self.update_date_string())

    def build_navigation_buttons(self):
        this_month_button = ttk.Button(self.frame, text="This month")
        previous_month_button = ttk.Button(self.frame, text="<")
        next_month_button = ttk.Button(self.frame, text=">")

        this_month_button.grid(row=0, column=1)
        previous_month_button.grid(row=0, column=2)
        next_month_button.grid(row=0, column=3)

    def update_days_view(self):
        row_offset = 1 # First row is used to display day of week
        if self.days_frame_initialised:
            return

        for idx, day in enumerate(DAYS_IN_WEEK):
            label = ttk.Label(self.days_frame, text=day)
            label.grid(row=0, column=idx)

        for row in range(5): # 5 weeks
            for column in range(7): # 7 days per week
                frame = ttk.Frame(self.days_frame)
                frame['borderwidth'] = 5
                frame['relief'] = 'ridge'
                label = ttk.Label(frame, text=f"{(column + 1) + (7 * row)}")
                frame.grid(row=row+row_offset, column=column, sticky=tk.NSEW)
                label.grid(row=0, column=0, sticky=tk.NW)
        self.days_frame_initialised = True
        
    
    @staticmethod
    def month_to_string(month_integer: int):
        return month_name[month_integer]