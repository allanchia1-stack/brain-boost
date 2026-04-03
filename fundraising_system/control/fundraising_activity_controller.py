from entity.fundraising_activity import FundRaisingActivity


class FundRaisingActivityController:
    def __init__(self, datastore):
        self.datastore = datastore

    def create_activity(self, title, description, target_amount, category, fundraiser_id):
        activity_id = self.datastore.generate_id("FA", self.datastore.activities)
        activity = FundRaisingActivity(
            activity_id, title, description, target_amount, category, fundraiser_id
        )
        self.datastore.activities.append(activity)
        return activity

    def view_all_activities(self):
        return self.datastore.activities

    def update_activity(self, activity_id, title, description, target_amount, category):
        for activity in self.datastore.activities:
            if activity.activity_id == activity_id:
                activity.update_activity(title, description, target_amount, category)
                return activity
        return None

    def complete_activity(self, activity_id):
        for activity in self.datastore.activities:
            if activity.activity_id == activity_id:
                activity.mark_completed()
                return activity
        return None