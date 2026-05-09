from flask import redirect, render_template, request, session, url_for

from datetime import datetime
from fund_raiser.controller.FundRaiserUpdateFraC import FundRaiserUpdateFraC
from fund_raiser.controller.FundRaiserViewFraC import FundRaiserViewFraC
from fund_raiser.controller.FundRaiserViewFraViewC import FundRaiserViewFraViewC
from fund_raiser.entity.FRA import FRA

def get_back_route(source):
    if source == "ongoing":
        return url_for("view_fra_bp.view_fras_ongoing")
    if source == "completed":
        return url_for("view_fra_bp.view_fras_completed")
    return url_for("view_fra_bp.view_fras_page")


class FundRaiserPg:
    @staticmethod
    def updateFra(fra_id):
        owner_id = session.get("user_id")
        if not owner_id:
            return redirect(url_for("login"))
        source = request.args.get("source", "all").strip() or "all"
        success = False
        error = None
        if request.method == "GET":
            FundRaiserViewFraViewC.updateNumOfViews(fra_id)
        if request.method == "POST" and request.form.get("action") == "update":
            
            print("Executing FundRaiserPg.updateFRA()")
            temp = FRA(
            title=request.form.get("title"),
            category_id=int(request.form.get("category")),
            start_date=datetime.strptime(request.form.get("start_date", ""), "%Y-%m-%d").date(),
            end_date=datetime.strptime(request.form.get("end_date", ""), "%Y-%m-%d").date(),
            goal=int(request.form.get("goal")),
            description=request.form.get("description"),
            owner_id=owner_id
            )

            result = FundRaiserUpdateFraC.updateFra(fra_id, temp, owner_id)
            if result is not None:
                success = True
                error = ""
            else:
                success = False
                error = "Unable to update fund raising activity."
        fra = FundRaiserViewFraC.viewFraById(fra_id, owner_id)
        categories = FundRaiserViewFraC.getCategories()
        if fra is None:
            return "Fund raising activity not found", 404
        return render_template(
            "fund_raiser/view_fra_detail.html",
            fra=fra,
            categories=categories,
            success=success,
            error=error,
            back_url=get_back_route(source),
            source=source,
        )
