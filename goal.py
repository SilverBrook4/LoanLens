# This is the Goal class that will populate checklist


class Goal:

    def __init__(self, id, description, status, duration):

        self.id = id
        self.description = description
        self.status = status
        self.duration = duration


    def Create_Post(self):

        return {'id':self.id, 'description':self.description, 'status':self.status}
