import tkinter as tk;
from tkinter import ttk

LARGEFONT =("Verdana", 35)

class CalendarPage:
    def __init__(self, parent):
        self.frame = tk.Frame(parent);

        label = ttk.Label(self.frame, text="Calendar")
        label.grid(row = 0, column = 0)

    def get_frame(self):
        return self.frame