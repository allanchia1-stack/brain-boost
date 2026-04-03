from control.auth_controller import AuthController


class LoginPage:
    def __init__(self, controller: AuthController):
        self.controller = controller

    def login(self, username, password):
        return self.controller.login(username, password)

    def logout(self):
        return self.controller.logout()