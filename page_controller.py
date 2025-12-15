import tkinter as tk;

class PageController:
    def __init__(self, container):
        self.container = container
        self.frames = [];        

    def register_page(self, page_class):
        pages_frame = tk.Frame(self.container, bg="white", width=1000, height=660)
        page_class(pages_frame)
        self.frames.append(pages_frame)
        pages_frame.grid(row = 0, column = 0, sticky=tk.NSEW)
        pages_frame.grid_propagate(False)

    def display_page(self, page):
        frame = self.frames[page]
        frame.tkraise()
    