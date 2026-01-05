from pages import calendar
from pages import dashboard
from pages import members

global PAGES

PAGES = [
    { "displayName": "Calendar", "className": calendar.CalendarPage, "default": True },
    { "displayName": "Dashboard", "className": dashboard.FitLifeDashboard, "default": False }
    { "displayName": "Members", "className": members.MemberPage, "default": False}
]