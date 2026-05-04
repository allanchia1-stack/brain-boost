from user_admin.entity.UserProf import UserProf


class UserAdminViewProfileC:
    @staticmethod
    def view(profile_id):
        return UserProf.view(profile_id)

    @staticmethod
    def view_all_user_profiles():
        return UserProf.get_all_profiles()
