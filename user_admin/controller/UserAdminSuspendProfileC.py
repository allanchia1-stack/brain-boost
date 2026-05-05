from user_admin.entity.UserProf import UserProf


class UserAdminSuspendProfileC:
    @staticmethod
    def SuspendUserProfile(profile_id):
        return UserProf.SuspendUserProfile(profile_id)
