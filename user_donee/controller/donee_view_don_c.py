from user_donee.entity.donation import Donation


class DoneeViewDonC:
    def viewDon(self, user_id, donation_id):
        print("Executing DoneeViewDonC.viewDon()")
        return Donation.viewDon(user_id, donation_id)
