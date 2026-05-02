from user_donee.entity.favourite_fra import FavouriteFRA


class DoneeSaveFraFavC:
    def toggle_save_fra(self, user_id, fra_id):
        if FavouriteFRA.is_saved(user_id, fra_id):
            FavouriteFRA.unsave_fra(user_id, fra_id)
            return "unsaved"
        FavouriteFRA.save_fra(user_id, fra_id)
        return "saved"
