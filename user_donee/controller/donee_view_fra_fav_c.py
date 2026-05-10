from user_donee.entity.favourite_fra import FavouriteFRA
from user_donee.entity.fra import FRA


class DoneeViewFraFavC:
    def donee_view_fav_fra(self, user_id):
        return FRA.viewAllFraFav(user_id)

    def searchFraFav(self, user_id, criteria):
        print("Executing DoneeViewFraFav.searchFraFav()")
        if criteria:
            return FRA.searchFraFav(user_id, criteria)
        return FRA.viewAllFraFav(user_id)
