from fund_raiser.controller.FundRaiserViewFraC import FundRaiserViewFraC


class FundRaiserUpdateFraC:
    @staticmethod
    def updateFraFromForm(fra_id, form, owner_id):
        return FundRaiserViewFraC.updateFraFromForm(fra_id, form, owner_id)
