from fund_raiser.controller.FundRaiserViewFraC import FundRaiserViewFraC
from fund_raiser.entity.FRA import FRA

class FundRaiserSearchFraC:
    @staticmethod
    def searchFra(query, owner_id):
        #print("Executing FundRaiserSearchFraC.searchFra()")
        return FRA.searchFra(query, owner_id)

    @staticmethod
    def searchOngoingFra(query, owner_id):
        return [
            fra
            for fra in FundRaiserViewFraC.searchFra(query, owner_id)
            if fra.get("fra_status") == "ongoing"
        ]
