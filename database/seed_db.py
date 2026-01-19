import sqlite3

connection = sqlite3.connect('SystemDatabase.db')
cursor_object = connection.cursor()

connection.execute('''INSERT INTO Employees 
                        (EmployeeID, FirstName, LastName, DateOfBirth, EmailAddress, PhoneNumber, JoinDate, EmployeeType)  
                      VALUES 
                        (1, 'Thomas', 'Creasey', '2000-01-01', 'thomas@gmail.com', '07000000000', '2026-01-19', 'ADMIN');''')

connection.execute('''INSERT INTO Classes 
                   (ClassID, ClassType, ClassDescription)  
                   VALUES 
                   (1, 'Strength Training', 'Strength Training Description');''')

connection.execute('''INSERT INTO Sessions 
                        (SessionID, ClassID, TrainerID, SessionStartTime, SessionFinishTime, SessionDate)  
                      VALUES 
                        (1, 1, 1, '1769337000', '1769340600', '2026-01-25');''') # 2026-01-25 10:30-11:30

connection.commit()
connection.close()