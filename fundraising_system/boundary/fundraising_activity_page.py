class FundRaisingActivityPage:
    def __init__(self, controller):
        self.controller = controller

    def create_activity(self, title, description, target_amount, category, fundraiser_id):
        return self.controller.create_activity(title, description, target_amount, category, fundraiser_id)

    def view_activities(self):
        return self.controller.view_all_activities()

    def update_activity(self, activity_id, title, description, target_amount, category):
        return self.controller.update_activity(activity_id, title, description, target_amount, category)

    def complete_activity(self, activity_id):
        return self.controller.complete_activity(activity_id)