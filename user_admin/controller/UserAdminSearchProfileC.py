from user_admin.entity.UserProf import UserProf


class UserAdminSearchProfileC:
    @staticmethod
    def searchUserProfile(user_name="", role=""):
        return UserProf.queryUserProfile(user_name, role)
