# This is the Checklist class for the checklist on the users dashboard
import goal
import sys
import os
# import database files
sys.path.append(os.path.join(os.path.dirname(__file__)), 'database')
import db

class Checklist:

    # checklist class constructor
    def __init__(self, user):

        self.user = user
        self.goals = []

        self.Get_Goals_From_DB()


    def Get_Goals_From_DB(self):

        # get user goals fro database
        goals_db = db.get_goals(user)

        # cycle through all goals and create tasks
        for goal_db in goals_db:

            # get goal values
            goal_ID = goal_db[0]
            description = goal_db[3]
            completion_status = goal_db[2]
            duration = goal_db[4]

            # create goal object
            goal = Goal(goal_ID, description, completion_status, duration)

            # adds goal to goals list
            self.goals.append(goal)


    def Create_Post(self):

        post = []

        for goal in self.goals:

            post.append(goal.Create_Post())
