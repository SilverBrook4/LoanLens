# database funcitonality

# create functions to access data from .db file

import sqlite3 as sql
import matplotlib


#creates a career a user wants and returns the career id
def insert_career(name):
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO career (career_name) VALUES (?)",
        (name,)
    )

    connection.commit()

    career_id = cursor.lastrowid

    connection.close()

    return career_id

def contribute_to_loan(loan_id, payment_amount):
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()
    cursor.execute(
        '''UPDATE loans SET amount_payed = amount_payed + ? WHERE loan_id = ?''',
        (payment_amount, loan_id)
    )
    connection.commit()
    connection.close()

#function that will insert a user to the database
#will return the user_id
def insert_user(name,email, career_id):
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()
    #retrieve email from kind
    
    #need to check if email exists through db
     #if not, create new user
    cursor.execute(
        '''SELECT user_id FROM user WHERE email = ?''',
        (email,)
    )

    same_email = cursor.fetchone()
    if same_email:
        print("email is already in use")
        connection.close()
        return None  # email already exists

    cursor.execute(
        '''INSERT into User (name, email, career_id) VALUES (?,?,?)''', 
    (name, email, career_id)
    )
    connection.commit()
    user_id = cursor.lastrowid
    connection.close()
    return user_id

#searches database if user is there returns id if it is there
def login_user(email):
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT user_id FROM users WHERE email = ?",
        (email,)
    )

    result = cursor.fetchone()
    connection.close()

    if result:
        return result[0]   # user_id
    else:
        return None



def get_user_id_by_email(email):
    """Return database user_id for the given email, or None."""
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM User WHERE email = ?", (email,))
    row = cursor.fetchone()
    connection.close()
    return row[0] if row else None


# Mason functions
#retrieves user info, returns a tuple of (user_id, name, email, h_pass, career_id)
def get_user(user_id):
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()
    cursor.execute(
        '''SELECT user_id, name, email, career_id
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

#creates a loan and adds it to db.
def create_loan(user_id, loan_name, min_payment, loan_type, late_fee, p_amount, IR, IT, term_length, amount_payed):
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()

    cursor.execute(
        '''INSERT into loans (user_id, loan_name, min_payment, type, late_fee, p_amount, IR, IT, term_length, amount_payed) VALUES (?,?,?,?,?,?,?,?,?,?)''', 
    (user_id, loan_name, min_payment, loan_type, late_fee, p_amount, IR, IT, term_length, amount_payed)
    )
    connection.commit()
    connection.close()

#deletes loan given its name and interest type.
def delete_loan(loan_name, IT):
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()

    cursor.execute(
        '''DELETE FROM loans WHERE loan_name= ? AND IT = ?''',
        (loan_name, IT)
    )

    connection.commit()
    connection.close()
    

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

#adds a goal to the db
def add_goal(user_id, completed, description, duration):
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()
    cursor.execute(
        '''INSERT into goal (user_id, completed, description, duration) VALUES (?,?,?,?)''',
        (user_id, completed,description,duration)
        )
    connection.commit()
    connection.close()

#deletes a goal
def delete_goal(goal_id):
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()

    cursor.execute(
        '''DELETE FROM goal WHERE goal_id = ?''',
        (goal_id,)
    )

    connection.commit()
    connection.close()


def update_goal_status(goal_id, new_status, user_id ):
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()

    cursor.execute(
        '''UPDATE goal SET completed = ? WHERE goal_id = ? AND user_id = ?''',
        (new_status, goal_id, user_id,)
    )

    connection.commit()
    connection.close()

def test():
    career_id = insert_career("Computer Science")

    user_id = insert_user(
        "Tyler",
        "tjsheeha@uvm.edu",
        career_id
    )

    user = get_user(user_id)

    print("Inserted user:", user)

    #creating functions to add jobs to a database.

    #adds a job to jobs table.
def add_job(job_title,description,salary, career_id):
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()
    cursor.execute(
    '''INSERT into Job (job_title, description, salary, career_id) VALUES (?,?,?,?)''',
    (job_title,description,salary, career_id)
    )
    connection.commit()
    connection.close()

#retrieves jobs given the career of the user
def retrieve_job__listings(user_id):
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()
    cursor.execute(
        '''
        SELECT j.*
        FROM Job j
        JOIN users u ON u.career_id = j.career_id
        WHERE u.user_id = ?
        ''',
        (user_id,)
    )

    jobs = cursor.fetchall()
    connection.close()
    return jobs

#test()
