from datetime import datetime
from fund_raiser.entity.FRA import FRA


class ViewFRAController:
    @staticmethod
    def get_categories():
        return FRA.get_categories()

    @staticmethod
    def view_all_fras():
        return FRA.get_all_fras()

    @staticmethod
    def search_fras(query):
        return FRA.search_fras(query)

    @staticmethod
    def view_fra_by_id(fra_id):
        return FRA.get_fra_by_id(fra_id)

    @staticmethod
    def view_ongoing_fras():
        return FRA.get_ongoing_fras()

    @staticmethod
    def view_completed_fras():
        return FRA.get_completed_fras()

    @staticmethod
    def update_fra_from_form(fra_id, form):
        title = form.get("title", "").strip()
        description = form.get("description", "").strip()

        try:
            category_id = int(form.get("category", ""))
            start_date = datetime.strptime(form.get("start_date", ""), "%Y-%m-%d").date()
            end_date = datetime.strptime(form.get("end_date", ""), "%Y-%m-%d").date()
            goal = int(form.get("goal", ""))
        except ValueError:
            return False, "Please enter a valid category, date range, and donation goal."

        success = ViewFRAController.update_fra(
            fra_id,
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

    @staticmethod
    def update_fra(fra_id, title, category_id, start_date, end_date, goal, description):
        if not title or not category_id or not start_date or not end_date or not goal:
            return False

        if end_date < start_date:
            return False

        if goal <= 0:
            return False

        return FRA.update_fra(
            fra_id,
            title,
            category_id,
            start_date,
            end_date,
            goal,
            description,
        )
