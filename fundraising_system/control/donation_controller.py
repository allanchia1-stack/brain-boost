from entity.donation import Donation


class DonationController:
    def __init__(self, datastore):
        self.datastore = datastore

    def make_donation(self, donee_id, activity_id, amount):
        donation_id = self.datastore.generate_id("D", self.datastore.donations)
        donation = Donation(donation_id, donee_id, activity_id, amount)
        self.datastore.donations.append(donation)

        for activity in self.datastore.activities:
            if activity.activity_id == activity_id:
                activity.add_donation(amount)
                break

        return donation

    def view_donation_history(self, donee_id):
        return [donation for donation in self.datastore.donations if donation.donee_id == donee_id]