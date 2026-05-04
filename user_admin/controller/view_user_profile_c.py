from user_admin.controller.UserAdminViewProfileC import UserAdminViewProfileC
from user_admin.controller.UserAdminSearchProfileC import UserAdminSearchProfileC
from user_admin.controller.UserAdminUpdateProfileC import UserAdminUpdateProfileC
from user_admin.controller.UserAdminSuspendProfileC import UserAdminSuspendProfileC
from user_admin.entity.UserProf import UserProf


class ViewUserProfileController:
    @staticmethod
    def view_all_user_profiles():
        return UserAdminViewProfileC.view_all_user_profiles()

    @staticmethod
    def search_user_profiles(query):
        return UserAdminSearchProfileC.searchUserProfile(query, query)

    @staticmethod
    def view_user_profile_by_id(profile_id):
        return UserAdminViewProfileC.view(profile_id)

    @staticmethod
    def update_user_profile(profile_id, role):
        return UserAdminUpdateProfileC.updateUser(UserProf(role=role, profile_id=profile_id))

    @staticmethod
    def toggle_suspend_user_profile(profile_id):
        return UserAdminSuspendProfileC.SuspendUserProfile(profile_id)
