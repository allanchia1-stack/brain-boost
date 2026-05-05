from user_admin.entity.UserProf import UserProf


class UserAdminUpdateProfileC:
    @staticmethod
    def updateProf(temp):
        return UserProf.updateProf(temp)

    # Backward compatible alias
    @staticmethod
    def updateUser(temp):
        return UserAdminUpdateProfileC.updateProf(temp)
