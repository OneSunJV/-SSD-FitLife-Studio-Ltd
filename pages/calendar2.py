import tkinter as tk;
from tkinter import ttk

LARGEFONT =("Verdana", 35)

class Calendar2Page:
    def __init__(self, frame):
        self.frame = frame;

        label = ttk.Label(self.frame, text="Calendar2")
        label.grid(row = 0, column = 0)

    def get_frame(self):
        return self.frame