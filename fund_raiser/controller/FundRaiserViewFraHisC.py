from fund_raiser.controller.FundRaiserViewFraC import FundRaiserViewFraC


class FundRaiserViewFraHisC:
    @staticmethod
    def viewFraHistory(owner_id):
        return FundRaiserViewFraC.viewCompletedFra(owner_id)
