from fund_raiser.controller.FundRaiserViewFraC import FundRaiserViewFraC


class FundRaiserSearchFraC:
    @staticmethod
    def searchFra(query, owner_id):
        return FundRaiserViewFraC.searchFra(query, owner_id)

    @staticmethod
    def searchOngoingFra(query, owner_id):
        return [
            fra
            for fra in FundRaiserViewFraC.searchFra(query, owner_id)
            if fra.get("fra_status") == "ongoing"
        ]
