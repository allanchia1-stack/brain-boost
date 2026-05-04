from user_admin.entity.UserAcct import UserAcct


class UserAdminSuspendAccountC:
    @staticmethod
    def SuspendUserAccount(idNum):
        return UserAcct.SuspendUserAccount(idNum)
