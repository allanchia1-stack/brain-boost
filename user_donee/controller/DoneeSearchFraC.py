from user_donee.entity.fra import FRA


class DoneeSearchFraC:
    def searchFra(self, query):
        #print("Executing DoneeSearchFraC.searchFra()")
        if query:
            return FRA.searchFra(query)
        return FRA.get_all_fras()
