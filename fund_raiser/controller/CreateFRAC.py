from datetime import date
from fund_raiser.entity.FRA import FRA


class CreateFRAC:
    @staticmethod
    def get_categories():
        return FRA.get_categories()

    @staticmethod
    def create_fra(title, category_id, start_date, end_date, goal, description, owner_id):
        if not title or not category_id or not start_date or not end_date or not goal:
            return False

        if end_date < start_date:
            return False

        if goal <= 0:
            return False

        if not owner_id:
            return False

        if start_date < date.today():
            return False

        return FRA.create_fra(
            title,
            category_id,
            start_date,
            end_date,
            goal,
            description,
            owner_id,
        )

