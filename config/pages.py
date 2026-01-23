from pages import calendar
from pages import dashboard
from pages import members
from pages import equipment_maintenance
from pages import class_management

global PAGES

PAGES = [
    { "displayName": "Calendar", "className": calendar.CalendarPage, "default": True },
    { "displayName": "Equipment Maintenance", "className": equipment_maintenance.EquipmentMaintenancePage, "default": False },
    { "displayName": "Dashboard", "className": dashboard.FitLifeDashboard, "default": False },
    { "displayName": "Calendar", "className": calendar.CalendarPage, "default": True },
    { "displayName": "Equipment Maintenance", "className": equipment_maintenance.EquipmentMaintenancePage, "default": False },
    { "displayName": "Members", "className": members.MemberPage, "default": False},
    { "displayName": "Class Management", "className": class_management.ClassManagementPage, "default": False}
]