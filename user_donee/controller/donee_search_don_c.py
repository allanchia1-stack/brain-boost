from user_donee.entity.donation import Donation


class DoneeSearchDonC:
    def search_don(self, user_id, criteria):
        if criteria:
            return Donation.search_donation_history(user_id, criteria)
        return Donation.get_donation_history(user_id)
