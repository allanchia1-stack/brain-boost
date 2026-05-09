from flask import redirect, request, session, url_for

from fund_raiser.boundary.FundRaiserPg import FundRaiserPg
from fund_raiser.controller.FundRaiserSuspendFraC import FundRaiserSuspendFraC


def get_back_route(source):
    if source == "ongoing":
        return url_for("view_fra_bp.view_fras_ongoing")
    if source == "completed":
        return url_for("view_fra_bp.view_fras_completed")
    return url_for("view_fra_bp.view_fras_page")


class FundRaisingActivityPg:
    @staticmethod
    def suspendFra(fra_id):
        owner_id = session.get("user_id")
        if not owner_id:
            return redirect(url_for("login"))
        source = request.args.get("source", "all").strip() or "all"
        if request.method == "POST" and request.form.get("action") == "suspend":
            print("Executing FundRaisingActivityPg.suspendFra()")
            FundRaiserSuspendFraC.suspendFra(fra_id, owner_id)
            return redirect(get_back_route(source))
        return FundRaiserPg.updateFra(fra_id)
