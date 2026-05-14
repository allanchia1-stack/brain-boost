from user_admin.entity.UserAcct import UserAcct


class UserAdminViewAccountC:
    @staticmethod
    def view(accountId):
        #print("executing UserAdminViewAccountC.view()")
        return UserAcct.view(accountId)

    @staticmethod
    def view_all_user_accounts():
        return UserAcct.get_all_accounts()
