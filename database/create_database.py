import sqlite3

print("-----------------------------------------------|")
print("Running database creation script...            |")
print("-----------------------------------------------|")
try:
     

     connection = sqlite3.connect('SystemDatabase.db')
     cursor_object = connection.cursor()
     cursor_object.execute('''CREATE TABLE IF NOT EXISTS Employees (
                         EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
                         Username TEXT NOT NULL,
                         PasswordHash TEXT NOT NULL,
                         FirstName TEXT NOT NULL,
                         MiddleNames TEXT,
                         LastName TEXT NOT NULL,
                         DateOfBirth DATE NOT NULL,
                         EmailAddress TEXT NOT NULL,
                         PhoneNumber INT NOT NULL,
                         JoinDate DATE NOT NULL,
                         LeftDate DATE,
                         EmployeeType TEXT NOT NULL
                    );''')

     cursor_object.execute('''CREATE TABLE IF NOT EXISTS Classes (
                         ClassID INTEGER PRIMARY KEY AUTOINCREMENT,
                         ClassType TEXT,
                         ClassDescription TEXT
                    );''')

     cursor_object.execute('''CREATE TABLE IF NOT EXISTS SessionMemberPayments (
                         SessionPaymentID INTEGER PRIMARY KEY AUTOINCREMENT,
                         MemberID INTEGER,
                         SessionID INTEGER,
                         PaymentScheme TEXT NOT NULL,
                         PaymentType TEXT NOT NULL,
                         PaymentLocation TEXT NOT NULL,
                         PaymentTime DATE NOT NULL,
                         PaymentDate DATE NOT NULL,
                         FOREIGN KEY (MemberID) REFERENCES Members (MemberID),
                         FOREIGN KEY (SessionID) REFERENCES Sessions (SessionID)
                    );''')

     cursor_object.execute('''CREATE TABLE IF NOT EXISTS MembershipTypes (
                         MembershipTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
                         MembershipDescription TEXT NOT NULL,
                         MembershipPricePerMonth INTEGER NOT NULL
                    );''')


     cursor_object.execute('''CREATE TABLE IF NOT EXISTS Sessions (
                         SessionID INTEGER PRIMARY KEY AUTOINCREMENT,
                         ClassID INTEGER,
                         TrainerID INTEGER,
                         SessionDate DATE,
                         SessionStartTime DATE,
                         SessionFinishTime DATE, 
                         SessionLocation TEXT,                  
                         FOREIGN KEY (ClassID) REFERENCES Classes (ClassID),
                         FOREIGN KEY (TrainerID) REFERENCES Employees (EmployeeID)
                    );''')
     
     

     cursor_object.execute('''CREATE TABLE IF NOT EXISTS Equipment (
                         EquipmentID INTEGER PRIMARY KEY AUTOINCREMENT,
                         EquipmentTypeID INTEGER,
                         RecentMaintenanceLogID INTEGER,
                         EquipmentStatus TEXT,
                         PurchaseDate DATE,
                         FOREIGN KEY (EquipmentTypeID) REFERENCES EquipmentTypes (EquipmentTypeID),
                         FOREIGN KEY (RecentMaintenanceLogID) REFERENCES EquipmentMaintenanceCheckLogs (EquipmentMaintenanceCheckLogID)
                    );''')

     cursor_object.execute('''CREATE TABLE IF NOT EXISTS Members (
                         MemberID INTEGER PRIMARY KEY AUTOINCREMENT,
                         FirstName TEXT NOT NULL,
                         LastName TEXT NOT NULL,
                         DateOfBirth DATE NOT NULL,
                         EmailAddress TEXT NOT NULL,
                         PhoneNumber TEXT NOT NULL,
                         MembershipType INTEGER,
                         NextPaymentDate DATE,
                         FOREIGN KEY (MembershipType) REFERENCES MembershipTypes (MembershipType)
                    );''')

     cursor_object.execute('''CREATE TABLE IF NOT EXISTS SessionAttendees (
                         SessionAttendeeID INTEGER PRIMARY KEY AUTOINCREMENT,
                         MemberID INTEGER,
                         SessionID INTEGER,
                         FOREIGN KEY (SessionID) REFERENCES Sessions (SessionID),
                         FOREIGN KEY (MemberID) REFERENCES Members (MemberID)
                    );''')

     cursor_object.execute('''CREATE TABLE IF NOT EXISTS EquipmentMaintenanceCheckLogs (
                         EquipmentMaintenanceCheckLogID INTEGER PRIMARY KEY AUTOINCREMENT,
                         EquipmentID INTEGER,
                         MaintenanceCheckNotes TEXT NOT NULL,
                         SafetyCheckResult TEXT NOT NULL,
                         ServicerName TEXT NOT NULL,
                         MaintenanceCompany TEXT NOT NULL,
                         CheckStartTime DATE NOT NULL,
                         CheckFinishTime DATE NOT NULL,
                         CheckDate DATE NOT NULL,
                         FOREIGN KEY (EquipmentID) REFERENCES Equipment (EquipmentID)
                    );''')

     cursor_object.execute('''CREATE TABLE IF NOT EXISTS EquipmentTypes (
                         EquipmentTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
                         EquipmentManufacturer TEXT NOT NULL,
                         EquipmentModel TEXT NOT NULL,
                         EquipmentSubModel TEXT NOT NULL
                    );''')
     

     connection.close()
     print("SUCCESS! Database has been created.            |")
     print("-----------------------------------------------|")
     print("The name of the database is 'SystemDatabase'.  |")
     print("The file extension is .db                      |")
     print("-----------------------------------------------|")
except:
     print("FAIL! Database could not be created.           |")
     print("-----------------------------------------------|")