from pages import calendar
from pages import calendar2

global PAGES

PAGES = [
    { "displayName": "Calendar", "className": calendar.CalendarPage, "default": True },
    { "displayName": "Calendar2", "className": calendar2.Calendar2Page, "default": False }
]