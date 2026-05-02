from user_donee.entity.donation import Donation


class DoneeViewDonC:
    def view_don(self, user_id, donation_id):
        return Donation.get_donation_by_id(user_id, donation_id)
