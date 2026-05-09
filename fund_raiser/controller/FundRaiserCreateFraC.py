from datetime import date

from fund_raiser.entity.FRA import FRA


class FundRaiserCreateFraC:
    @staticmethod
    def get_categories():
        return FRA.get_categories()

    @staticmethod
    def createFra(temp):
        print("Executing FundRaiserCreateFraC.createFra()")
        if not temp.title or not temp.category_id or not temp.start_date or not temp.end_date or not temp.goal:
            return False
        if temp.end_date < temp.start_date:
            return False
        if temp.goal <= 0:
            return False
        if not temp.owner_id:
            return False
        if temp.start_date < date.today():
            return False

        return FRA.createFra(temp)
