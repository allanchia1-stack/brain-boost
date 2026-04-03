class FundRaisingActivity:
    def __init__(self, activity_id, title, description, target_amount, category, fundraiser_id, status="active"):
        self.activity_id = activity_id
        self.title = title
        self.description = description
        self.target_amount = target_amount
        self.category = category
        self.fundraiser_id = fundraiser_id
        self.status = status
        self.amount_raised = 0.0

    def update_activity(self, title, description, target_amount, category):
        self.title = title
        self.description = description
        self.target_amount = target_amount
        self.category = category

    def mark_completed(self):
        self.status = "completed"

    def add_donation(self, amount):
        self.amount_raised += amount