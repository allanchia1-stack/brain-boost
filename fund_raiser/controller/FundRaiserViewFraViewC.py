from fund_raiser.entity.FRA import FRA


class FundRaiserViewFraViewC:
    @staticmethod
    def viewNumOfViews(fra_id, owner_id):
        fra = FRA.get_fra_by_id(fra_id, owner_id)
        return 0 if fra is None else fra.get("fra_views", 0)
