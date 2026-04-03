class DonationHistoryPage:
    def __init__(self, controller):
        self.controller = controller

    def view_history(self, donee_id):
        return self.controller.view_donation_history(donee_id)