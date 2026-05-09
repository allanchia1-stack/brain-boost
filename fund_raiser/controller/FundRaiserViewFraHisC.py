from fund_raiser.controller.FundRaiserViewFraC import FundRaiserViewFraC
from fund_raiser.entity.FRA import FRA

class FundRaiserViewFraHisC:
    @staticmethod
    def viewFraHistory(owner_id):
        #return FundRaiserViewFraC.viewCompletedFra(owner_id)
        return FRA.viewFraHistory(owner_id)
