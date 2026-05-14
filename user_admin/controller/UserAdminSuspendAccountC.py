from user_admin.entity.UserAcct import UserAcct


class UserAdminSuspendAccountC:
    @staticmethod
    def suspendUserAccount(account_id):
        #print("Executing UserAdminSuspendAccountC.suspendUserAccout()")
        return UserAcct.suspendUserAccount(account_id)
