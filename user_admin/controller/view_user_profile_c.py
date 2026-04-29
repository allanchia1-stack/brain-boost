from user_admin.entity.user_profile import UserProfile


class ViewUserProfileController:
    @staticmethod
    def view_all_user_profiles():
        return UserProfile.get_all_profiles()

    @staticmethod
    def search_user_profiles(query):
        return UserProfile.search_profiles(query)

    @staticmethod
    def view_user_profile_by_id(profile_id):
        return UserProfile.get_profile_by_id(profile_id)
