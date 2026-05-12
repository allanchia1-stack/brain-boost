from user_donee.entity.FRA import FRA


class DoneeSearchFraC:
    def searchFra(self, query):
        print("Executing DoneeSearchFraC.searchFra()")
        if query:
            return FRA.searchFra(query)
        return FRA.get_all_fras()
