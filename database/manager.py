from peewee import *

class DatabaseManager:
    def __init__(self):
        self.db = SqliteDatabase('database.db')

    def create_tables(self):
        self.db.connect()
        #self.db.create_tables()
