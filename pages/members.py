import tkinter as tk
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
        #Calls a subroutine to configure the notebook tabs
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

        edit_btn = tk.Button(manage_member_tab, text="Edit", font=self.button_font, command=self.edit_member)
        edit_btn.place(x=120, y=30)

        delete_btn = tk.Button(manage_member_tab, text="Delete", font=self.button_font, command=self.delete_member)
        delete_btn.place(x=270, y=30)

        return manage_member_tab

    def setup_add_tab(self, member_notebook):
        add_member_tab = tk.Frame(member_notebook, background=self.bg_colour)

        #defines a ttk style used for all labels in this tab
        add_member_font = ("Verdana", 15)
        label_style = ttk.Style()
        label_style.theme_use("clam")
        label_style.configure("AddMember.TLabel", font=add_member_font, background=self.bg_colour)

        #defines values for widget positioning
        x_position = 20
        x_gap = 160
        y_position = 30
        y_gap = 40

        #First name label & entry
        first_name_lbl = ttk.Label(add_member_tab, text="First Name", style="AddMember.TLabel")
        first_name_lbl.place(x = x_position, y = y_position)
        first_name_txt = ttk.Entry(add_member_tab, font=add_member_font)
        first_name_txt.place(x = x_position + x_gap, y = y_position)

        #Last name label & entry
        last_name_lbl = ttk.Label(add_member_tab, text="Last Name", style="AddMember.TLabel")
        last_name_lbl.place(x = x_position, y = y_position + (y_gap*1))
        last_name_txt = ttk.Entry(add_member_tab, font=add_member_font)
        last_name_txt.place(x = x_position + x_gap, y= y_position + (y_gap*1))

        #Date of birth label & datepicker
        dob_lbl = ttk.Label(add_member_tab, text="Date of Birth", style="AddMember.TLabel")
        dob_lbl.place(x = x_position, y = y_position + (y_gap*2))
        dob_dtp = DateEntry(add_member_tab, font=add_member_font, date_pattern="dd-mm-yyyy", background="white", showweeknumbers=False)
        dob_dtp.place(x = x_position + x_gap + 105, y= y_position + (y_gap*2))

        #Email address label & entry
        email_lbl = ttk.Label(add_member_tab, text="Email", style="AddMember.TLabel")
        email_lbl.place(x = x_position, y = y_position + (y_gap*3))
        email_txt = ttk.Entry(add_member_tab, font=add_member_font)
        email_txt.place(x = x_position + x_gap, y= y_position + (y_gap*3))

        #Phone number label & entry
        phone_lbl = ttk.Label(add_member_tab, text="Phone number", style="AddMember.TLabel")
        phone_lbl.place(x = x_position, y = y_position + (y_gap*4))
        phone_txt = ttk.Entry(add_member_tab, font=add_member_font)
        phone_txt.place(x = x_position + x_gap, y= y_position + (y_gap*4))

        #Membership type label & drop-down
        membership_lbl = ttk.Label(add_member_tab, text="Membership", style="AddMember.TLabel")
        membership_lbl.place(x = x_position, y = y_position + (y_gap*5))
        membership_cmb = ttk.Combobox(add_member_tab, font=add_member_font)
        membership_cmb.place(x = x_position + x_gap, y= y_position + (y_gap*5))

        #Next payment date label and datepicker
        next_payment_date_lbl = ttk.Label(add_member_tab, text="Next Payment Date", style="AddMember.TLabel")
        next_payment_date_lbl.place(x = x_position, y = y_position + (y_gap*6))
        next_Payment_date_dtp = DateEntry(add_member_tab, font=add_member_font, date_pattern="dd-mm-yyyy", background="white", showweeknumbers=False)
        next_Payment_date_dtp.place(x = x_position + x_gap + 105, y= y_position + (y_gap*6))

        #Button to save the details input in the above entries
        add_btn = tk.Button(add_member_tab, text="Add", font=self.button_font, command=lambda: self.add_member(
            first_name_txt.get(), 
            last_name_txt.get(), 
            dob_dtp.get_date(),
            email_txt.get(),
            phone_txt.get(), 
            membership_cmb.get(),
            next_Payment_date_dtp.get_date()))
        
        add_btn.place(x=120, y=400)

        return add_member_tab
        
    def setup_find_tab(self, member_notebook):
        find_member_tab = tk.Frame(member_notebook, background=self.bg_colour)

        #Ability to select from list and view all member details
        #Ability to filter by different member details (reuse from add new member tab?)

        return find_member_tab
    
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
    def add_member(self, first_name, last_name, dob, email, phone, membership_type, next_payment_date):
        self.member_list.insert(tk.END, f"{first_name} {last_name}")
        
        #Add all details to database



