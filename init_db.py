import sqlite3 as sql
import os

def init_db():
    # Ensure the database directory exists
    os.makedirs("database", exist_ok=True)
    
    connection = sql.connect("database/fintech.db")
    cursor = connection.cursor()

    # 1. Career Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "career" (
            "career_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "career_name" TEXT
        )
    ''')

    # 2. User Table
    # Note: Kinde users might not have a traditional hashed password,
    # so h_pass is kept nullable.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "User" (
            "user_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "name" TEXT,
            "h_pass" TEXT,
            "email" TEXT,
            "career_id" INTEGER,
            FOREIGN KEY("career_id") REFERENCES "career"("career_id")
        )
    ''')

    # 3. Job Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "Job" (
            "job_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "job_title" TEXT,
            "description" TEXT,
            "salary" NUMERIC,
            "career_id" INTEGER,
            FOREIGN KEY("career_id") REFERENCES "career"("career_id")
        )
    ''')

    # 4. Loans Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "loans" (
            "loan_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "user_id" INTEGER,
            "loan_name" TEXT,
            "min_payment" NUMERIC,
            "type" TEXT,
            "late_fee" NUMERIC,
            "p_amount" NUMERIC,
            "IR" NUMERIC,
            "IT" TEXT,
            "term_length" TEXT,
            "amount_payed" NUMERIC,
            FOREIGN KEY("user_id") REFERENCES "User"("user_id")
        )
    ''')

    # 5. Goal Table
    # user_id is kept as INTEGER to match your schema, but if you 
    # use Kinde IDs (strings) directly, consider changing this to TEXT.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "Goal" (
            "goal_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "user_id" INTEGER,
            "completed" INTEGER,
            "description" TEXT,
            "duration" TEXT,
            FOREIGN KEY("user_id") REFERENCES "User"("user_id")
        )
    ''')

    connection.commit()
    connection.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()