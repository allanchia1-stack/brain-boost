from user_donee.entity.donation import Donation


class DoneeSearchDonC:
    def searchDon(self, user_id, criteria):
        if criteria:
            print("Executing DoneeSearchDonC.searchDon()")
            return Donation.searchDon(user_id, criteria)
        return Donation.get_donation_history(user_id)
