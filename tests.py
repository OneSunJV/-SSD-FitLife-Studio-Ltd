import unittest
import sqlite3
import bcrypt
from database.teardown import teardown
from database.create_database import create_database

from pages.login import validate_login_credentials


class TestLoginPage(unittest.TestCase):
    def setUp(self):
        create_database()

    def test_credential_validation_with_valid_credentials(self):
        # SETUP
        with sqlite3.connect('SystemDatabase.db') as connection:
            password = "TestPassword"
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            connection.execute('''INSERT INTO Employees
                                  (EmployeeID, Username, PasswordHash, FirstName, LastName, DateOfBirth, EmailAddress,
                                   PhoneNumber, JoinDate, EmployeeType)
                                  VALUES (9999, 'TestUser', ?, 'Test', 'User', '2000-01-01', 'test@gmail.com',
                                          '07000000000',
                                          '2026-01-26', 'ADMIN');''', (password_hash,))
            connection.commit()

        # EXECUTE
        (valid, _row) = validate_login_credentials("TestUser", "TestPassword")

        # VERIFY
        self.assertTrue(valid, "Expected login credentials to be valid")

    def test_credential_validation_with_invalid_credentials(self):
        # SETUP
        with sqlite3.connect('SystemDatabase.db') as connection:
            password = "TestPassword"
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            connection.execute('''INSERT INTO Employees
                                  (EmployeeID, Username, PasswordHash, FirstName, LastName, DateOfBirth, EmailAddress,
                                   PhoneNumber, JoinDate, EmployeeType)
                                  VALUES (9998, 'TestUser', ?, 'Test', 'User', '2000-01-01', 'test@gmail.com',
                                          '07000000000',
                                          '2026-01-26', 'ADMIN');''', (password_hash,))
            connection.commit()

        # EXECUTE
        (valid, _row) = validate_login_credentials("TestUser", "SomeInvalidPassword") # Note that in this case the correct password should be TestPassword

        # VERIFY
        self.assertFalse(valid, "Expected login credentials to be invalid")

    def tearDown(self):
        teardown()

if __name__ == "__main__":
    unittest.main()