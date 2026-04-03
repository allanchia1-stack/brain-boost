from entity.user_account import UserAccount


class UserAccountController:
    def __init__(self, datastore):
        self.datastore = datastore

    def create_user_account(self, username, password, user_id):
        account_id = self.datastore.generate_id("A", self.datastore.user_accounts)
        account = UserAccount(account_id, username, password, user_id)
        self.datastore.user_accounts.append(account)
        return account

    def find_account_by_username(self, username):
        for account in self.datastore.user_accounts:
            if account.username == username:
                return account
        return None