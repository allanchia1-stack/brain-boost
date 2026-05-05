from user_admin.entity.UserAcct import UserAcct


class UserAdminViewAccountC:
    @staticmethod
    def view(accountId):
        return UserAcct.view(accountId)

    @staticmethod
    def view_all_user_accounts():
        return UserAcct.get_all_accounts()
