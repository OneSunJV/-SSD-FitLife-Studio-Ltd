import sqlite3

def teardown():
    connection = sqlite3.connect('SystemDatabase.db')
    cursor_object = connection.cursor()

    cursor_object.execute('DROP TABLE IF EXISTS Employees;')
    cursor_object.execute('DROP TABLE IF EXISTS Classes;')
    cursor_object.execute('DROP TABLE IF EXISTS SessionMemberPayments;')
    cursor_object.execute('DROP TABLE IF EXISTS MembershipTypes;')
    cursor_object.execute('DROP TABLE IF EXISTS Sessions;')
    cursor_object.execute('DROP TABLE IF EXISTS Equipment;')
    cursor_object.execute('DROP TABLE IF EXISTS Members;')
    cursor_object.execute('DROP TABLE IF EXISTS SessionAttendees;')
    cursor_object.execute('DROP TABLE IF EXISTS EquipmentMaintenanceCheckLogs;')
    cursor_object.execute('DROP TABLE IF EXISTS EquipmentTypes;')

    connection.commit()
    connection.close()

if __name__ == '__main__':
    teardown()