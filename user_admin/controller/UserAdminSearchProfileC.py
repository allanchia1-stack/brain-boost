from user_admin.entity.UserProf import UserProf


class UserAdminSearchProfileC:
    @staticmethod
    def searchUserProfile(query=""):
        print("Executing UserAdminSearchProfileC.searchUserProfile")
        return UserProf.queryUserProfile(query)
