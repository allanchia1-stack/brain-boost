from datetime import datetime
from flask import redirect, render_template, request, session, url_for
from fund_raiser.controller.CreateFRAC import CreateFRAC


class CreateFRAPg:
    def __init__(self):
        self.control = CreateFRAC()

    def get(self, error=None):
        categories = self.control.get_categories()
        return render_template("fund_raiser/create_fra.html", categories=categories, error=error)

    def post(self):
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        owner_id = session.get("user_id")

        try:
            category_id = int(request.form.get("category", ""))
            start_date = datetime.strptime(request.form.get("start_date", ""), "%Y-%m-%d").date()
            end_date = datetime.strptime(request.form.get("end_date", ""), "%Y-%m-%d").date()
            goal = int(request.form.get("goal", ""))
        except ValueError:
            return self.get("Please enter a valid category, date range, and donation goal."), 400

        created = self.control.create_fra(
            title,
            category_id,
            start_date,
            end_date,
            goal,
            description,
            owner_id,
        )
        if created:
            return redirect(url_for("view_fra_bp.view_fras_page"))

        return self.get("Unable to create fund raising activity."), 400

