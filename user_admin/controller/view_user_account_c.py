from user_admin.controller.UserAdminViewAccountC import UserAdminViewAccountC
from user_admin.controller.UserAdminSearchAccountC import UserAdminSearchAccountC
from user_admin.controller.UserAdminUpdateAccountC import UserAdminUpdateAccountC
from user_admin.controller.UserAdminSuspendAccountC import UserAdminSuspendAccountC
from user_admin.entity.UserAcct import UserAcct


class ViewUserAccountController:
    @staticmethod
    def view_all_user_accounts():
        return UserAdminViewAccountC.view_all_user_accounts()

    @staticmethod
    def search_user_accounts(query):
        return UserAdminSearchAccountC.searchUserAccount(query)

    @staticmethod
    def view_user_account_by_id(user_id):
        return UserAdminViewAccountC.view(user_id)

    @staticmethod
    def update_user_account(user_id, email, password=None, name=None, phone=None, address=None, role=None):
        return UserAdminUpdateAccountC.updateUser(UserAcct(
            account_id=user_id, email=email, password=password, name=name,
            phone=phone, address=address, role=role
        ))

    @staticmethod
    def toggle_suspend_user_account(user_id):
        return UserAdminSuspendAccountC.SuspendUserAccount(user_id)
