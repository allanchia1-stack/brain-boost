from user_admin.entity.UserProf import UserProf


class UserAdminSearchProfileC:
    @staticmethod
    def searchUserProfile(search_query=""):
        return UserProf.queryUserProfile(search_query)
