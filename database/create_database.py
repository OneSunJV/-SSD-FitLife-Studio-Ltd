import sqlite3

connection = sqlite3.connect('SystemDatabase.db')
cursor_object = connection.cursor()
connection.execute('''CREATE TABLE IF NOT EXISTS Employees (
                        EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
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

connection.execute('''CREATE TABLE IF NOT EXISTS Classes (
                        ClassID INTEGER PRIMARY KEY AUTOINCREMENT,
                        ClassType TEXT,
                        ClassDescription TEXT
                   );''')

connection.execute('''CREATE TABLE IF NOT EXISTS SessionMemberPayments (
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

connection.execute('''CREATE TABLE IF NOT EXISTS MembershipTypes (
                        MembershipTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
                        MembershipDescription TEXT NOT NULL,
                        MembershipPricePerMonth INTEGER NOT NULL
                   );''')


connection.execute('''CREATE TABLE IF NOT EXISTS Sessions (
                        SessionID INTEGER PRIMARY KEY AUTOINCREMENT,
                        ClassID INTEGER,
                        TrainerID INTEGER,
                        SessionStartTime DATE,
                        SessionFinishTime DATE,
                        SessionDate DATE,
                        FOREIGN KEY (ClassID) REFERENCES Classes (ClassID),
                        FOREIGN KEY (TrainerID) REFERENCES Employees (EmployeeID)
                   );''')

connection.execute('''CREATE TABLE IF NOT EXISTS Equipment (
                        EquipmentID INTEGER PRIMARY KEY AUTOINCREMENT,
                        EquipmentTypeID INTEGER,
                        RecentMaintenanceLogID INTEGER,
                        EquipmentStatus TEXT,
                        PurchaseDate DATE,
                        FOREIGN KEY (EquipmentTypeID) REFERENCES EquipmentTypes (EquipmentTypeID),
                        FOREIGN KEY (RecentMaintenanceLogID) REFERENCES EquipmentMaintenanceCheckLogs (EquipmentMaintenanceCheckLogID)
                   );''')

connection.execute('''CREATE TABLE IF NOT EXISTS Members (
                        MemberID INTEGER PRIMARY KEY AUTOINCREMENT,
                        FirstName TEXT NOT NULL,
                        LastName TEXT NOT NULL,
                        DateOfBirth DATE NOT NULL,
                        EmailAddress TEXT NOT NULL,
                        PhoneNumber INTEGER NOT NULL,
                        MembershipType INTEGER,
                        NextPaymentDate DATE,
                        FOREIGN KEY (MembershipType) REFERENCES MembershipTypes (MembershipType)
                   );''')

connection.execute('''CREATE TABLE IF NOT EXISTS FitnessWatchLogs (
                        FitnessWatchLogID INTEGER PRIMARY KEY AUTOINCREMENT,
                        SessionID INTEGER,
                        MemberID INTEGER,
                        CaloriesBurnt INTEGER,
                        AverageHeartRate INTEGER,
                        MaximumHeartRate INTEGER,
                        MinimumHeartRate INTEGER,
                        FOREIGN KEY (SessionID) REFERENCES Sessions (SessionID),
                        FOREIGN KEY (MemberID) REFERENCES Members (MemberID)
                   );''')

connection.execute('''CREATE TABLE IF NOT EXISTS EquipmentMaintenanceCheckLogs (
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

connection.execute('''CREATE TABLE IF NOT EXISTS EquipmentTypes (
                        EquipmentTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
                        EquipmentManufacturer TEXT NOT NULL,
                        EquipmentModel TEXT NOT NULL,
                        EquipmentSubModel TEXT NOT NULL
                   );''')

connection.close()