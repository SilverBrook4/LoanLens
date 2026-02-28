# database funcitonality

# create functions to access data from .db file

import sqlite3 as sql
import matplotlib

#creates a career a user wants and returns the career id
def insert_career(name):
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO career (name) VALUES (?)",
        (name,)
    )

    connection.commit()

    career_id = cursor.lastrowid

    connection.close()

    return career_id

    
#function that will insert a user to the database
def insert_user(name,email, h_pass, career_id):
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()
    cursor.execute(
        '''INSERT into User (name, email, h_pass, career_id) VALUES (?,?,?,?)''', 
    (name, email, h_pass, career_id)
    )
    connection.commit()
    connection.close()

#searches database if user is there returns true if so
def login_user(email, h_pass):
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT 1 FROM users WHERE email = ? AND h_pass = ?",
        (email, h_pass)
    )

    result = cursor.fetchone()
    connection.close()

    return result is not None


# Mason functions
    
    #retrieves users goals
    #need a function to add goals
    #need a function to delete goals

# gets list of user task
def get_goals():
    pass
# End of masons functions
