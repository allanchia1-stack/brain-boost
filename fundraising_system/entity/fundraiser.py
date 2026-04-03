from entity.user import User


class FundRaiser(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email, role="fundraiser")

        self.activities = []  # list of activity IDs

    def add_activity(self, activity_id):
        self.activities.append(activity_id)

    def view_activities(self):
        return self.activities