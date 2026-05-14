from user_admin.entity.UserAcct import UserAcct


class UserAdminSearchAccountC:
    @staticmethod
    def searchUserAccount(text):
        #print("Executing UserAdminSearchAccountC.searchUserAccount()")
        return UserAcct.queryUserAccount(text)
