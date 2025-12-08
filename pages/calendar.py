import tkinter as tk;
from tkinter import ttk
from calendar import monthrange, month_name
from datetime import datetime

LARGEFONT =("Verdana", 35)

class CalendarPage:
    def __init__(self, frame):
        self.selectedYear = datetime.now().year
        self.selectedMonth = datetime.now().month
        self.currentDay = datetime.now().day

        self.frame = frame;

        label = ttk.Label(self.frame, text="Calendar")
        label.grid(row = 0, column = 0)

        self.updateYearLabel()
        self.updateMonthLabel()
    
    def select_month(self, month):
        self.selectedMonth = month
        daysInMonth = monthrange(self.selectedYear, month)
        self.updateMonthLabel()

        # Update display

    def updateYearLabel(self):
        yearLabel = ttk.Label(self.frame, text="Year:")
        yearLabel.grid(row=1, column=0)
        selectedYearLabel = ttk.Label(self.frame, text=f"{self.selectedYear}")
        selectedYearLabel.grid(row=2, column=0)

    def updateMonthLabel(self):
        monthLabel = ttk.Label(self.frame, text="Month:")
        monthLabel.grid(row=3, column=0)
        selectedMonthLabel = ttk.Label(self.frame, text=f"{self.month_to_string(self.selectedMonth)}")
        selectedMonthLabel.grid(row=4, column=0)
    
    def month_to_string(self, monthInteger: int):
        return month_name[monthInteger]