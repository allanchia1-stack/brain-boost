from datetime import datetime

from fund_raiser.entity.FRA import FRA


class FundRaiserViewFraC:
    @staticmethod
    def viewFra(owner_id):
        return FRA.get_all_fras(owner_id)

    @staticmethod
    def viewFraById(fra_id, owner_id):
        print("Executing FundRaiserViewFraC.viewFraById()")
        return FRA.viewFraById(fra_id, owner_id)

    @staticmethod
    def getCategories():
        return FRA.get_categories()

    @staticmethod
    def viewOngoingFra(owner_id):
        return FRA.get_ongoing_fras(owner_id)

    @staticmethod
    def viewCompletedFra(owner_id):
        return FRA.get_completed_fras(owner_id)

    @staticmethod
    def searchFra(query, owner_id):
        return FRA.search_fras(query, owner_id)

    @staticmethod
    def updateFra(fra_id, owner_id, title, category_id, start_date, end_date, goal, description):
        if not title or not category_id or not start_date or not end_date or not goal:
            return False
        if not owner_id:
            return False
        if end_date < start_date:
            return False
        if goal <= 0:
            return False
        return FRA.update_fra(
            fra_id,
            owner_id,
            title,
            category_id,
            start_date,
            end_date,
            goal,
            description,
        )

    @staticmethod
    def updateFraFromForm(fra_id, form, owner_id):
        title = form.get("title", "").strip()
        description = form.get("description", "").strip()
        try:
            category_id = int(form.get("category", ""))
            start_date = datetime.strptime(form.get("start_date", ""), "%Y-%m-%d").date()
            end_date = datetime.strptime(form.get("end_date", ""), "%Y-%m-%d").date()
            goal = int(form.get("goal", ""))
        except ValueError:
            return False, "Please enter a valid category, date range, and donation goal."

        success = FundRaiserViewFraC.updateFra(
            fra_id,
            owner_id,
            title,
            category_id,
            start_date,
            end_date,
            goal,
            description,
        )
        if not success:
            return False, "Unable to update fund raising activity."
        return True, None
