import tkinter as tk
from tkinter import ttk

#Page for member management - to include tabs for managing current members & adding new members
class MemberPage:
    def __init__(self, parent):
        self.bg_colour = "lightblue"
        # ------------------------------Member Frame----------------------------- #
        #Creates frame for the members page to house widgets
        self.frame = tk.Frame(parent, width=2000, height=4000, bg=self.bg_colour)

        # ------------------------------Title Label------------------------------ #
        #Calls a subroutine to create a title label widget
        self.title_init()

        # ------------------------------Notebook View---------------------------- #
        #Defines a style to be used for the notebook view
        style = ttk.Style()
        #Require a theme alternate to the default to manipulate background colour
        style.theme_use("clam")
        style.configure("TNotebook", background=self.bg_colour, borderwidth=0)
        #Creates a notebook within the page frame
        self.members_notebook = ttk.Notebook(self.frame, style="TNotebook")
        #Calls a subroutine to configure the notebook tabs
        self.tab_init()

        # ---------------------------------Listbox------------------------------- #
        #Creates and places a listbox to display existing member information to the right of the notebook view
        members_lsbx = tk.Listbox(self.frame, width=70, height=25)
        members_lsbx.place(x=530, y=100)
        
        #Creates and places a scrollbar for the listbox
        members_scrll = tk.Scrollbar(self.frame)
        members_scrll.place(x=953, y=100)
        #Configures the scrollbar to the listbox
        members_lsbx.config(yscrollcommand = members_scrll.set)
        members_scrll.config(command = members_lsbx.yview)

        #Populates listbox with test data
        for i in range(100):
            members_lsbx.insert(tk.END, i)

    def get_frame(self):
        return self.frame
    
    #Subroutine to create the page title label "Members"
    def title_init(self):
        #Declares a TTK Style
        style = ttk.Style()
        style.theme_use("clam")
        #Defines the characteristics of the TTK Style
        style.configure("MemberStyle.TLabel", background=self.bg_colour, foreground="black", font=("Verdana", 35))
        
        #Creates a label in the current frame with the configured style
        title_label = ttk.Label(self.frame, text="Members", style="MemberStyle.TLabel")
        #Places the label in the top-left of the frame
        title_label.place(x=0, y=0)

    #Subroutine to configure the tabs of the created notebook
    def tab_init(self):

        #Declares 2 tabs for the notebook - uses tk instead of ttk to facilitate design configuration
        manage_member_tab = tk.Frame(self.members_notebook, background=self.bg_colour)
        new_member_tab = tk.Frame(self.members_notebook, background=self.bg_colour)
        find_member_tab = tk.Frame(self.members_notebook, background=self.bg_colour)

        #Adds the tabs to the notebook
        self.members_notebook.add(manage_member_tab, text="Manage Members")
        self.members_notebook.add(new_member_tab, text="Add New Member")
        self.members_notebook.add(find_member_tab, text="Find Member")

        #Places the notebook and tabs
        self.members_notebook.place(x=0, y=60, width=500, height=3940)


