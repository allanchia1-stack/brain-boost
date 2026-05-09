from fund_raiser.controller.FundRaiserViewFraC import FundRaiserViewFraC
from fund_raiser.entity.FRA import FRA

class FundRaiserSearchFraHisC:
    @staticmethod
    def searchFraHis(query, owner_id):
        #return [
        #    fra
        #    for fra in FundRaiserViewFraC.searchFra(query, owner_id)
        #    if fra.get("fra_status") == "completed"
        #]
        return[
            fra
            for fra in FRA.searchFra(query, owner_id)
            if fra.get("fra_status") == "completed"
        ]
