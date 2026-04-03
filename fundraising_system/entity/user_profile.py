class UserProfile:
    def __init__(self, profile_id, user_id, address="", phone=""):
        self.profile_id = profile_id
        self.user_id = user_id
        self.address = address
        self.phone = phone

    def update_profile(self, address, phone):
        self.address = address
        self.phone = phone