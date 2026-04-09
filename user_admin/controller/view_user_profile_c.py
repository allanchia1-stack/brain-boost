from user_admin.entity.user_profile import UserProfile


class ViewUserProfileController:
    @staticmethod
    def view_all_user_profiles():
        profiles = UserProfile.query.all()
        return [profile.to_dict() for profile in profiles]

    @staticmethod
    def view_user_profile_by_id(profile_id):
        profile = UserProfile.query.get(profile_id)
        if profile:
            return profile.to_dict()
        return None