# This is the Checklist class for the checklist on the users dashboard
import goal
import sys
import os
# import database files
from database import db
from goal import Goal

class Checklist:

    # checklist class constructor
    def __init__(self, user):

        self.user = user
        self.goals = []

        self.Get_Goals_From_DB()


    def Get_Goals_From_DB(self):
        user_id = self.user.get("id")  # extract Kinde user ID
        goals_db = db.retrieve_goals(user_id)

        # cycle through all goals and create tasks
        for goal_db in goals_db:

            # get goal values
            goal_ID = goal_db[0]
            description = goal_db[3]
            completion_status = goal_db[2]
            duration = goal_db[4]

            # create goal object
            g = Goal(goal_ID, description, completion_status, duration)

            # adds goal to goals list
            self.goals.append(g)


    def Create_Post(self):

        post = []

        for g in self.goals:

            post.append(g.Create_Post())

        return post
