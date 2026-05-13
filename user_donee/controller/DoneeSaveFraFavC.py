from user_donee.entity.fra import FRA


class DoneeSaveFraFavC:
    def saveFra(self, acct_id, fra_id):
        print("Executing DoneeSaveFraFavC.saveFra()")
        if FRA.is_saved(acct_id, fra_id):
            return FRA.unsaveFra(acct_id, fra_id)
        return FRA.saveFra(acct_id, fra_id)
