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

#searches database if user is there returns id if it is there
def login_user(email, h_pass):
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT user_id FROM users WHERE email = ? AND h_pass = ?",
        (email, h_pass)
    )

    result = cursor.fetchone()
    connection.close()

    if result:
        return result[0]   # user_id
    else:
        return None



# Mason functions
#retrieves user info, returns a tuple of (user_id, name, email, h_pass, career_id)
def get_user(user_id):
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()
    cursor.execute(
        '''SELECT user_id, name, email, h_pass, career_id
    FROM User
    WHERE user_id = ?
    ''',(user_id,)
    )
    user = cursor.fetchone()
    connection.close()

    return user

#returns a list of tuples where each tuple represents loan info
#loan tuple = (loan_id, user_id, loan_name, min_payment, type, late_fee, p_amount, IR, IT, term_length)
def get_loans(user_id):
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()
    cursor.execute(
        '''SELECT *
    FROM loans
    WHERE user_id = ?
    ''',(user_id,)
    )
    loans = cursor.fetchall()
    connection.close()

    return loans

    

#retrieves users goals, returns a list of tuples of each goal information.
def retrieve_goals(user_id):
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM Goal WHERE user_id = ?",
        (user_id,)
    )
    goals = cursor.fetchall()
    connection.close()

    return goals

#
def add_goals(user_id, completed, description, duration):
    pass



    #need a function to add goals
    #need a function to delete goals


# End of masons functions
