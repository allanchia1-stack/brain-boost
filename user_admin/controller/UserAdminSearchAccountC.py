from user_admin.entity.UserAcct import UserAcct


class UserAdminSearchAccountC:
    @staticmethod
    def searchUserAccount(user_id_match):
        return UserAcct.queryUserAccount(user_id_match)
