from entity.user_profile import UserProfile


class UserProfileController:
    def __init__(self, datastore):
        self.datastore = datastore

    def create_user_profile(self, user_id, address, phone):
        profile_id = self.datastore.generate_id("P", self.datastore.user_profiles)
        profile = UserProfile(profile_id, user_id, address, phone)
        self.datastore.user_profiles.append(profile)
        return profile

    def view_user_profile(self, user_id):
        for profile in self.datastore.user_profiles:
            if profile.user_id == user_id:
                return profile
        return None

    def update_user_profile(self, user_id, address, phone):
        profile = self.view_user_profile(user_id)
        if profile:
            profile.update_profile(address, phone)
            return profile
        return None