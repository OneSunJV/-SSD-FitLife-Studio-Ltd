import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime

TRAINERS = []
TRAINERS_WITH_ID_APPENDED = []
CLASSTYPES = []
TIMES = ["9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00"]
LOCATIONS = ["Location A", "Location B", "Location C"]

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

        self.load_data()

    def load_data(self):
        # Getting Trainers
        with sqlite3.connect('SystemDatabase.db') as connection:
            cursor_object = connection.cursor()
            cursor_object.execute('''SELECT FirstName, LastName, EmployeeID
                                     FROM Employees
                                     WHERE EmployeeType LIKE ?''', ("TRAINER",))
            trainers_entries = cursor_object.fetchall()
            for trainer_data in trainers_entries:
                TRAINERS.append(str(trainer_data[0]) + " " + str(trainer_data[1]))
                TRAINERS_WITH_ID_APPENDED.append((trainer_data[2], str(trainer_data[0]) + " " + str(trainer_data[1])))
                print((trainer_data[2], str(trainer_data[0]) + " " + str(trainer_data[1])))

            # Getting Class Types
            cursor_object.execute('''SELECT ClassType
                                     FROM Classes''')
            class_types_entries = cursor_object.fetchall()
            for class_types_data in class_types_entries:
                for class_type in class_types_data:
                    CLASSTYPES.append(str(class_type))

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
        filters_label.grid(column=0, row=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)

        # Defining filters
        sessionID_label = ttk.Label(self.filters_frame, text="SessionID:")
        sessionID_label.grid(column=0, row=1, sticky=tk.E)
        self.sessionID_entrybox = ttk.Entry(self.filters_frame)
        self.sessionID_entrybox.grid(column=1, row=1, padx=5, sticky=tk.EW)

        classType_label = ttk.Label(self.filters_frame, text="Class Type:")
        classType_label.grid(column=2, row=1, sticky=tk.E)      
        self.classType_entrybox = ttk.Combobox(self.filters_frame, values=CLASSTYPES)
        self.classType_entrybox.grid(column=3, padx=5, row=1, sticky=tk.EW)

        trainer_label = ttk.Label(self.filters_frame, text="Trainer:")
        trainer_label.grid(column=4, row=1, sticky=tk.E)
        
        self.trainer_combobox = ttk.Combobox(self.filters_frame, values=TRAINERS)
        self.trainer_combobox.grid(column=5, padx=5, row=1, sticky=tk.EW)

        sessionDate_label = ttk.Label(self.filters_frame, text="Session Date:")
        sessionDate_label.grid(column=6, row=1, sticky=tk.E)
        self.sessionDate_dateEntry = DateEntry(self.filters_frame, date_pattern="dd/MM/yyyy")
        self.sessionDate_dateEntry.grid(column=7, padx=5, row=1, sticky=tk.EW)

        sessionStartTime_label = ttk.Label(self.filters_frame, text="Session Start Time:")
        sessionStartTime_label.grid(column=0, row=2, sticky=tk.E)
        self.sessionStartTime_combobox = ttk.Combobox(self.filters_frame, values=TIMES)
        self.sessionStartTime_combobox.grid(column=1, padx=5, row=2, sticky=tk.EW)

        sessionFinishTime_label = ttk.Label(self.filters_frame, text="Session Finish Time:")
        sessionFinishTime_label.grid(column=2, row=2, sticky=tk.E)
        self.sessionFinishTime_combobox = ttk.Combobox(self.filters_frame, values=TIMES)
        self.sessionFinishTime_combobox.grid(column=3, padx=5, row=2, sticky=tk.EW)

        sessionLocation_label = ttk.Label(self.filters_frame, text="Session Location:")
        sessionLocation_label.grid(column=4, row=2, sticky=tk.E)
        self.sessionLocation_combobox = ttk.Combobox(self.filters_frame, values=LOCATIONS)
        self.sessionLocation_combobox.grid(column=5, padx=5, row=2, sticky=tk.EW)

        # Defining action buttons
        search_sessions_button = ttk.Button(self.filters_frame, text="🔍︎Search sessions", command=lambda: self.search_sessions())
        search_sessions_button.grid(column=4, row=3, sticky=tk.EW)

        refresh_sessions_button = ttk.Button(self.filters_frame, text="➕ Add session", command=lambda: self.create_session())
        refresh_sessions_button.grid(column=5, row=3, sticky=tk.EW)

        add_sessions_button = ttk.Button(self.filters_frame, text="➖ Delete session", command=lambda: self.delete_session())
        add_sessions_button.grid(column=6, row=3, sticky=tk.EW)

        delete_sessions_button = ttk.Button(self.filters_frame, text="⟳ Refresh table", command=lambda: self.refresh_treeview())
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
        table_columns = ("SessionID", "Class Type", "Trainer", "Session Date", "Session Start Time", "Session Finish Time", "Session Location")
        self.sessions_table = ttk.Treeview(self.treeview_frame, columns=table_columns, show="headings")

        self.sessions_table.heading("SessionID", text="SessionID")
        self.sessions_table.heading("Class Type", text="Class Type")
        self.sessions_table.heading("Trainer", text="Trainer")
        self.sessions_table.heading("Session Date", text="Session Date")
        self.sessions_table.heading("Session Start Time", text="Session Start Time")
        self.sessions_table.heading("Session Finish Time", text="Session Finish Time")
        self.sessions_table.heading("Session Location", text="Session Location")

        self.sessions_table.column("SessionID", width=60)
        self.sessions_table.column("Class Type", width=100)
        self.sessions_table.column("Trainer", width=100)
        self.sessions_table.column("Session Date", width=80)
        self.sessions_table.column("Session Start Time", width=80)
        self.sessions_table.column("Session Finish Time", width=80)
        self.sessions_table.column("Session Location", width=100)

        self.sessions_table.insert("", tk.END, values=(1,2,3,4,5,6,7),)
        
        self.sessions_table.grid(column=0, row=1, sticky=tk.NSEW, padx=10, pady=5)
 
    
    def search_sessions(self):
        for row in self.sessions_table.get_children():
            self.sessions_table.delete(row)

        connection = sqlite3.connect('SystemDatabase.db')
        cursor_object = connection.cursor()
        cursor_object.execute('''SELECT SessionID, ClassType, TrainerID, SessionDate, SessionStartTime, SessionFinishTime, SessionLocation FROM Sessions INNER JOIN Classes ON Sessions.ClassID = Classes.ClassID;''')
        search_results_tuple = cursor_object.fetchall()
        connection.close()
        session_list = []
        trainer_name = ''
        for session_tuple in search_results_tuple:
            for trainer in TRAINERS_WITH_ID_APPENDED:
                if session_tuple[2] == trainer[0]:
                    trainer_name = trainer[1]
            session_list.append((session_tuple[0], session_tuple[1], trainer_name, session_tuple[3], session_tuple[4], session_tuple[5], session_tuple[6]))
        for session in session_list:
            self.sessions_table.insert("", tk.END, values=session,)

    def create_session(self):
        self.session_ID = self.sessionID_entrybox.get()
        self.class_type = self.classType_entrybox.get()
        self.trainer_name = self.trainer_combobox.get()
        self.session_date = self.sessionDate_dateEntry.get_date()
        self.session_start_time = self.sessionStartTime_combobox.get()
        self.session_end_time = self.sessionFinishTime_combobox.get()
    
    def delete_session(self):
        pass

    def refresh_treeview(self):
        for row in self.sessions_table.get_children():
            self.sessions_table.delete(row)

        connection = sqlite3.connect('SystemDatabase.db')
        cursor_object = connection.cursor()
        cursor_object.execute('''SELECT SessionID, ClassType, TrainerID, SessionDate, SessionStartTime, SessionFinishTime, SessionLocation FROM Sessions INNER JOIN Classes ON Sessions.ClassID = Classes.ClassID;''')
        search_results_tuple = cursor_object.fetchall()
        connection.close()
        session_list = []
        trainer_name = ''
        for session_tuple in search_results_tuple:
            for trainer in TRAINERS_WITH_ID_APPENDED:
                if session_tuple[2] == trainer[0]:
                    trainer_name = trainer[1]
            session_list.append((session_tuple[0], session_tuple[1], trainer_name, session_tuple[3], session_tuple[4], session_tuple[5], session_tuple[6]))
        for session in session_list:
            self.sessions_table.insert("", tk.END, values=session,)