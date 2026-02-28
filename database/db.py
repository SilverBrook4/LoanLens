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

# Mason functions


# End of masons functions
