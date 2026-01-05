from pages import calendar
from pages import dashboard

global PAGES

PAGES = [
    { "displayName": "Calendar", "className": calendar.CalendarPage, "default": True },
    { "displayName": "Dashboard", "className": dashboard.FitLifeDashboard, "default": False }
]