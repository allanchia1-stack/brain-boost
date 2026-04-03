from entity.user import User


class Donee(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email, role="donee")

        self.favourites = []   # list of activity IDs
        self.donations = []    # list of donation IDs

    def add_favourite(self, activity_id):
        if activity_id not in self.favourites:
            self.favourites.append(activity_id)

    def remove_favourite(self, activity_id):
        if activity_id in self.favourites:
            self.favourites.remove(activity_id)

    def add_donation(self, donation_id):
        self.donations.append(donation_id)

    def view_favourites(self):
        return self.favourites

    def view_donations(self):
        return self.donationsd