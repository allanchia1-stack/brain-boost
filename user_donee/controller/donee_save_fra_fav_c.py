from user_donee.entity.favourite_fra import FavouriteFRA


class DoneeSaveFraFavC:
    def saveFra(self, user_id, fra_id):
        print("Executing DoneeSaveFraFavC.saveFra()")
        if FavouriteFRA.is_saved(user_id, fra_id):
            #FavouriteFRA.unsave_fra(user_id, fra_id)
            #return "unsaved"
            return FavouriteFRA.unsave_fra(user_id, fra_id)
        #return "saved"
        return FavouriteFRA.saveFra(user_id, fra_id)
