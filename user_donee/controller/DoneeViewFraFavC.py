from user_donee.entity.FRA import FRA


class DoneeViewFraFavC:
    def viewFraFav(self, user_id):
        return FRA.viewAllFraFav(user_id)

    def searchFraFav(self, user_id, query):
        print("Executing DoneeViewFraFavC.searchFraFav()")
        if query:
            return FRA.searchFraFav(user_id, query)
        return FRA.viewAllFraFav(user_id)
