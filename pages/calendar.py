import tkinter as tk;
from tkinter import ttk
from calendar import monthrange, month_name
from datetime import datetime

LARGEFONT =("Verdana", 25)

class CalendarPage:
    def __init__(self, frame):
        self.selectedYear = datetime.now().year
        self.selectedMonth = datetime.now().month
        self.currentDay = datetime.now().day

        self.frame = frame;
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)
        self.frame.grid_columnconfigure(4, weight=1)



        label = ttk.Label(self.frame, text="Calendar", justify="center")
        label.grid(row=0, column=2)

        self.updateYearLabel()
        self.updateMonthLabel()
    
    def select_month(self, month):
        self.selectedMonth = month
        daysInMonth = monthrange(self.selectedYear, month)
        self.updateMonthLabel()

        # Update display

    def updateYearLabel(self):
        yearLabel = ttk.Label(self.frame, text="Year")
        yearLabel.grid(row=1, column=2, pady=5)
        leftButton = ttk.Button(self.frame, text="<")
        leftButton.grid(row=2, column=1)
        selectedYearLabel = ttk.Label(self.frame, text=f"{self.selectedYear}", font=LARGEFONT)
        selectedYearLabel.grid(row=2, column=2)
        rightButton = ttk.Button(self.frame, text=">")
        rightButton.grid(row=2, column=3)

    def updateMonthLabel(self):
        monthLabel = ttk.Label(self.frame, text="Month")
        monthLabel.grid(row=3, column=2, pady=5)
        leftButton = ttk.Button(self.frame, text="<")
        leftButton.grid(row=4, column=1)
        selectedMonthLabel = ttk.Label(self.frame, text=f"{self.month_to_string(self.selectedMonth)}", font=LARGEFONT)
        selectedMonthLabel.grid(row=4, column=2)
        rightButton = ttk.Button(self.frame, text=">")
        rightButton.grid(row=4, column=3)
    
    def month_to_string(self, monthInteger: int):
        return month_name[monthInteger]