import tkinter as tk;
from tkinter import ttk

LARGEFONT =("Verdana", 35)

class DashboardPage:
    def __init__(self, frame):
        self.frame = frame;
        self.frame.grid_propagate(False)
        self.frame.grid_columnconfigure(0,weight=1)
        self.frame.grid_columnconfigure(1,weight=1)
        self.frame.grid_columnconfigure(2,weight=1)
        frame1 = tk.Frame(self.frame,bg="red",height=100,width=100)
        frame2 = tk.Frame(self.frame,bg="yellow",height=100,width=100)
        frame3 = tk.Frame(self.frame,bg="purple",height=100,width=100)

        frame1.grid(row=0,column=0)
        frame2.grid(row=0,column=1)
        frame3.grid(row=0,column=2)

        frame4 = tk.Frame(self.frame,bg="green",height=100,width=100)
        frame5 = tk.Frame(self.frame,bg="yellow",height=100,width=100)
        frame6 = tk.Frame(self.frame,bg="purple",height=100,width=100)

        frame4.place(anchor="e",relx=1)

        label = ttk.Label(self.frame, text="Dashboard")
        label.grid(row = 0, column = 0)

