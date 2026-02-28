# This is the Checklist class for the checklist on the users dashboard
import sqlite3

class Checklist:

    # checklist class constructor
    def __init__(self):

        self.task = []

        self.Get_Tasks_From_DB()


    def Connect_To_DB(self:)

        connection = sqlite3.connect() 


    def Get_Tasks_From_DB(self):

        pass
