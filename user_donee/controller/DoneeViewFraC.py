from user_donee.entity.fra import FRA


class DoneeViewFraC:
    def view(self, fra_id, user_id):
        print("Executing DoneeViewFraC.view()")
        FRA.increment_fra_views(fra_id)
        fra = FRA.view(fra_id)
        saved = FRA.is_saved(user_id, fra_id)
        return fra, saved

    def view_all_fra(self):
        print("Executing DoneeViewFraC.view_all_fra()")
        return FRA.get_all_fras()
