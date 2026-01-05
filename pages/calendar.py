import tkinter as tk
from tkinter import ttk
from calendar import monthrange, month_name
from datetime import datetime
from functools import partial


DAYS_IN_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DISABLED_TEXT_COLOUR = "#ababab"
MAX_WINDOW_HEIGHT = 720
WINDOW_WIDTH = 600

class Event:
    def __init__(self, title):
        self.title = title

class DateInfo:
    def __init__(self, day, month, events: list[Event]):
        self.day = day
        self.month = month
        self.events = events

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

        # ToDo query database using dates_in_range to get the events for the given dates
        calendar_days: list[DateInfo] = list(map(lambda d: DateInfo(d['day'], d['month'], [Event("Example Event 1"), Event("Example Event 2"), Event("Example Event 3"), Event("Example Event 4"), Event("Example Event 5")]), dates_in_range))

        row_offset = 1 # First row is used to display day of week

        for idx, day in enumerate(DAYS_IN_WEEK):
            label = ttk.Label(self.days_frame, text=day)
            label.grid(row=0, column=idx)

        for row in range(6): # 6 weeks
            for column in range(7): # 7 days per week
                date = calendar_days[(column + 1) + (7 * row) - 1]
                label_foreground = "black" if date.month == self.selectedMonth else DISABLED_TEXT_COLOUR

                frame = ttk.Frame(self.days_frame, relief="solid", borderwidth=5)
                frame.grid_columnconfigure(0, weight=1)
                frame.grid_rowconfigure(0, weight=1)
                frame.grid_rowconfigure(1, weight=1)
                frame.grid_rowconfigure(2, weight=1)
                frame.grid_rowconfigure(3, weight=1)

                label = ttk.Label(frame, text=date.day, foreground=label_foreground)
                frame.grid(row=row+row_offset, column=column, sticky=tk.NSEW)
                label.grid(row=0, column=0, sticky=tk.NW)

                frame.bind("<Button-1>", partial(self.open_date_overview, date))
                label.bind("<Button-1>", partial(self.open_date_overview, date))

                for idx, event in enumerate(date.events):
                    if idx == 2 and len(date.events) > 3:
                        button = ttk.Button(frame, text=f"+ {len(date.events) - 2} more", command=partial(self.open_date_overview, date))
                        button.grid(row=idx + 1, column=0, sticky=tk.EW)
                        break
                    else:
                        button = ttk.Button(frame, text=event.title, command=partial(self.open_event_view, event))
                        button.grid(row=idx + 1, column=0, sticky=tk.EW)
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
        if self.selectedMonth != datetime.now().month:
            self.selectedYear = datetime.now().year
            self.selectedMonth = datetime.now().month

            self.update_date_string()
            self.update_days_view()

    def open_date_overview(self, date: DateInfo, _event=None):
        root = self.frame.winfo_toplevel()

        top = tk.Toplevel(root)
        top.resizable(False, False)
        top.title("Date Overview")
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)

        canvas = tk.Canvas(top)
        scrollbar = ttk.Scrollbar(top, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=0, column=00, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        def on_canvas_configure(event):
            canvas.itemconfigure(window_id, width=event.width)

        canvas.bind("<Configure>", on_canvas_configure)

        content = ttk.Frame(canvas)
        window_id = canvas.create_window(0, 0, window=content, anchor="nw")
        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=1)
        label = ttk.Label(content, text="Date Overview")
        label.grid(row=0, column=0, sticky=tk.NSEW)

        def resize():
            content.update_idletasks()
            height = min(content.winfo_reqheight(), MAX_WINDOW_HEIGHT)
            top.geometry(f"{WINDOW_WIDTH}x{height}")
            canvas.configure(scrollregion=canvas.bbox("all"))

        content.bind("<Configure>", lambda e: content.after_idle(resize))

        for idx, event in enumerate(date.events):
            button = ttk.Button(content, text=f"{event.title}", command=partial(self.open_event_view, event))
            button.grid(row=idx + 1, column=0, sticky=tk.EW)

        print(f"FRAME CLICKED: {date.day}/{date.month}")

    def open_event_view(self, event: Event):
        print(f"EVENT CLICKED: {event.title}")