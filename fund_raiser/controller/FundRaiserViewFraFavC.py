from fund_raiser.entity.FRA import FRA


class FundRaiserViewFraFavC:
    @staticmethod
    def viewNumOfFavourites(fra_id, owner_id):
        fra = FRA.get_fra_by_id(fra_id, owner_id)
        return 0 if fra is None else fra.get("fra_num_of_fav", 0)
