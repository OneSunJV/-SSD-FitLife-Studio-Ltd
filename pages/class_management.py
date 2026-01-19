import tkinter as tk
from tkinter import ttk
from calendar import monthrange, month_name
from datetime import datetime

class ClassManagementPage:
    def __init__(self, sample_frame):
        self.frame = sample_frame
        self.frame.config(bg="white")

        # Defines the columns in the main frame
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        # Defines the rows in the main frame
        self.frame.rowconfigure(0, weight=2)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=5)

        self.init_title()
        self.init_filters_table()

    def init_title(self):
        self.title_label = ttk.Label(self.frame, text="Equipment Maintenance Records", font=("Arial", 14))
        self.title_label.grid(column=0, row=0, sticky=tk.NW)


    def init_treeview(self):
        table_columns = ("SessionID", "ClassID", "TrainerID", "SessionDate", "SessionStartTime", "SessionFinishTime")
        self.sessions_table = ttk.Treeview(self.frame, columns=table_columns)

        self.sessions_table.heading(column="SessionID", text="SessionID")
        self.sessions_table.heading(column="ClassID", text="ClassID")
        self.sessions_table.heading(column="TrainerID", text="TrainerID")
        self.sessions_table.heading(column="SessionDate", text="SessionDate")
        self.sessions_table.heading(column="SessionStartTime", text="SessionStartTime")
        self.sessions_table.heading(column="SessionFinishTime", text="SessionFinishTime")

       
        self.sessions_table.grid(row=2, column=0, sticky=tk.EW)
 
    def create_session():
        pass
        #Create new window
    
    def delete_session():
        pass