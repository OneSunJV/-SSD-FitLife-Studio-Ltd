import tkinter as tk
from tkinter import ttk
from calendar import monthrange, month_name
from datetime import datetime
from functools import partial
import sqlite3

DAYS_IN_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DISABLED_TEXT_COLOUR = "#ababab"
MAX_WINDOW_HEIGHT = 720
WINDOW_WIDTH = 600

USER_ID = 1 # In the full app this would come from the user's authentication session.

class Event:
    def __init__(self, title, start, finish):
        self.title = title
        self.start = start
        self.finish = finish

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
                dates_in_range.append({"year": prev_months_year, "month": prev_month, "day": i})

        for i in range(days_in_month):
            dates_in_range.append({"year": self.selectedYear, "month": self.selectedMonth, "day": i+1})

        for i in range(6*7 - len(dates_in_range)): # Fill the remaining values with the next month (there are 6 rows * 7 columns)
            next_month, next_months_year = self.get_next_month(self.selectedMonth)
            dates_in_range.append({"year": next_months_year, "month": next_month, "day": i+1}) # We can never go over by more than 7 so we don't have to worry about how many days are in the month.

        calendar_days: list[DateInfo] = get_events_for_dates(dates_in_range)

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

                frame.bind("<Button-1>", partial(self.open_date_overview, date, None))
                label.bind("<Button-1>", partial(self.open_date_overview, date, None))

                for idx, event in enumerate(date.events):
                    if idx == 2 and len(date.events) > 3:
                        button = ttk.Button(frame, text=f"+ {len(date.events) - 2} more", command=partial(self.open_date_overview, date, None))
                        button.grid(row=idx + 1, column=0, sticky=tk.EW)
                        break
                    else:
                        button = ttk.Button(frame, text=event.title, command=partial(self.open_date_overview, date, event))
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

    def open_date_overview(self, date: DateInfo, selected_event: Event=None, _event=None):
        root = self.frame.winfo_toplevel()

        top = tk.Toplevel(root)
        top.resizable(False, False)
        top.title("Date Overview")
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)

        frame = ttk.Frame(top)
        frame.grid(row=0, column=0, sticky=tk.NSEW)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        columns = ("event", "start", "end")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        tree.heading("event", text="Event")
        tree.heading("start", text="Starts At")
        tree.heading("end", text="Ends At")
        tree.grid(row=0, column=0, sticky=tk.NSEW)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        for event in date.events:
            start_time = datetime.fromtimestamp(event.start).time()
            start_time_str = f"{start_time.hour:02}:{start_time.minute:02}"
            end_time = datetime.fromtimestamp(event.finish).time()
            end_time_str = f"{end_time.hour:02}:{end_time.minute:02}"

            values = (event.title, start_time_str, end_time_str)
            tree.insert("", "end", values=values)

        if selected_event is not None:
            idx = date.events.index(selected_event)
            selected_row = tree.get_children()[idx]
            tree.selection_set(selected_row)

        def resize():
            tree.update_idletasks()
            req_height = tree.winfo_reqheight()
            # Clamp height to the maximum window height
            height = min(req_height, MAX_WINDOW_HEIGHT)
            top.geometry(f"{WINDOW_WIDTH}x{height}")
            # Show scrollbar only if needed
            if req_height > MAX_WINDOW_HEIGHT:
                scrollbar.grid()
            else:
                scrollbar.grid_remove()

        tree.bind("<Configure>", lambda e: tree.after_idle(resize))

        print(f"FRAME CLICKED: {date.day}/{date.month}")

def get_events_for_dates(dates) -> list[DateInfo]:
    dates_with_events: list[DateInfo] = []

    connection = sqlite3.connect("database/SystemDatabase.db")
    cursor = connection.cursor()

    for date in dates:
        day = date["day"]
        month = date["month"]
        year = date["year"]

        date_str = f"{year}-{month:02}-{day:02}"
        cursor.execute(f'''SELECT 
                                Classes.ClassType, Sessions.SessionStartTime, Sessions.SessionFinishTime
                           FROM Sessions 
                           INNER JOIN Classes 
                                ON Sessions.ClassID = Classes.ClassID
                           WHERE 
                                Sessions.TrainerID == {USER_ID} 
                                AND SessionDate == '{date_str}'
                           ORDER BY Sessions.SessionStartTime;''')

        rows = cursor.fetchall()

        dates_with_events.append(DateInfo(day, month, list(map(lambda r: Event(r[0], r[1], r[2]), rows))))


    connection.close()

    return dates_with_events

