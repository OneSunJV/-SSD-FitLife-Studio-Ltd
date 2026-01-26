import random
import sqlite3
from datetime import datetime, timedelta
from calendar import monthrange
import bcrypt

connection = sqlite3.connect('SystemDatabase.db')
cursor_object = connection.cursor()

password_hash = bcrypt.hashpw("12345".encode('utf-8'), bcrypt.gensalt())
connection.execute('''INSERT INTO Employees 
                        (EmployeeID, Username, PasswordHash, FirstName, LastName, DateOfBirth, EmailAddress, PhoneNumber, JoinDate, EmployeeType)  
                      VALUES 
                        (1, 'JohnDoe', ?, 'John', 'Doe', '2000-01-01', 'john@gmail.com', '07000000000', '2026-01-19', 'ADMIN');''', (password_hash,))

connection.execute('''INSERT INTO Employees 
                        (EmployeeID, Username, PasswordHash, FirstName, LastName, DateOfBirth, EmailAddress, PhoneNumber, JoinDate, EmployeeType)  
                      VALUES 
                        (2, 'Spiderman', ?, 'Peter', 'Parker', '2001-01-01', 'peter@gmail.com', '07100000000', '2026-01-19', 'TRAINER');''', (password_hash,))

connection.execute('''INSERT INTO Employees 
                        (EmployeeID, Username, PasswordHash, FirstName, LastName, DateOfBirth, EmailAddress, PhoneNumber, JoinDate, EmployeeType)  
                      VALUES 
                        (3, 'Batman', ?, 'Bruce', 'Wayne', '2002-01-01', 'bruce@gmail.com', '07200000000', '2026-01-19', 'TRAINER');''', (password_hash,))

connection.execute('''INSERT INTO Classes 
                   (ClassID, ClassType, ClassDescription)  
                   VALUES 
                   (1, 'Strength Training', 'Strength Training Description');''')

connection.execute('''INSERT INTO Classes 
                   (ClassID, ClassType, ClassDescription)  
                   VALUES 
                   (2, 'HIIT', 'HIIT Description');''')

connection.execute('''INSERT INTO Classes 
                   (ClassID, ClassType, ClassDescription)  
                   VALUES 
                   (3, 'Spin Class', 'Spin Class Description');''')

connection.execute('''INSERT INTO Classes 
                   (ClassID, ClassType, ClassDescription)  
                   VALUES 
                   (4, 'Dance Class', 'Dance Class Description');''')

connection.execute('''INSERT INTO Classes 
                   (ClassID, ClassType, ClassDescription)  
                   VALUES 
                   (5, 'Yoga', 'Yoga Description');''')


current_month = datetime.now().month
current_year = datetime.now().year

_, days_in_month = monthrange(current_year, current_month)

idx = 1
for day in range(1, days_in_month + 1):
    date_str = f'{current_year}-{current_month:02}-{day:02}'

    locations = ["Location A", "Location B", "Location C"]
    trainer_ids = [2,3]

    for i in range(0, random.randint(0,5)):
        class_id = random.randint(1, 5)

        start_time = datetime.now()
        finish_time = start_time + timedelta(hours=1)
        start_time = start_time.strftime("%H:%M:%S")
        finish_time = finish_time.strftime("%H:%M:%S")

        connection.execute(f'''INSERT INTO Sessions
                              (SessionID, ClassID, TrainerID, SessionStartTime, SessionFinishTime, SessionDate, SessionLocation)
                              VALUES ({idx}, {class_id}, {random.choice(trainer_ids)}, '{start_time}', '{finish_time}', '{datetime.now().strftime("%d-%m-%Y")}', '{random.choice(locations)}');''')

        idx += 1

connection.commit()
connection.close()