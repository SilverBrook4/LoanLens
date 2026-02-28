# databse funcitonality

# create functions to access data from .db file

import sqlite3 as sql
import matplotlib

# get all users 
def get_users():
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, username, email FROM users ORDER BY username")
    users = []
    for row in cursor.fetchall():
        users.append({"user_id": row[0], "username": row[1], "email": row[2]})
    connection.close()
    return users




# Mason functions

# gets list of user task
def get_goals():
    pass
# End of masons functions
