import tkinter as tk;

class PageController:
    def __init__(self, container):
        self.container = container
        self.frames = [];        

    def register_page(self, pageClass):
        pagesFrame = tk.Frame(self.container, bg="blue", width=1000, height=660)
        pageClass(pagesFrame)
        self.frames.append(pagesFrame)
        pagesFrame.grid(row = 0, column = 0, sticky=tk.NSEW)

    def display_page(self, page):
        frame = self.frames[page]
        frame.tkraise()
    