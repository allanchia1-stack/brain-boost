class AuthController:
    def __init__(self, datastore):
        self.datastore = datastore

    def login(self, username, password):
        for account in self.datastore.user_accounts:
            if account.username == username and account.check_password(password):
                return account
        return None

    def logout(self):
        return "User logged out successfully."