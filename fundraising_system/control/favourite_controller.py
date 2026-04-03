from entity.favourite import Favourite


class FavouriteController:
    def __init__(self, datastore):
        self.datastore = datastore

    def save_favourite(self, donee_id, activity_id):
        favourite_id = self.datastore.generate_id("F", self.datastore.favourites)
        favourite = Favourite(favourite_id, donee_id, activity_id)
        self.datastore.favourites.append(favourite)
        return favourite

    def view_favourites(self, donee_id):
        return [fav for fav in self.datastore.favourites if fav.donee_id == donee_id]

    def remove_favourite(self, favourite_id):
        for fav in self.datastore.favourites:
            if fav.favourite_id == favourite_id:
                self.datastore.favourites.remove(fav)
                return True
        return False