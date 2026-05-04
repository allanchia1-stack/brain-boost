from user_donee.entity.fra import FRA


class DoneeSearchFraC:
    def search_fra(self, criteria):
        if criteria:
            return FRA.search_fras(criteria)
        return FRA.get_all_fras()
