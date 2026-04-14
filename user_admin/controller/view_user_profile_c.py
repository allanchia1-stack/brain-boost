from user_admin.entity.user_profile import UserProfile


class ViewUserProfileController:
    @staticmethod
    def view_all_user_profiles():
        profiles = UserProfile.get_all_profiles()
        return [profile.to_dict() for profile in profiles]

    @staticmethod
    def view_user_profile_by_id(profile_id):
        profile = UserProfile.get_profile_by_id(profile_id)
        if profile is None:
            return None
        return profile.to_dict()