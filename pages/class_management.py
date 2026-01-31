import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from tkcalendar import DateEntry
import sqlite3

TRAINERS = [""]
TRAINERS_WITH_ID_APPENDED = []
CLASSTYPES = [""]
CLASSTYPES_WITH_ID_APPENDED = []
TIMES = ["","09:00:00","09:30:00","10:00:00","10:30:00","11:00:00","11:30:00","12:00:00","12:30:00","13:00:00","13:30:00","14:00:00","14:30:00","15:00:00","15:30:00","16:00:00"]
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


        self.frame.columnconfigure(0, weight=1)

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
        # Defining treeview frame
        self.treeview_frame = ttk.Frame(self.frame)

        self.treeview_frame.rowconfigure(0, weight=1)
        self.treeview_frame.rowconfigure(1, weight=10)
        self.treeview_frame.columnconfigure(0, weight=1)

        self.treeview_frame.grid(column=0, row=1, padx=5, pady=5, sticky=tk.NSEW)

        # Defining title on top of treeview
        session_records_label = ttk.Label(self.treeview_frame, text="Studio session records", font=("Arial", 11, "bold"))
        session_records_label.grid(column=0, row=0, sticky=tk.NSEW, padx=400)

        # Defining actual treeview/table
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
    
#-----------------------------------------------------------------------------------------------------------------------#

    def disable_or_enable_date_filter(self):
        if self.date_filter_disabled_check.get() == True:
            self.sessionDate_dateEntry.config(state=["disabled"])
        else:
            self.sessionDate_dateEntry.config(state=['normal'])


    def get_parameters_from_entries(self, db_action):
        self.session_ID = str(self.sessionID_entrybox.get())
        self.class_type = ''
        self.trainer_ID = ''
        self.session_date = ''
        if self.date_filter_disabled_check.get() == False:
            self.session_date = str((self.sessionDate_dateEntry.get_date()).strftime("%d-%m-%Y"))
        self.session_start_time = str(self.sessionStartTime_combobox.get())
        self.session_end_time = str(self.sessionFinishTime_combobox.get())
        self.session_location = str(self.sessionLocation_combobox.get())

        for trainer in TRAINERS_WITH_ID_APPENDED:
            if trainer[1] == str(self.trainer_combobox.get()):
                self.trainer_ID = str(trainer[0])
                break
        
        if db_action == "search":
            self.class_type = str(self.classType_entrybox.get())
        elif db_action == "create" or "delete":
            for type_of_class in CLASSTYPES_WITH_ID_APPENDED:
                if type_of_class[1] == str(self.classType_entrybox.get()):
                    self.class_type = str(type_of_class[0])
                    break


    def search_sessions(self):
        self.get_parameters_from_entries("search")
        
        if self.session_ID and self.class_type and self.trainer_ID and self.session_date and self.session_start_time and self.session_end_time and self.session_location == '':
            self.refresh_treeview()
        else:
            try:
                # Deletes data currently in table so that its empty for the data to be inserted
                for row in self.sessions_table.get_children():
                    self.sessions_table.delete(row)
                # Applying an SQL value that tells SQL to find similar entries to the parameters entered by the user
                self.session_ID = '%' + self.session_ID + '%'
                self.class_type =  '%' + self.class_type + '%'
                self.trainer_ID =  '%' + self.trainer_ID + '%'
                self.session_date = '%' + self.session_date + '%'
                self.session_start_time =  '%' + self.session_start_time + '%'
                self.session_end_time =  '%' + self.session_end_time + '%'
                self.session_location = '%' + self.session_location + '%'
                # Parameters are plugged into an SQL SELECT command
                connection = sqlite3.connect('SystemDatabase.db')
                cursor_object = connection.cursor()
                cursor_object.execute('''SELECT SessionID, ClassType, TrainerID, SessionDate, SessionStartTime, SessionFinishTime, SessionLocation FROM Sessions 
                                    INNER JOIN Classes ON Sessions.ClassID = Classes.ClassID 
                                    WHERE SessionID LIKE ? AND ClassType LIKE ? AND TrainerID LIKE ? AND SessionDate LIKE ? AND SessionStartTime LIKE ? AND SessionFinishTime LIKE ? AND SessionLocation LIKE ? 
                                    GROUP BY SessionID, ClassType, TrainerID, SessionDate, SessionStartTime, SessionFinishTime, SessionLocation''', 
                                    (self.session_ID, self.class_type, self.trainer_ID, self.session_date, self.session_start_time, self.session_end_time, self.session_location,))
                # Fetches entries that meet the SQL SELECT statement
                search_results_tuple = cursor_object.fetchall()
                connection.close()
                # This lsit is created so it can store sessions with the Trainer's full name instead of the Trainer ID
                session_list = []
                trainer_name = ''
                # Goes through each tuple/entry and looks for the TrainerID and then replaces it with the Trainer's full name and adds all the details into a tuple that is appended to a new list
                for session_tuple in search_results_tuple:
                    for trainer in TRAINERS_WITH_ID_APPENDED:
                        if session_tuple[2] == trainer[0]:
                            trainer_name = trainer[1]
                    session_list.append((session_tuple[0], session_tuple[1], trainer_name, session_tuple[3], session_tuple[4], session_tuple[5], session_tuple[6]))
                # Goes through the list of sessions (the ones with the Trainer full name) and inserts each entry into the treeview/table
                for session in session_list:
                    self.sessions_table.insert("", tk.END, values=session,)
            except:
                showerror(title = "Error 404", message = "Something went wrong!")



    def create_session(self):
        self.get_parameters_from_entries("create")

        self.trainer_ID_integer = 0
        self.class_ID = 0
        self.empty_params_flag = 0
        self.valid_entries_flag = False
        self.valid_trainer_flag = False
        self.valid_class_type_flag = False
  
        # 1st Check - Validates if TrainerID is an integer
        try:
            self.trainer_ID_integer = int(self.trainer_ID)
            self.valid_trainer_flag = True
        except:
            showerror(title = "Invalid Trainer", message = "The trainer you have selected does not match any of the options in the dropdown!")

        # 2nd Check - Validates if ClassID is an integer
        try:
            self.class_ID = int(self.class_type)
            self.valid_class_type_flag = True
        except:
            showerror(title = "Invalid Trainer", message = "The class type you have selected does not match any of the options in the dropdown!")

        PARAMETERS = [self.session_ID, self.class_ID, self.trainer_ID_integer, self.session_date, self.session_start_time, self.session_end_time, self.session_location]

        # 3rd Check - Checks if any entries are empty. 
        for param in PARAMETERS:
            if param == '':
                self.empty_params_flag += 1

        if self.empty_params_flag == 0:
            if self.valid_trainer_flag == True and self.valid_class_type_flag == True:
                try:
                    # 4th Check - If SessionID is a positive integer
                    self.session_ID = int(self.session_ID)

                    # 5th Check - If this SessionID already exists
                    self.session_ID = str(self.session_ID)
                    connection = sqlite3.connect('SystemDatabase.db')
                    cursor_object = connection.cursor()
                    cursor_object.execute('''SELECT * FROM Sessions WHERE SessionID LIKE ?;''', (self.session_ID,))
                    session_id_results = cursor_object.fetchall()
                    connection.close()
                    self.session_ID = int(self.session_ID)
                    
                    if session_id_results == []:
                        # 6th Check - If same data already exists
                        connection = sqlite3.connect('SystemDatabase.db')
                        cursor_object = connection.cursor()
                        cursor_object.execute('''SELECT SessionID FROM Sessions WHERE 
                                            ClassID LIKE ? AND TrainerID LIKE ? AND SessionDate LIKE ? AND SessionStartTime LIKE ? AND SessionFinishTime LIKE ? AND SessionLocation LIKE ?;''',
                                            (self.class_ID, self.trainer_ID_integer, self.session_date, self.session_start_time, self.session_end_time, self.session_location,))
                        new_session_id = cursor_object.fetchall()

                        if new_session_id == []:
                            # 7th Check - If a trainer is available during that session
                            cursor_object.execute('''SELECT * FROM Sessions WHERE 
                                                    TrainerID LIKE ? AND SessionDate LIKE ? AND SessionStartTime LIKE ? AND SessionFinishTime LIKE ?;''',
                                                    (self.trainer_ID_integer, self.session_date, self.session_start_time, self.session_end_time,))
                            clashing_sessions = cursor_object.fetchall()
                            connection.close()
                            if clashing_sessions == []:
                                self.valid_entries_flag = True
                            else:
                                showerror(title = "Unavailable trainer", message = "The trainer that you have chosen is not available for this session!")
                        else:
                            showerror(title = "Duplicate Data", message = "A session with this data already exists!")
                    else:
                        showerror(title = "SessionID already exists", message = "A session with this SessionID already exists!")
                except:
                    showerror(title = "Invalid Session ID", message = "SessionID needs to be a positive integer!")            
        else:
            showerror(title = "Empty entries", message = "All entries need to be filled!")

        if self.valid_entries_flag == True:
            try:
                connection = sqlite3.connect('SystemDatabase.db')
                cursor_object = connection.cursor()
                cursor_object.execute('''INSERT INTO Sessions(SessionID, ClassID, TrainerID, SessionDate, SessionStartTime, SessionFinishTime, SessionLocation) VALUES(?, ?, ?, ?, ?, ?, ?);''', 
                                    (self.session_ID, self.class_ID, self.trainer_ID_integer, self.session_date, self.session_start_time, self.session_end_time, self.session_location))
                connection.commit()
                cursor_object.execute('''SELECT SessionID FROM Sessions WHERE 
                                    ClassID LIKE ? AND TrainerID LIKE ? AND SessionDate LIKE ? AND SessionStartTime LIKE ? AND SessionFinishTime LIKE ? AND SessionLocation LIKE ?;''',
                                    (self.class_ID, self.trainer_ID_integer, self.session_date, self.session_start_time, self.session_end_time, self.session_location,))
                newly_added_session_id = cursor_object.fetchall()
                connection.close()
                self.valid_entries_flag = False
                self.valid_session_ID_flag = False
                self.valid_trainer_flag = False
                self.valid_class_type_flag = False
                self.empty_params_flag = False
                showinfo(title="New session created!", message=f"Success! The session was created successfully and has a Session ID of {newly_added_session_id[0][0]}")
            except:
                showerror(title="Error 404", message="Something went wrong!")
        

    def delete_session(self):
        self.session_ID_integer = 0
        self.valid_session_ID_flag = False
        self.get_parameters_from_entries("delete")

        if self.session_ID and self.class_type and self.trainer_ID and self.session_date and self.session_start_time and self.session_end_time and self.session_location == '':
            self.refresh_treeview()    
        else:
            try:
                # Deletes data currently in table so that its empty for the data to be inserted
                for row in self.sessions_table.get_children():
                    self.sessions_table.delete(row)
                # Check if then entered sessionID is a number
                try:
                    self.session_ID_integer = int(self.session_ID)
                    self.valid_session_ID_flag = True
                except:
                    showerror(title="Invalid SessionID!", message="This SessionID is not valid!")
                if self.valid_session_ID_flag == True:
                    try:
                        connection = sqlite3.connect('SystemDatabase.db')
                        cursor_object = connection.cursor()
                        cursor_object.execute('''DELETE FROM Sessions WHERE SessionID = ?''', (self.session_ID_integer,))
                        connection.commit()
                        connection.close()
                        showinfo(title="Session deleted!", message=f"Success! The session was deleted!")
                    except:
                        showerror(title="Invalid SessionID!", message="This SessionID does not exist!")
            except:
                showerror(title = "Error 404", message = "Something went wrong!")
        
        


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