from control.user_account_controller import UserAccountController


class UserAccountPage:
    def __init__(self, controller: UserAccountController):
        self.controller = controller

    def create_account(self, username, password, user_id):
        return self.controller.create_user_account(username, password, user_id)

    def find_account(self, username):
        return self.controller.find_account_by_username(username)