import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import re

#Page for member management - to include tabs for managing current members & adding new members
class MemberPage:
    def __init__(self, frame):
        self.bg_colour = "lightblue"
        self.button_font = ("Verdana", 20)

        #Creates frame for the members page to house widgets
        self.frame = frame
        self.frame.config(bg=self.bg_colour)

        #Calls a subroutine to create a title label widget
        self.setup_title()

        #Creates and places a listbox to display existing member information to the right of the notebook view
        self.member_table = self.setup_member_table()

        #Populates the members list box with the most up-to-date data
        self.update_member_table()

        #Calls a function to define and configure a notebook and tabs for different member operations
        self.member_notebook = self.setup_notebook()

    def get_frame(self):
        return self.frame
    
    #Subroutine to create the page title label "Members"
    def setup_title(self):
        #Declares a TTK Style
        style = ttk.Style()
        style.theme_use("clam")
        #Defines the characteristics of the TTK Style
        style.configure("MemberStyle.TLabel", background=self.bg_colour, foreground="black", font=("Verdana", 35))
        
        #Creates a label in the current frame with the configured style
        title_label = ttk.Label(self.frame, text="Members", style="MemberStyle.TLabel")
        #Places the label in the top-left of the frame
        title_label.place(x=0, y=0)

    #Function that defines, configures and returns a list box showing members
    def setup_member_table(self):

        #Define columns and treeview for table
        member_table_columns = ("Member_ID", "First_Name", "Last_Name")
        members_table = ttk.Treeview(self.frame, columns=member_table_columns, height=20)

        #Define column headings
        members_table.heading("Member_ID", text="ID")
        members_table.heading("First_Name", text="First Name")
        members_table.heading("Last_Name", text="Last Name")

        #Set column widths
        members_table.column("Member_ID", width=50)
        members_table.column("First_Name", width=100)
        members_table.column("Last_Name", width=100)

        #Places the table
        members_table.place(x=530, y=85)

        #Binds the selection of a table record to the self.populate_member_details subroutine to populate widgets with the details of the selected member
        members_table.bind("<<TreeviewSelect>>", self.treeview_item_selected)
        
        #Creates and places a scrollbar for the listbox
        members_scroll = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=members_table.yview)
        members_scroll.place(x=972, y=85)
        #Configures the scrollbar to the listbox
        members_table.config(yscroll = members_scroll.set)
        
        return members_table
    
    #Subroutine that updates the member list box with the most recent data    
    def update_member_table(self):
        #Deletes all records of the member table treeview
        self.member_table.delete(*self.member_table.get_children())

        #Connects to database
        connection = sqlite3.connect("SystemDatabase.db")
        #Defines cursor
        cursor = connection.cursor()
        #Gets the data from the Members table for the MemberID, FirstName and LastName columns and stores them in the data variable
        cursor.execute(f'''
                SELECT MemberID, FirstName, LastName 
                FROM Members;
                ''')
        data = cursor.fetchall()
        connection.commit()
        connection.close()

        #Iterates through each member found in the database and adds their MemberID, FirstName and LastName to the member listbox
        for member in data:
            self.member_table.insert("", tk.END, values=member)

    #Function to define, configure and return a notebook of tabs for different member operations
    def setup_notebook(self):
        #Defines a style to be used for the notebook view
        style = ttk.Style()
        #Require a theme alternate to the default to manipulate background colour
        style.theme_use("clam")
        style.configure("TNotebook", background=self.bg_colour, borderwidth=0)
        #Creates a notebook within the page frame
        member_notebook = ttk.Notebook(self.frame, name="member_notebook", style="TNotebook")
        
        self.setup_tabs(member_notebook)

        return member_notebook

    #Subroutine to configure the tabs of the created notebook
    def setup_tabs(self, member_notebook):

        #Calls functions to declare and configure 3 tabs for the notebook - uses tk instead of ttk to facilitate design configuration
        manage_member_tab = self.setup_manage_tab(member_notebook)
        add_member_tab = self.setup_add_tab(member_notebook)
        find_member_tab = self.setup_find_tab(member_notebook)

        #Adds the tabs to the notebook
        member_notebook.add(manage_member_tab, text="Manage Members")
        member_notebook.add(add_member_tab, text="Add New Member")
        member_notebook.add(find_member_tab, text="Find Member")

        #Places the notebook and tabs
        member_notebook.place(x=0, y=60, width=500, height=3940)

    #Function to define, configure and return the Manage Member tab of the notebook
    def setup_manage_tab(self, member_notebook):
        manage_member_tab = tk.Frame(member_notebook, name = "manage_member_tab", background=self.bg_colour)

        edit_btn = tk.Button(manage_member_tab, name="edit_btn", text="Edit", font=self.button_font, command=self.setup_edit_window)
        edit_btn.place(x=120, y=30)

        delete_btn = tk.Button(manage_member_tab, name="delete_btn", text="Delete", font=self.button_font, command=self.delete_member)
        delete_btn.place(x=270, y=30)

        return manage_member_tab
    
    #Function to define, configure and return the Add Member tab of the notebook
    def setup_add_tab(self, member_notebook):
        #Creates frame for tab
        add_member_tab = tk.Frame(member_notebook, name="add_member_tab", background=self.bg_colour)

        #Passes frame into subroutine to configure widgets
        self.add_widgets(add_member_tab, "add")

        return add_member_tab
    
    #Function to define, configure and return the Find Member tab of the notebook
    def setup_find_tab(self, member_notebook):
        #Creates frame for tab
        find_member_tab = tk.Frame(member_notebook, name="find_member_tab", background=self.bg_colour)

        #Passes frame into subroutine to configure widgets
        self.add_widgets(find_member_tab, "find")

        #Ability to select from list and view all member details
        #Ability to filter by different member details (reuse from add new member tab?)

        return find_member_tab
    

    def add_widgets(self, frame, tab_name):

        #defines a ttk style used for all labels in this tab
        widget_font = ("Verdana", 15)
        label_style = ttk.Style()
        label_style.theme_use("clam")
        label_style.configure("MemberWidget.TLabel", font=widget_font, background=self.bg_colour)

        #defines values for widget positioning
        x_position = 20
        x_gap = 160
        y_position = 30
        y_gap = 40

        #ID label & entry
        if (tab_name == "find") or (tab_name == "filter") or (tab_name == "edit"):
            id_lbl = ttk.Label(frame, text="ID", style="MemberWidget.TLabel")
            id_lbl.place(x = x_position, y = y_position)
            id_txt = ttk.Entry(frame, name="id_txt", font=widget_font)
            if tab_name == "edit": id_txt.state(["disabled"])
            id_txt.place(x = x_position + x_gap, y = y_position)
            #Update y-position for next label & entry
            y_position += y_gap

        #First name label & entry
        first_name_lbl = ttk.Label(frame, text="First Name", style="MemberWidget.TLabel")
        first_name_lbl.place(x = x_position, y = y_position)
        first_name_txt = ttk.Entry(frame, name="first_name_txt", font=widget_font)
        first_name_txt.place(x = x_position + x_gap, y = y_position)

        #Last name label & entry
        last_name_lbl = ttk.Label(frame, text="Last Name", style="MemberWidget.TLabel")
        last_name_lbl.place(x = x_position, y = y_position + (y_gap*1))
        last_name_txt = ttk.Entry(frame, name="last_name_txt", font=widget_font)
        last_name_txt.place(x = x_position + x_gap, y= y_position + (y_gap*1))

        #Date of birth label & datepicker
        dob_lbl = ttk.Label(frame, text="Date of Birth", style="MemberWidget.TLabel")
        dob_lbl.place(x = x_position, y = y_position + (y_gap*2))
        dob_dtp = DateEntry(frame, font=widget_font, date_pattern="dd-mm-yyyy", background="white", showweeknumbers=False)
        dob_dtp.place(x = x_position + x_gap + 105, y= y_position + (y_gap*2))

        #Email address label & entry
        email_lbl = ttk.Label(frame, text="Email", style="MemberWidget.TLabel")
        email_lbl.place(x = x_position, y = y_position + (y_gap*3))
        email_txt = ttk.Entry(frame, name="email_txt", font=widget_font)
        email_txt.place(x = x_position + x_gap, y= y_position + (y_gap*3))

        #Phone number label & entry
        phone_lbl = ttk.Label(frame, text="Phone number", style="MemberWidget.TLabel")
        phone_lbl.place(x = x_position, y = y_position + (y_gap*4))
        phone_txt = ttk.Entry(frame, name="phone_txt", font=widget_font)
        phone_txt.place(x = x_position + x_gap, y= y_position + (y_gap*4))

        #Membership type label & drop-down
        membership_lbl = ttk.Label(frame, text="Membership", style="MemberWidget.TLabel")
        membership_lbl.place(x = x_position, y = y_position + (y_gap*5))
        membership_cmb = ttk.Combobox(frame, name="membership_cmb", font=widget_font)
        membership_cmb.place(x = x_position + x_gap, y= y_position + (y_gap*5))
        membership_cmb["values"] = [1, 2, 3] #Adds integer values corresponding to the membership type
        membership_cmb.state(["readonly"]) #Ensures the user can't type in the box, only use the selections

        #Next payment date label and datepicker
        next_payment_date_lbl = ttk.Label(frame, text="Next Payment Date", style="MemberWidget.TLabel")
        next_payment_date_lbl.place(x = x_position, y = y_position + (y_gap*6))
        next_payment_date_dtp = DateEntry(frame, font=widget_font, date_pattern="dd-mm-yyyy", background="white", showweeknumbers=False)
        next_payment_date_dtp.place(x = x_position + x_gap + 105, y= y_position + (y_gap*6))

        #Selection statement to configure tab depending on if for the Add Member or Find Member tab - add_widgets() used commonly for both
        if tab_name == "add":
            #Button to save the details input in the above entries
            add_btn = tk.Button(frame, name="add_btn", text="Add", font=self.button_font, command=lambda: self.add_member(
                first_name_txt, 
                last_name_txt, 
                dob_dtp,
                email_txt,
                phone_txt, 
                membership_cmb,
                next_payment_date_dtp))
        
            add_btn.place(x=120, y=400)
        
        elif tab_name == "edit":
            #Save button
            save_btn = tk.Button(frame, name="save_btn", text="Save", font=self.button_font, command=lambda: self.save_member(
            frame,
            id_txt.get(),
            first_name_txt.get(), 
            last_name_txt.get(), 
            dob_dtp.get_date(),
            email_txt.get(),
            phone_txt.get(), 
            membership_cmb.get(),
            next_payment_date_dtp.get_date()
            ))
            save_btn.place(x=120, y=400)
        
        elif tab_name == "find":
            #sets all widgets to be readonly and disables date pickers and combo box in the Find Member tab
            id_txt.state(["readonly"])
            first_name_txt.state(["readonly"])
            last_name_txt.state(["readonly"])
            dob_dtp.state(["disabled"])
            email_txt.state(["readonly"])
            phone_txt.state(["readonly"])
            membership_cmb.state(["disabled"])
            next_payment_date_dtp.state(["disabled"])

            filter_btn = tk.Button(frame, name="filter_btn", text="Filter", font=self.button_font, command=self.setup_filter_window)
            filter_btn.place(x=100, y=400)
        
        elif tab_name == "filter":
            #Apply button
            apply_btn = tk.Button(frame, name="apply_btn", text="Apply", font=self.button_font, command=lambda: self.apply_filter(
            frame,
            id_txt.get(),
            first_name_txt.get(), 
            last_name_txt.get(), 
            dob_dtp.get_date(),
            email_txt.get(),
            phone_txt.get(), 
            membership_cmb.get(),
            next_payment_date_dtp.get_date()
            ))
            apply_btn.place(x=120, y=400)

        #Adds a cancel button to both edit and filter pages
        if (tab_name == "edit") or (tab_name == "filter"):
            #Cancel button
            cancel_btn = tk.Button(frame, name="cancel_btn", text="Cancel", font=self.button_font, command=frame.destroy)
            cancel_btn.place(x=250, y=400)

    #Subroutine to create and display a window for the user to edit the currently selected member
    def setup_edit_window(self):
        #Calls a function to get all member details of the selected member
        selected_member = self.get_selected_member()

        if selected_member:
            #Defines a new modal window
            edit_win = tk.Tk()
            edit_win.geometry("500x500")
            edit_win.title("Edit Member")
            edit_win.config(bg=self.bg_colour)


            #Adds the necessary widgets to the window
            self.add_widgets(edit_win, "edit")
            self.populate_member_details(edit_win, "")

    #Subroutine to update the values of the selected member in the database upon clicking the Save button
    def save_member(self, frame, id, first_name, last_name, dob, email, phone, membership_type, next_payment_date):
        #Connects to database
        connection = sqlite3.connect("SystemDatabase.db")
        #Defines cursor
        cursor = connection.cursor()
        #Inserts the values input into the database
        cursor.execute(f'''
                UPDATE Members
                SET FirstName = "{first_name}",
                    LastName = "{last_name}",
                    DateOfBirth = {dob},
                    EmailAddress = "{email}",
                    PhoneNumber = "{phone}",
                    MembershipType = {membership_type},
                    NextPaymentDate = {next_payment_date}
                WHERE MemberID="{id}";
                ''')
        connection.commit()
        connection.close()
        #Updates the member table treeview
        self.update_member_table()
        messagebox.showinfo(title="Member Saved", message=f"{first_name} {last_name} has been edited and saved successfully.")
        #Closes the edit window
        frame.destroy()

    #Subroutine that allows the user to delete an existing member picked from the listbox
    def delete_member(self):
        #checks that the user wants to delete the selected user
        selected_member = self.get_selected_member()
        delete_confirmed = messagebox.askokcancel(title = "Delete Member", message = f"Are you sure you want to delete {selected_member["first_name"]} {selected_member["last_name"]}?")
        #if user confirms OK then user is deleted from database and listbox
        if selected_member and delete_confirmed: 
            #Connects to database
            connection = sqlite3.connect("SystemDatabase.db")
            #Defines cursor
            cursor = connection.cursor()
            #Inserts the values input into the database
            cursor.execute(f'''
                    DELETE FROM Members
                    WHERE MemberID="{selected_member["id"]}";
                    ''')
            connection.commit()
            connection.close()

            self.update_member_table()

    #Subroutine to append the details entered in the Add New Member tab to the member database & listbox
    def add_member(self, first_name_txt, last_name_txt, dob_dtp, email_txt, phone_txt, membership_cmb, next_payment_date_dtp):
        #Gets the data input from each of the widgets
        first_name = first_name_txt.get()
        last_name = last_name_txt.get()
        dob = dob_dtp.get_date()
        email = email_txt.get()
        phone = phone_txt.get()
        membership_type = membership_cmb.get()
        next_payment_date = next_payment_date_dtp.get_date()

        #Calls a function that validates the data entered in each of the entry widgets
        data_valid = self.validate_entries(first_name, last_name, dob, email, phone, membership_type, next_payment_date)

        if data_valid:
            #Adds all details to database
            #Connects to database
            connection = sqlite3.connect("SystemDatabase.db")
            #Defines cursor
            cursor = connection.cursor()
            #Inserts the values input into the database
            cursor.execute(f'''
                    INSERT INTO Members(FirstName, LastName, DateOfBirth, EmailAddress, PhoneNumber, MembershipType, NextPaymentDate)
                    VALUES ("{first_name}", "{last_name}", {dob}, "{email}", "{phone}", {membership_type}, {next_payment_date});
                    ''')
            connection.commit()
            connection.close()

            #Updates the member table treeview with the updated database contents
            self.update_member_table()

            #Displays an info message to confirm the member has been added to the database
            messagebox.showinfo(title="Member Added", message= f"{first_name} {last_name} added successfully.")

            #Clears the contents of each of the Add Member widgets
            first_name_txt.delete(0, tk.END)
            last_name_txt.delete(0, tk.END)
            dob_dtp.delete(0, tk.END)
            email_txt.delete(0, tk.END)
            phone_txt.delete(0, tk.END)
            membership_cmb.delete(0, tk.END)
            next_payment_date_dtp.delete(0, tk.END)
    
    #Function that checks all date entered is valid, returns True/False accordingly and throws pop-up messages
    def validate_entries(self, first_name, last_name, dob, email, phone, membership_type, next_payment_date):
        data_valid = True

        #Gets the current datetime and converts it to date format
        date_now = datetime.now().date()
        #Compiles a valid RegEx pattern to check the input email against
        valid_email_format = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
        #Checks if the values entered are valid and displays an pop-up message if not
        if first_name == "" or last_name == "" or email == "" or phone == "" or membership_type == "":
            messagebox.showwarning(title="Missing Data", message="Please ensure all fields are populated with data.")
            data_valid = False
        elif re.match(valid_email_format, email) is None:
            messagebox.showerror(title="Invalid Email", message=f"Email {email} is invalid. Please enter an email in a valid format and try again.")
            data_valid = False
        elif len(phone) != 11 or phone.isdecimal() == False:
            messagebox.showerror(title="Invalid Phone Number", message=f"Phone number {phone} is invalid. Please enter an 11-digit phone number and try again.")
            data_valid = False
        elif dob > date_now:
            messagebox.showerror(title="Invalid Date of Birth", message=f"Date of birth {str(dob)} is invalid. Please enter a date of birth in the past and try again.")
            data_valid = False
        elif next_payment_date < date_now:
            messagebox.showerror(title="Invalid Payment Date", message=f"Next payment date {str(next_payment_date)} is invalid. Please enter a payment date in the future and try again.")
            data_valid = False
        
        return data_valid

    #Function that gets the details of the selected member from the list box and database and returns them as a dictionary
    def get_selected_member(self):
        is_member_selected = True
        try:
            #Gets the index of the selected list item
            selected_member = self.member_table.selection()
            #Gets the names from the listbox at the selected index
            selected_member_index = selected_member[0]
            member = self.member_table.item(selected_member_index, "values")
        except IndexError:
            is_member_selected = False

            messagebox.showwarning(title = "No Member Selected", message = "There is no member selected.")

        if is_member_selected:
            #Connects to database
            connection = sqlite3.connect("SystemDatabase.db")
            #Defines cursor
            cursor = connection.cursor()
            cursor.execute(f'''
                SELECT * FROM Members
                WHERE MemberID = {member[0]};''')
            data = cursor.fetchall()
            cursor.close()
        else:
            return None

        #Creates a dictionary to store all details found about selected member
        selected_member = {
            "id" : data[0][0],
            "first_name" : data[0][1],
            "last_name" : data[0][2],
            "dob" : data[0][3],
            "email": data[0][4],
            "phone": data[0][5],
            "membership_type": data[0][6],
            "next_payment_date": data[0][7]
        }

        return selected_member
    
    #Subroutine that updates the value of affected widgets to reflect the selected list item in the find tab
    def set_widget_value(self, widget, new_value):
        #Gets the current state to determine what state the widget should be returned to after editing
        current_state = widget.state()
        #Remove excess states to avoid Tuple error on line 285 - widget.state([current_state])
        ignore_state = False
        if "readonly" in current_state: 
            current_state = "readonly"
        elif "disabled" in current_state: 
            current_state = "disabled"
        else:
            ignore_state = True #In this case, widget state has not been set so is read/write

        #Removes locked states, edits widget, returns to previous state
        widget.state(["!disabled", "!readonly"])
        widget.delete(0, tk.END)
        widget.insert(0, new_value)
        if ignore_state == False: widget.state([current_state]) #Only if the widget had a state before does it need to be set back

    #Subroutine called when an item in the treeview is selected
    def treeview_item_selected(self, event):
        self.populate_member_details(self.frame, "member_notebook.find_member_tab")

    #Main subroutine that deals with inserting values of a selected list item into relevant widgets
    def populate_member_details(self, window, frame):
        #Determines which tab is currently selected, if not the Find Member Tab then does not populate details as will not be seen anyway
        current_tab = self.member_notebook.select()
        #Checks if the current tab is the Find Member Tab or if the frame corresponds to the Edit Window - only in these cases are there widgets to populate
        if "find_member_tab" in current_tab or frame == "":
            #Calls a function to get the details of the selected member
            selected_member = self.get_selected_member()

            #Checks if member has been selected
            if selected_member:
                #Calls a subroutine to overwrite any existing data in the widgets with the data of the selected member in the specified window and frame
                self.set_widget_value(window.nametowidget(f"{frame}.id_txt"), selected_member["id"])
                self.set_widget_value(window.nametowidget(f"{frame}.first_name_txt"), selected_member["first_name"])
                self.set_widget_value(window.nametowidget(f"{frame}.last_name_txt"), selected_member["last_name"])
                self.set_widget_value(window.nametowidget(f"{frame}.!dateentry"), selected_member["dob"])
                self.set_widget_value(window.nametowidget(f"{frame}.email_txt"), selected_member["email"])
                self.set_widget_value(window.nametowidget(f"{frame}.phone_txt"), selected_member["phone"])
                self.set_widget_value(window.nametowidget(f"{frame}.membership_cmb"), selected_member["membership_type"])
                self.set_widget_value(window.nametowidget(f"{frame}.!dateentry2"), selected_member["next_payment_date"])

    #Subroutine to create, configure and display a window where the user can input data to filter by
    def setup_filter_window(self):
        filter_win = tk.Tk()
        filter_win.geometry("500x500")
        filter_win.title("Filter")
        filter_win.config(bg=self.bg_colour)

        self.add_widgets(filter_win, "filter")

        filter_win.mainloop()
    
    #Subroutine to apply the filters input by the user - called by pressing Apply button
    def apply_filter(self, filter_win, id, first_name, last_name, dob, email, phone, membership, next_payment_date):
        self.member_table.delete(0, tk.END)
        #needs code adding to check database and only display matching records
        filter_win.destroy()




