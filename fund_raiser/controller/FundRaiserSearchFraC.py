from fund_raiser.controller.FundRaiserViewFraC import FundRaiserViewFraC


class FundRaiserSearchFraC:
    @staticmethod
    def searchFra(query, owner_id):
        return FundRaiserViewFraC.searchFra(query, owner_id)
