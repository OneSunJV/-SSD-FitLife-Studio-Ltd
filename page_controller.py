import tkinter as tk;

class PageController:
    def __init__(self, container):
        self.container = container
        self.frames = [];        

    def register_page(self, pageClass):
        page = pageClass(self.container)
        frame = page.get_frame()
        self.frames.append(frame)
        frame.grid(row = 0, column = 0)

    def display_page(self, page):
        frame = self.frames[page]
        frame.tkraise()
    