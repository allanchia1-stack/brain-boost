from user_donee.entity.FRA import FRA


class DoneeViewFraC:
    def view_all_fra(self):
        return FRA.get_all_fras()

    def update_num_of_views(self, fra_id):
        return FRA.increment_fra_views(fra_id)

    def viewFra(self, fra_id, user_id):
        print("Executing DoneeViewFraC.viewFra()")
        fra = FRA.viewFra(fra_id)
        saved = FRA.is_saved(user_id, fra_id)
        return fra, saved
