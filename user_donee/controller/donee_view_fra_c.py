from user_donee.entity.fra import FRA
from user_donee.entity.favourite_fra import FavouriteFRA


class DoneeViewFraC:
    def view_all_fra(self):
        return FRA.get_all_fras()

    def update_num_of_views(self, fra_id):
        return FRA.increment_fra_views(fra_id)

    def view_fra(self, fra_id, user_id):
        fra = FRA.get_fra_by_id(fra_id)
        saved = FavouriteFRA.is_saved(user_id, fra_id)
        return fra, saved
