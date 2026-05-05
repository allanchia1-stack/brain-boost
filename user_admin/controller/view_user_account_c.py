from user_admin.entity.UserAcct import UserAcct


class ViewUserAccountController:
    @staticmethod
    def view_all_user_accounts():
        return UserAcct.get_all_accounts()

    @staticmethod
    def search_user_accounts(query):
        return UserAcct.search_accounts(query)

    @staticmethod
    def view_user_account_by_id(user_id):
        return UserAcct.get_account_by_user_id(user_id)

    @staticmethod
    def update_user_account(user_id, email, password):
        return UserAcct.update_account(user_id, email, password)

    @staticmethod
    def toggle_suspend_user_account(user_id):
        return UserAcct.toggle_suspend_account(user_id)
