from user_admin.entity.user_profiles import UserProfiles


class ViewUserProfilesController:
    @staticmethod
    def view_all_user_profiles():
        profiles = UserProfiles.query.all()
        return [profile.to_dict() for profile in profiles]

    @staticmethod
    def view_user_profiles_by_id(profile_id):
        profile = UserProfiles.query.get(profile_id)
        if profile:
            return profile.to_dict()
        return None