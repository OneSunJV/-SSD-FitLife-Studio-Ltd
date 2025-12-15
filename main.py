from controllers.login_layout import LoginLayoutController
import tkinter as tk

global window

defaultSystemPage = 0

class Window():
    def __init__(self):          
        self.root = tk.Tk()
        self.root.title('Login Page')
        self.root.geometry('1280x720')
        self.root.resizable(False, False)
        self.defaultSystemPage = 0
        LoginLayoutController.load_login(self.root)

    def run_mainloop(self):
        self.root.mainloop()

        
root = Window()
root.run_mainloop()
