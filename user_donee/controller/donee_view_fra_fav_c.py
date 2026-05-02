from user_donee.entity.favourite_fra import FavouriteFRA


class DoneeViewFraFavC:
    def donee_view_fav_fra(self, user_id):
        return FavouriteFRA.get_favourite_fras(user_id)

    def donee_search_fav_fra(self, user_id, criteria):
        if criteria:
            return FavouriteFRA.search_favourite_fras(user_id, criteria)
        return FavouriteFRA.get_favourite_fras(user_id)
