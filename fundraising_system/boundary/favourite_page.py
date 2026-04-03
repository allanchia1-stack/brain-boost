class FavouritePage:
    def __init__(self, controller):
        self.controller = controller

    def save_activity(self, donee_id, activity_id):
        return self.controller.save_favourite(donee_id, activity_id)

    def view_saved_activities(self, donee_id):
        return self.controller.view_favourites(donee_id)

    def remove_saved_activity(self, favourite_id):
        return self.controller.remove_favourite(favourite_id)