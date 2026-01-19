import random
import sqlite3
from datetime import datetime, timedelta
from calendar import monthrange

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

    for i in range(0, random.randint(0,5)):
        class_id = random.randint(1, 5)

        start_hour = random.randint(0,23)
        start_time = datetime(current_year, current_month, day, start_hour).timestamp()
        finish_time = start_time + 1 * 60 * 60

        connection.execute(f'''INSERT INTO Sessions
                              (SessionID, ClassID, TrainerID, SessionStartTime, SessionFinishTime, SessionDate)
                              VALUES ({idx}, {class_id}, 1, '{start_time}', '{finish_time}', '{date_str}');''')

        idx += 1

connection.commit()
connection.close()