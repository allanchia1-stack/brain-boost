from user_admin.entity.UserProf import UserProf


class UserAdminUpdateProfileC:
    @staticmethod
    def updateUser(tempProfile):
        return UserProf.updateUser(tempProfile)
