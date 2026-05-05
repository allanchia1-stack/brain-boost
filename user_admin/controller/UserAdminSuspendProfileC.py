from user_admin.entity.UserProf import UserProf


class UserAdminSuspendProfileC:
    @staticmethod
    def SuspendProf(profile_id):
        return UserProf.SuspendProf(profile_id)

    # Backward compatible alias
    @staticmethod
    def SuspendUserProfile(profile_id):
        return UserAdminSuspendProfileC.SuspendProf(profile_id)
