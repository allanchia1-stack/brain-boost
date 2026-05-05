from fund_raiser.entity.FRA import FRA


class FundRaiserSuspendFraC:
    @staticmethod
    def suspendFra(fra_id, owner_id):
        return FRA.suspend_fra(fra_id, owner_id)
