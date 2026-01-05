import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

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
        self.member_list = self.setup_member_list()

        #Calls a function to define and configure a notebook and tabs for different member operations
        self.member_notebook = self.setup_notebook()
    
        #temporary subroutine to test with data
        self.add_data()

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
    def setup_member_list(self):
        members_listbox = tk.Listbox(self.frame, width=35, height=20, font=("Verdana", 15))
        members_listbox.place(x=530, y=85)

        members_listbox.bind("<<ListboxSelect>>", self.populate_member_details)
        
        #Creates and places a scrollbar for the listbox
        members_scroll = tk.Scrollbar(self.frame)
        members_scroll.place(x=972, y=85)
        #Configures the scrollbar to the listbox
        members_listbox.config(yscrollcommand = members_scroll.set)
        members_scroll.config(command = members_listbox.yview)
        
        return members_listbox

    #Function to define, configure and return a notebook of tabs for different member operations
    def setup_notebook(self):
        #Defines a style to be used for the notebook view
        style = ttk.Style()
        #Require a theme alternate to the default to manipulate background colour
        style.theme_use("clam")
        style.configure("TNotebook", background=self.bg_colour, borderwidth=0)
        #Creates a notebook within the page frame
        member_notebook = ttk.Notebook(self.frame, style="TNotebook")
        
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
        manage_member_tab = tk.Frame(member_notebook, background=self.bg_colour)

        edit_btn = tk.Button(manage_member_tab, name="edit_btn", text="Edit", font=self.button_font, command=self.edit_member)
        edit_btn.place(x=120, y=30)

        delete_btn = tk.Button(manage_member_tab, name="delete_btn", text="Delete", font=self.button_font, command=self.delete_member)
        delete_btn.place(x=270, y=30)

        return manage_member_tab
    
    #Function to define, configure and return the Add Member tab of the notebook
    def setup_add_tab(self, member_notebook):
        #Creates frame for tab
        add_member_tab = tk.Frame(member_notebook, background=self.bg_colour)

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
    

    def add_widgets(self, window, tab_name):

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
        if (tab_name == "find") or (tab_name == "filter"):
            id_lbl = ttk.Label(window, text="ID", style="MemberWidget.TLabel")
            id_lbl.place(x = x_position, y = y_position)
            id_txt = ttk.Entry(window, name="id_txt", font=widget_font)
            id_txt.place(x = x_position + x_gap, y = y_position)
            #Update y-position for next label & entry
            y_position += y_gap

        #First name label & entry
        first_name_lbl = ttk.Label(window, text="First Name", style="MemberWidget.TLabel")
        first_name_lbl.place(x = x_position, y = y_position)
        first_name_txt = ttk.Entry(window, name="first_name_txt", font=widget_font)
        first_name_txt.place(x = x_position + x_gap, y = y_position)

        #Last name label & entry
        last_name_lbl = ttk.Label(window, text="Last Name", style="MemberWidget.TLabel")
        last_name_lbl.place(x = x_position, y = y_position + (y_gap*1))
        last_name_txt = ttk.Entry(window, name="last_name_txt", font=widget_font)
        last_name_txt.place(x = x_position + x_gap, y= y_position + (y_gap*1))

        #Date of birth label & datepicker
        dob_lbl = ttk.Label(window, text="Date of Birth", style="MemberWidget.TLabel")
        dob_lbl.place(x = x_position, y = y_position + (y_gap*2))
        dob_dtp = DateEntry(window, name="dob_dtp", font=widget_font, date_pattern="dd-mm-yyyy", background="white", showweeknumbers=False)
        dob_dtp.place(x = x_position + x_gap + 105, y= y_position + (y_gap*2))

        #Email address label & entry
        email_lbl = ttk.Label(window, text="Email", style="MemberWidget.TLabel")
        email_lbl.place(x = x_position, y = y_position + (y_gap*3))
        email_txt = ttk.Entry(window, name="email_txt", font=widget_font)
        email_txt.place(x = x_position + x_gap, y= y_position + (y_gap*3))

        #Phone number label & entry
        phone_lbl = ttk.Label(window, text="Phone number", style="MemberWidget.TLabel")
        phone_lbl.place(x = x_position, y = y_position + (y_gap*4))
        phone_txt = ttk.Entry(window, name="phone_txt", font=widget_font)
        phone_txt.place(x = x_position + x_gap, y= y_position + (y_gap*4))

        #Membership type label & drop-down
        membership_lbl = ttk.Label(window, text="Membership", style="MemberWidget.TLabel")
        membership_lbl.place(x = x_position, y = y_position + (y_gap*5))
        membership_cmb = ttk.Combobox(window, name="membership_cmb", font=widget_font)
        membership_cmb.place(x = x_position + x_gap, y= y_position + (y_gap*5))

        #Next payment date label and datepicker
        next_payment_date_lbl = ttk.Label(window, text="Next Payment Date", style="MemberWidget.TLabel")
        next_payment_date_lbl.place(x = x_position, y = y_position + (y_gap*6))
        next_payment_date_dtp = DateEntry(window, name="next_payment_date_dtp", font=widget_font, date_pattern="dd-mm-yyyy", background="white", showweeknumbers=False)
        next_payment_date_dtp.place(x = x_position + x_gap + 105, y= y_position + (y_gap*6))

        #Selection statement to configure tab depending on if for the Add Member or Find Member tab - add_widgets() used commonly for both
        if tab_name == "add":
            #Button to save the details input in the above entries
            add_btn = tk.Button(window, name="add_btn", text="Add", font=self.button_font, command=lambda: self.add_member(
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
            save_btn = tk.Button(window, name="save_btn", text="Save", font=self.button_font, command=lambda: self.save_member_details(
            window,
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

            filter_btn = tk.Button(window, name="filter_btn", text="Filter", font=self.button_font, command=self.setup_filter_window)
            filter_btn.place(x=100, y=400)
        
        elif tab_name == "filter":
            #Apply button
            apply_btn = tk.Button(window, name="apply_btn", text="Apply", font=self.button_font, command=lambda: self.apply_filter(
            window,
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
            cancel_btn = tk.Button(window, name="cancel_btn", text="Cancel", font=self.button_font, command=window.destroy)
            cancel_btn.place(x=250, y=400)
    
    #Subroutine that allows the user to edit an existing member picked from the listbox
    def edit_member(self):
        member_selected = True
        #verifies that a member is selected
        try:
            index = self.member_list.curselection()[0]
        except IndexError:
            #displays a warning message if no member is selected
            messagebox.showwarning(title = "No Member Selected", message = "There is no member selected to edit.")
            member_selected = False

        if member_selected:
            #calls a function to get all member details of the selected member
            member = self.get_selected_member()

            #calls a subroutine to set up a new window for the user to edit member details
            self.setup_edit_window()

    #subroutine to create and display a window for the user to edit the currently selected member
    def setup_edit_window(self):
        edit_win = tk.Tk()
        edit_win.geometry("500x500")
        edit_win.title("Edit Member")
        edit_win.config(bg=self.bg_colour)
        #adds the necessary widgets to the window
        self.add_widgets(edit_win, "edit")

    #Subroutine that allows the user to delete an existing member picked from the listbox
    def delete_member(self):
        member_selected = True
        #verifies that a member is selected
        try:
            index = self.member_list.curselection()[0]
        except IndexError:
            #displays a warning message if no member is selected
            messagebox.showwarning(title = "No Member Selected", message = "There is no member selected to delete.")
            member_selected = False
        
        if member_selected:
            #checks that the user wants to delete the selected user
            member_name = self.member_list.get(index)
            delete_confirmed = messagebox.askokcancel(title = "Delete Member", message = f"Are you sure you want to delete {member_name}?")
            #if user confirms OK then user is deleted from database and listbox
            if delete_confirmed: 
                self.member_list.delete(index)

    #Subroutine to append the details entered in the Add New Member tab to the member database & listbox
    def add_member(self, first_name_txt, last_name_txt, dob_dtp, email_txt, phone_txt, membership_cmb, next_payment_date_dtp):
        #Gets the data input from each of the widgets
        first_name = first_name_txt.get()
        last_name = last_name_txt.get()
        dob = str(dob_dtp.get_date())
        email = email_txt.get()
        phone = phone_txt.get()
        membership_type = membership_cmb.get()
        next_payment_date = str(next_payment_date_dtp.get_date())

        #Converts the date picker outputs into SQL date formats - THIS DOES NOT WORK
        python_date = datetime.strptime(dob, "%Y-%m-%d").date()
        sql_dob = python_date.strftime("%Y-%m-%d")

        python_date = datetime.strptime(next_payment_date, "%Y-%m-%d").date()
        sql_next_payment_date = python_date.strftime("%Y-%m-%d")

        #self.member_list.insert(tk.END, f"{first_name} {last_name}")
        
        #Add all details to database
        #Connects to database
        connection = sqlite3.connect("SystemDatabase.db")
        #Defines cursor
        cursor = connection.cursor()
        #Inserts the values input into the database
        cursor.execute(f'''
            INSERT INTO Members(FirstName, LastName, DateOfBirth, EmailAddress, PhoneNumber, MembershipType, NextPaymentDate)
            VALUES ("{first_name}", "{last_name}", {sql_dob}, "{email}", "{phone}", {membership_type}, {sql_next_payment_date});
                       ''')
        connection.commit()
        connection.close()

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
    
    #Function that gets the details of the selected member from the list box and database and returns them as a dictionary
    def get_selected_member(self):
        try:
            #Gets the index of the selected list item
            index = self.member_list.curselection()[0]
            #Gets the names from the listbox at the selected index
            names = self.member_list.get(index)
        except IndexError:
            item = " "
        
        #Splits the list value into first & last names
        id = item.split(" ", 1)[0]

        if id != "":
            #Connects to database
            connection = sqlite3.connect("SystemDatabase.db")
            #Defines cursor
            cursor = connection.cursor()
            cursor.execute(f'''
                SELECT * FROM Members
                WHERE MemberID = {id};''')
            data = cursor.fetchall()
            print(data)
            cursor.close()
        else:
            first_name = ""
            last_name = ""

        #Creates a dictionary to store all details found about selected member
        selected_member = {
            "id" : id,
            "first_name" : first_name,
            "last_name" : last_name
            #All other member details
        }

        return selected_member
    
    #Subroutine that updates the value of affected widgets to reflect the selected list item in the find tab
    def set_widget_value(self, widget, new_value):
        #Gets the current state to determine what state the widget should be returned to after editing
        current_state = widget.state()
        #Remove excess states to avoid Tuple error on line 285 - widget.state([current_state])
        if "readonly" in current_state: current_state = "readonly"
        if "disabled" in current_state: current_state = "disabled"

        #Removes locked states, edits widget, returns to previous state
        widget.state(["!disabled", "!readonly"])
        widget.delete(0, tk.END)
        widget.insert(0, new_value)
        widget.state([current_state])

    #Main subroutine that deals with inserting values of a selected list item into relevant widgets
    def populate_member_details(self, event):
        #Calls a function to get the details of the selected member
        selected_member = self.get_selected_member()

        #Checks if member has been selected
        if selected_member:
            #Calls a subroutine to overwrite any existing data with the data of the selected member
            self.set_widget_value(self.member_notebook.children["find_member_tab"].children["first_name_txt"], selected_member["first_name"])
            self.set_widget_value(self.member_notebook.children["find_member_tab"].children["last_name_txt"], selected_member["last_name"])

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
        self.member_list.delete(0, tk.END)
        #needs code adding to check database and only display matching records
        filter_win.destroy()

    def add_data(self):
        self.member_list.insert(tk.END, "1  Thomas Creasey")
        self.member_list.insert(tk.END, "2  Jaison Varghese")
        self.member_list.insert(tk.END, "3  Hanif Uddin")
        self.member_list.insert(tk.END, "4  Jonathan Trivett")
        self.member_list.insert(tk.END, "5  Alex Legg")





