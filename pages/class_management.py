import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

class ClassManagementPage:
    def __init__(self, sample_frame):
        self.frame = sample_frame
        self.frame.config(bg="white")

        # Defines the columns in the main frame
        self.frame.columnconfigure(0, weight=1)

        # Defines the rows in the main frame
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=3)

        # Calling methods that setup different UI parts of page
        self.init_filters_frame()
        self.init_treeview_frame()

    def init_filters_frame(self):
        self.filters_frame = ttk.Frame(self.frame)

        # Defines the columns in the filters frame
        self.filters_frame.columnconfigure(0, weight=1)
        self.filters_frame.columnconfigure(1, weight=1)
        self.filters_frame.columnconfigure(2, weight=1)
        self.filters_frame.columnconfigure(3, weight=1)
        self.filters_frame.columnconfigure(4, weight=1)
        self.filters_frame.columnconfigure(5, weight=1)
        self.filters_frame.columnconfigure(6, weight=1)
        self.filters_frame.columnconfigure(7, weight=1)

        # Defines the rows in the filters frame
        self.filters_frame.rowconfigure(0, weight=1)
        self.filters_frame.rowconfigure(1, weight=1)
        self.filters_frame.rowconfigure(2, weight=1)
        self.filters_frame.rowconfigure(3, weight=1)

        self.filters_frame.grid(column=0, row=0, padx=5, pady=5, sticky=tk.NSEW)

        # Defining filters title
        filters_label = ttk.Label(self.filters_frame, text="Search / Add / Remove Sessions", font=("Arial", 11, "bold"))
        filters_label.grid(column=0, row=0, padx=5, pady=5, sticky=tk.EW)

        # Defining filters
        sessionID_label = ttk.Label(self.filters_frame, text="SessionID:")
        sessionID_label.grid(column=0, row=1, sticky=tk.E)
        self.sessionID_entrybox = ttk.Entry(self.filters_frame)
        self.sessionID_entrybox.grid(column=1, row=1, padx=5, sticky=tk.EW)

        classType_label = ttk.Label(self.filters_frame, text="Class Type:")
        classType_label.grid(column=2, row=1, sticky=tk.E)
        self.classType_entrybox = ttk.Entry(self.filters_frame)
        self.classType_entrybox.grid(column=3, padx=5, row=1, sticky=tk.EW)

        trainer_label = ttk.Label(self.filters_frame, text="Trainer:")
        trainer_label.grid(column=4, row=1, sticky=tk.E)
        self.trainer_combobox = ttk.Combobox(self.filters_frame)
        self.trainer_combobox.grid(column=5, padx=5, row=1, sticky=tk.EW)

        sessionDate_label = ttk.Label(self.filters_frame, text="Session Date:")
        sessionDate_label.grid(column=6, row=1, sticky=tk.E)
        self.sessionDate_dateEntry = DateEntry(self.filters_frame)
        self.sessionDate_dateEntry.grid(column=7, padx=5, row=1, sticky=tk.EW)

        sessionStartTime_label = ttk.Label(self.filters_frame, text="Session Start Time:")
        sessionStartTime_label.grid(column=0, row=2, sticky=tk.E)
        self.sessionStartTime_combobox = ttk.Combobox(self.filters_frame)
        self.sessionStartTime_combobox.grid(column=1, padx=5, row=2, sticky=tk.EW)

        sessionFinishTime_label = ttk.Label(self.filters_frame, text="Session Finish Time:")
        sessionFinishTime_label.grid(column=2, row=2, sticky=tk.E)
        self.sessionFinishTime_combobox = ttk.Combobox(self.filters_frame)
        self.sessionFinishTime_combobox.grid(column=3, padx=5, row=2, sticky=tk.EW)

        sessionLocation_label = ttk.Label(self.filters_frame, text="Session Location:")
        sessionLocation_label.grid(column=4, row=2, sticky=tk.E)
        self.sessionLocation_combobox = ttk.Combobox(self.filters_frame)
        self.sessionLocation_combobox.grid(column=5, padx=5, row=2, sticky=tk.EW)

        # Defining action buttons
        search_sessions_button = ttk.Button(self.filters_frame, text="Search sessions")
        search_sessions_button.grid(column=4, row=3, sticky=tk.EW)

        refresh_sessions_button = ttk.Button(self.filters_frame, text="Refresh sessions")
        refresh_sessions_button.grid(column=5, row=3, sticky=tk.EW)

        add_sessions_button = ttk.Button(self.filters_frame, text="Add session")
        add_sessions_button.grid(column=6, row=3, sticky=tk.EW)

        delete_sessions_button = ttk.Button(self.filters_frame, text="Delete session")
        delete_sessions_button.grid(column=7, row=3, sticky=tk.EW)


    def init_treeview_frame(self):
        self.treeview_frame = ttk.Frame(self.frame)

        # Defines the rows in the treeview frame
        self.treeview_frame.rowconfigure(0, weight=1)
        self.treeview_frame.rowconfigure(1, weight=10)

        # Defines the columns in the treeview frame
        self.treeview_frame.columnconfigure(0, weight=1)

        self.treeview_frame.grid(column=0, row=1, padx=5, pady=5, sticky=tk.NSEW)

        # Defining title
        session_records_label = ttk.Label(self.treeview_frame, text="Studio session records", font=("Arial", 11, "bold"))
        session_records_label.grid(column=0, row=0, sticky=tk.NSEW, padx=400)

        # Defining Treeview
        table_columns = ("SessionID", "Class Type", "Trainer", "Session Date", "Session Start Time", "Session Finish Time", "Spaces Available", "Session Location")
        self.sessions_table = ttk.Treeview(self.treeview_frame, columns=table_columns, show="headings")

        self.sessions_table.heading("SessionID", text="SessionID")
        self.sessions_table.heading("Class Type", text="Class Type")
        self.sessions_table.heading("Trainer", text="Trainer")
        self.sessions_table.heading("Session Date", text="Session Date")
        self.sessions_table.heading("Session Start Time", text="Session Start Time")
        self.sessions_table.heading("Session Finish Time", text="Session Finish Time")
        self.sessions_table.heading("Spaces Available", text="Spaces Available")
        self.sessions_table.heading("Session Location", text="Session Location")

        self.sessions_table.column("SessionID", width=40)
        self.sessions_table.column("Class Type", width=70)
        self.sessions_table.column("Trainer", width=90)
        self.sessions_table.column("Session Date", width=80)
        self.sessions_table.column("Session Start Time", width=80)
        self.sessions_table.column("Session Finish Time", width=80)
        self.sessions_table.column("Spaces Available", width=80)
        self.sessions_table.column("Session Location", width=80)

        self.sessions_table.insert("", tk.END, values=(1,2,3,4,5,6,7),)
        
        self.sessions_table.grid(column=0, row=1, sticky=tk.NSEW, padx=10, pady=5)
 
    def create_session():
        pass
        #Create new window
    
    def delete_session():
        pass