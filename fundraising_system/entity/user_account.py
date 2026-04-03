class UserAccount:
    def __init__(self, account_id, username, password, user_id):
        self.account_id = account_id
        self.username = username
        self.password = password
        self.user_id = user_id

    def check_password(self, password):
        return self.password == password