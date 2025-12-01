# ------------------------------Modules------------------------------ #
from layouts import system_layout # Applies the login ui layout for th
from layouts import login_layout 
import page_controller # Used to control pages
import tkinter as tk # Used to create the window
from pages import calendar
from pages import calendar2
from pages import members

# ------------------------------Variables----------------------------- #

PAGES = [
    { "displayName": "Calendar", "className": calendar.CalendarPage, "default": True },
    { "displayName": "Calendar2", "className": calendar2.Calendar2Page, "default": False },
    {"displayName": "Members", "className": members.MemberPage, "default": False}
]

defaultSystemPage = 0

bypassLoginPage = True


# ----------------------------Main Function--------------------------- #
if __name__=="__main__":
    root = tk.Tk()
    root.title('Login Page')
    root.geometry('1280x720')
    root.resizable(False, False)
    
    pageLayout = system_layout.SystemLayout(root) if bypassLoginPage else login_layout.LoginLayout(root)

    if bypassLoginPage:
        pageContainer = pageLayout.get_page_container();
        pageController = page_controller.PageController(pageContainer)
        pageLayout.create_sidebar_buttons(PAGES, pageController)
        for idx, page in enumerate(PAGES):
            pageController.register_page(page["className"])

            if page["default"] == True:
                pageController.display_page(idx)

        

    root.mainloop();
