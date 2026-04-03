class UserProfilePage:
    def __init__(self, controller):
        self.controller = controller

    def create_profile(self, user_id, address, phone):
        return self.controller.create_user_profile(user_id, address, phone)

    def view_profile(self, user_id):
        return self.controller.view_user_profile(user_id)

    def update_profile(self, user_id, address, phone):
        return self.controller.update_user_profile(user_id, address, phone)