from fund_raiser.controller.FundRaiserViewFraC import FundRaiserViewFraC


class FundRaiserSearchFraHisC:
    @staticmethod
    def searchFraHistory(query, owner_id):
        return [
            fra
            for fra in FundRaiserViewFraC.searchFra(query, owner_id)
            if fra.get("fra_status") == "completed"
        ]
