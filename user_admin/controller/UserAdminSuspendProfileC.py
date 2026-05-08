from user_admin.entity.UserProf import UserProf


class UserAdminSuspendProfileC:
    @staticmethod
    def suspendProf(profile_id):
        print("Executing UserAdminSuspendProfileC.suspendProf")
        return UserProf.suspendProf(profile_id)

    # Backward compatible alias
    @staticmethod
    def SuspendUserProfile(profile_id):
        return UserAdminSuspendProfileC.SuspendProf(profile_id)
