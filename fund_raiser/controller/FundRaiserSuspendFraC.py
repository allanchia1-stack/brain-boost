from fund_raiser.entity.FRA import FRA


class FundRaiserSuspendFraC:
    @staticmethod
    def suspendFra(fra_id, owner_id):
        #print("Executing FundRaiserSuspendFraC.suspendFra()")
        return FRA.suspendFra(fra_id, owner_id)
