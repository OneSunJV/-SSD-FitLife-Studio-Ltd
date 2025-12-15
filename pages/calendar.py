import tkinter as tk
from tkinter import ttk
from calendar import monthrange, month_name
from datetime import datetime

DAYS_IN_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DISABLED_TEXT_COLOUR = "#ababab"

class CalendarPage:
    def __init__(self, frame):
        self.selectedYear = datetime.now().year
        self.selectedMonth = 6
        self.currentDay = datetime.now().day

        self.frame = frame
        self.frame.grid_columnconfigure(0, weight=50)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=50)

        self.days_frame: tk.Frame | None = None
        self.dateString: ttk.Label | None = None

        self.update_date_string()
        self.create_navigation_buttons()
        self.update_days_view()

    def create_days_frame(self):
        self.days_frame = tk.Frame(self.frame)
        self.days_frame.grid(row=1, columnspan=4, sticky=tk.NSEW)
        self.days_frame.grid_rowconfigure(0, weight=1)
        self.days_frame.grid_rowconfigure(1, weight=8)
        self.days_frame.grid_rowconfigure(2, weight=8)
        self.days_frame.grid_rowconfigure(3, weight=8)
        self.days_frame.grid_rowconfigure(4, weight=8)
        self.days_frame.grid_rowconfigure(5, weight=8)
        self.days_frame.grid_rowconfigure(6, weight=8)
        self.days_frame.grid_columnconfigure(0, weight=1, uniform="equal")
        self.days_frame.grid_columnconfigure(1, weight=1, uniform="equal")
        self.days_frame.grid_columnconfigure(2, weight=1, uniform="equal")
        self.days_frame.grid_columnconfigure(3, weight=1, uniform="equal")
        self.days_frame.grid_columnconfigure(4, weight=1, uniform="equal")
        self.days_frame.grid_columnconfigure(5, weight=1, uniform="equal")
        self.days_frame.grid_columnconfigure(6, weight=1, uniform="equal")

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

    def create_navigation_buttons(self):
        this_month_button = ttk.Button(self.frame, text="This month", command=self.this_month)
        previous_month_button = ttk.Button(self.frame, text="<", command=self.previous_month)
        next_month_button = ttk.Button(self.frame, text=">", command=self.next_month)

        this_month_button.grid(row=0, column=1)
        previous_month_button.grid(row=0, column=2)
        next_month_button.grid(row=0, column=3)

    def update_days_view(self):
        if self.days_frame is not None:
            self.days_frame.destroy() # Destroy frame if it already exists
        self.create_days_frame() # Create a new days frame

        first_day_offset, days_in_month = monthrange(self.selectedYear, self.selectedMonth)

        dates_in_range = []

        if first_day_offset > 0:
            prev_month, prev_months_year = self.get_previous_month(self.selectedMonth)
            _, days_in_prev_month = monthrange(prev_months_year, prev_month)

            for i in range(days_in_prev_month-first_day_offset, days_in_prev_month):
                dates_in_range.append({"month": prev_month, "day": i})

        for i in range(days_in_month):
            dates_in_range.append({"month": self.selectedMonth, "day": i+1})

        for i in range(6*7 - len(dates_in_range)): # Fill the remaining values with the next month (there are 6 rows * 7 columns)
            next_month, _next_months_year = self.get_next_month(self.selectedMonth)
            dates_in_range.append({"month": next_month, "day": i+1}) # We can never go over by more than 7 so we don't have to worry about how many days are in the month.

        row_offset = 1 # First row is used to display day of week

        for idx, day in enumerate(DAYS_IN_WEEK):
            label = ttk.Label(self.days_frame, text=day)
            label.grid(row=0, column=idx)

        for row in range(6): # 6 weeks
            for column in range(7): # 7 days per week
                date = dates_in_range[(column + 1) + (7 * row) - 1]
                day = date['day']
                month = date['month']
                label_foreground = "black" if month == self.selectedMonth else DISABLED_TEXT_COLOUR

                frame = ttk.Frame(self.days_frame, relief="solid", borderwidth=5)
                label = ttk.Label(frame, text=day, foreground=label_foreground)
                frame.grid(row=row+row_offset, column=column, sticky=tk.NSEW)
                label.grid(row=0, column=0, sticky=tk.NW)

    
    @staticmethod
    def month_to_string(month_integer: int):
        return month_name[month_integer]

    def get_previous_month(self, current_month: int) -> (int, int):
        # If current month is January, return December and the previous year
        if current_month == 1:
            return 12, (self.selectedYear - 1)
        else: # Else just return the previous month and the current year.
            return current_month - 1, self.selectedYear

    def get_next_month(self, current_month: int) -> (int, int):
        if current_month == 12:
            return 1, (self.selectedYear + 1)
        else:
            return current_month + 1, self.selectedYear

    def next_month(self):
        if self.selectedMonth == 12:
            self.selectedMonth = 1
            self.selectedYear += 1
        else:
            self.selectedMonth += 1

        self.update_date_string()
        self.update_days_view()

    def previous_month(self):
        if self.selectedMonth == 1:
            self.selectedMonth = 12
            self.selectedYear -= 1
        else:
            self.selectedMonth -= 1

        self.update_date_string()
        self.update_days_view()

    def this_month(self):
        self.selectedYear = datetime.now().year
        self.selectedMonth = datetime.now().month

        self.update_date_string()
        self.update_days_view()
