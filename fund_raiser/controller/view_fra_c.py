from fund_raiser.entity.FRA import FRA


class ViewFRAController:
    @staticmethod
    def view_all_fras():
        return FRA.get_all_fras()

    @staticmethod
    def search_fras(query):
        return FRA.search_fras(query)

    @staticmethod
    def view_fra_by_id(fra_id):
        return FRA.get_fra_by_id(fra_id)

