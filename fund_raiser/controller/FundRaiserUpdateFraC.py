from fund_raiser.controller.FundRaiserViewFraC import FundRaiserViewFraC
from fund_raiser.entity.FRA import FRA

class FundRaiserUpdateFraC:
    @staticmethod
    def updateFra(fra_id, temp, owner_id):
        print("Executing FundRaiserUpdateFraC.updateFRA()")
        #return FundRaiserViewFraC.updateFraFromForm(fra_id, form, owner_id)
        return FRA.updateFra(fra_id, temp, owner_id)
    
