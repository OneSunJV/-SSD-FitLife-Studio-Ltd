import tkinter as tk
from tkinter import ttk

LARGEFONT = ("Verdana", 35)

#Page for member management - to include tabs for managing current members & adding new members
class MemberPage:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, width=200, height=400, bg="lightblue")

        title_label = ttk.Label(self.frame, text="Members", font=LARGEFONT)
        title_label.grid(row=0, column=0, sticky="nw")

    def get_frame(self):
        return self.frame