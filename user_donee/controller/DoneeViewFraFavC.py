from user_donee.entity.fra import FRA


class DoneeViewFraFavC:
    def doneeViewFavFra(self, fra_id):
        print("Executing DoneeViewFraFavC.doneeViewFavFra()")
        return FRA.doneeViewFavFra(fra_id)

    def viewFraFav(self, user_id):
        print("Executing DoneeViewFraFavC.viewFraFav()")
        return FRA.viewAllFraFav(user_id)

    def searchFraFav(self, user_id, query):
        #print("Executing DoneeViewFraFavC.searchFraFav()")
        if query:
            return FRA.searchFraFav(user_id, query)
        return FRA.viewAllFraFav(user_id)
