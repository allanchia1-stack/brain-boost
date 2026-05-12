from user_donee.entity.FRA import FRA


class DoneeSaveFraFavC:
    def saveFra(self, user_id, fra_id):
        print("Executing DoneeSaveFraFavC.saveFra()")
        if FRA.is_saved(user_id, fra_id):
            return FRA.unsave_fra(user_id, fra_id)
        return FRA.saveFra(user_id, fra_id)
