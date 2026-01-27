import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime

TRAINERS = []
TRAINERS_WITH_ID_APPENDED = []
CLASSTYPES = []
CLASSTYPES_WITH_ID_APPENDED = []
TIMES = ["","9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00"]
LOCATIONS = ["","Location A", "Location B", "Location C"]

#Getting Trainers
connection = sqlite3.connect('SystemDatabase.db')
cursor_object = connection.cursor()
cursor_object.execute('''SELECT FirstName, LastName, EmployeeID FROM Employees WHERE EmployeeType LIKE ?''', ("TRAINER",))
trainers_entries = cursor_object.fetchall()
connection.close()
for trainer_data in trainers_entries:
    TRAINERS.append(str(trainer_data[0]) +  " " + str(trainer_data[1]))
    TRAINERS_WITH_ID_APPENDED.append((trainer_data[2], str(trainer_data[0]) +  " " + str(trainer_data[1]))) # (TrainerID, Full Name)

#Getting Class Types
connection = sqlite3.connect('SystemDatabase.db')
cursor_object = connection.cursor()
cursor_object.execute('''SELECT ClassID, ClassType FROM Classes''')
class_types_entries = cursor_object.fetchall()
connection.close()
for class_type in class_types_entries:
    CLASSTYPES.append(str(class_type[1]))
    CLASSTYPES_WITH_ID_APPENDED.append((class_type[0], str(class_type[1]))) # (ClassID, ClassType)



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
    
        self.valid_session_ID_flag = False
        self.valid_entries_flag = False

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

        self.date_filter_disabled_check = tk.BooleanVar()
        self.disable_date_checkbox = ttk.Checkbutton(self.filters_frame, text="Disable date filter", command=self.disable_or_enable_date_filter, variable=self.date_filter_disabled_check)
        self.disable_date_checkbox.grid(column=0, row=3, columnspan=2, sticky=tk.EW)

        # Defining action buttons
        search_sessions_button = ttk.Button(self.filters_frame, text="🔍︎Search sessions", command=self.search_sessions)
        search_sessions_button.grid(column=4, row=3, sticky=tk.EW)

        refresh_sessions_button = ttk.Button(self.filters_frame, text="➕ Add session", command=self.create_session)
        refresh_sessions_button.grid(column=5, row=3, sticky=tk.EW)

        add_sessions_button = ttk.Button(self.filters_frame, text="➖ Delete session", command=self.delete_session)
        add_sessions_button.grid(column=6, row=3, sticky=tk.EW)

        delete_sessions_button = ttk.Button(self.filters_frame, text="⟳ Refresh table", command=self.refresh_treeview)
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
        
        self.sessions_table.grid(column=0, row=1, sticky=tk.NSEW, padx=10, pady=5)
    


    def disable_or_enable_date_filter(self):
        if self.date_filter_disabled_check.get() == True:
            self.sessionDate_dateEntry.config(state=["disabled"])
        else:
            self.sessionDate_dateEntry.config(state=['normal'])



    def get_parameters_from_entries(self):
        self.session_ID = str(self.sessionID_entrybox.get())
        self.class_type = ''
        self.trainer_ID = ''
        self.session_date = ''
        if self.date_filter_disabled_check.get() == False:
            self.session_date = str((self.sessionDate_dateEntry.get_date()).strftime("%d-%m-%Y"))
        self.session_start_time = str(self.sessionStartTime_combobox.get())
        self.session_end_time = str(self.sessionFinishTime_combobox.get())
        self.session_location = str(self.sessionLocation_combobox.get())



    def search_sessions(self):
        self.get_parameters_from_entries()

        for trainer in TRAINERS_WITH_ID_APPENDED:
            if trainer[1] == str(self.trainer_combobox.get()):
                self.trainer_ID = str(trainer[0])
                break

        for type_of_class in CLASSTYPES_WITH_ID_APPENDED:
            if type_of_class[1] == str(self.classType_entrybox.get()):
                self.class_type = str(type_of_class[0])
                break

        if self.session_ID and self.class_type and self.trainer_ID and self.session_date and self.session_start_time and self.session_end_time and self.session_location == '':
            self.refresh_treeview()
        else:
            try:
                for row in self.sessions_table.get_children():
                    self.sessions_table.delete(row)

                self.session_ID = self.session_ID + '%'
                self.class_type =  self.class_type + '%'
                self.trainer_ID =  self.trainer_ID + '%'
                self.session_date = self.session_date + '%'
                self.session_start_time =  self.session_start_time + '%'
                self.session_end_time =  self.session_end_time + '%'
                self.session_location = self.session_location + '%'

                connection = sqlite3.connect('SystemDatabase.db')
                cursor_object = connection.cursor()
                cursor_object.execute('''SELECT SessionID, ClassType, TrainerID, SessionDate, SessionStartTime, SessionFinishTime, SessionLocation FROM Sessions 
                                    INNER JOIN Classes ON Sessions.ClassID = Classes.ClassID 
                                    WHERE SessionID LIKE ? AND ClassType LIKE ? AND TrainerID LIKE ? AND SessionDate LIKE ? AND SessionStartTime LIKE ? AND SessionFinishTime LIKE ? AND SessionLocation LIKE ? 
                                    GROUP BY SessionID, ClassType, TrainerID, SessionDate, SessionStartTime, SessionFinishTime, SessionLocation''', 
                                    (self.session_ID, self.class_type, self.trainer_ID, self.session_date, self.session_start_time, self.session_end_time, self.session_location))
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
            except:
                showerror(title = "Error 404", message = "Something went wrong!")



    def create_session(self):
        self.get_parameters_from_entries()

        self.class_ID = ''

        # Fetches TrainerID
        for trainer in TRAINERS_WITH_ID_APPENDED:
            if trainer[1] == str(self.trainer_combobox.get()):
                self.trainer_ID = str(trainer[0])
                break
        
        # Fetches ClassID
        for type_of_class in CLASSTYPES_WITH_ID_APPENDED:
            if type_of_class[1] == str(self.classType_entrybox.get()):
                self.class_ID = str(type_of_class[1])
                break

        # 1st Check - Checks if any entries are empty. 
        if self.session_ID or self.class_ID or self.trainer_ID or self.session_date or self.session_start_time or self.session_end_time or self.session_location != '':
            try:
                # 2nd Check - If SessionID is a positive integer
                self.session_ID = int(self.session_ID)

                # 3rd Check - If this SessionID already exists
                connection = sqlite3.connect('SystemDatabase.db')
                cursor_object = connection.cursor()
                cursor_object.execute('''SELECT SessionID FROM Sessions;''')
                session_id_results = cursor_object.fetchall()
                connection.close()
                for session_id in session_id_results:
                    if session_id != self.session_ID:
                        self.valid_entries_flag = True

                # 4th Check - If same data already exists
                connection = sqlite3.connect('SystemDatabase.db')
                cursor_object = connection.cursor()
                cursor_object.execute('''SELECT * FROM Sessions WHERE 
                                        SessionID LIKE ? AND ClassType LIKE ? AND TrainerID LIKE ? AND SessionDate LIKE ? AND SessionStartTime LIKE ? AND SessionFinishTime LIKE ? AND SessionLocation LIKE ?;''',
                                        (self.class_type, self.trainer_ID, self.session_date, self.session_start_time, self.session_end_time, self.session_location))
                new_session_id = cursor_object.fetchall()
                if new_session_id != []:
                    showerror(title = "Duplicate Session", message = "This session already exists!")
                
                # 5th Check - If a trainer is available during that session
                cursor_object.execute('''SELECT * FROM Sessions WHERE 
                                        TrainerID LIKE ? AND SessionDate LIKE ? AND SessionStartTime LIKE ? AND SessionFinishTime LIKE ?;''',
                                        (self.trainer_ID, self.session_date, self.session_start_time, self.session_end_time))
                clashing_sessions = cursor_object.fetchall()
                if clashing_sessions != []:
                    showerror(title = "Unavailable trainer", message = "The trainer that you have chosen is not available for this session!")
                connection.close()
                self.valid_entries_flag = True               
            except:
                showerror(title = "Invalid Session ID", message = "SessionID needs to be a positive integer!")
        else:
            showerror(title = "Empty entries", message = "All entries need to be filled!")

        if self.valid_entries_flag == True:
                    try:
                        connection = sqlite3.connect('SystemDatabase.db')
                        cursor_object = connection.cursor()
                        cursor_object.execute('''INSERT INTO Sessions(SessionID, ClassType, TrainerID, SessionDate, SessionStartTime, SessionFinishTime, SessionLocation) FROM Sessions VALUES(?, ?, ?, ?, ?, ?, ?);''', 
                                            (self.session_ID, self.class_type, self.trainer_ID, self.session_date, self.session_start_time, self.session_end_time, self.session_location))
                        cursor_object.execute('''SELECT SessionID FROM Sessions WHERE 
                                            ClassType LIKE ? AND TrainerID LIKE ? AND SessionDate LIKE ? AND SessionStartTime LIKE ? AND SessionFinishTime LIKE ? AND SessionLocation LIKE ?;''',
                                            (self.class_type, self.trainer_ID, self.session_date, self.session_start_time, self.session_end_time, self.session_location))
                        new_session_id = cursor_object.fetchall()
                        connection.close()
                        self.valid_entries_flag = False
                        self.valid_session_ID_flag = False
                        showinfo(title="New session created!", message=f"Success! The session was created successfully and has a Session ID of {new_session_id}")
                    except:
                        showerror(title="Error 404", message="Something went wrong!")
        


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
        self.session_date = str((self.sessionDate_dateEntry.get_date()).strftime("%d-%m-%Y"))
        for session_tuple in search_results_tuple:
            # if session_tuple[3] == self.session_date:
            #     print(session_tuple[3],"== ",self.session_date)
            # else:
            #     print(session_tuple[3],"!= ",self.session_date)
            for trainer in TRAINERS_WITH_ID_APPENDED:
                if session_tuple[2] == trainer[0]:
                    trainer_name = trainer[1]
            session_list.append((session_tuple[0], session_tuple[1], trainer_name, session_tuple[3], session_tuple[4], session_tuple[5], session_tuple[6]))
        for session in session_list:
            self.sessions_table.insert("", tk.END, values=session,)