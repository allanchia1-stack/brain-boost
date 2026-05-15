from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for

from fund_raiser.controller.FundRaiserSearchFraC import FundRaiserSearchFraC
from fund_raiser.controller.FundRaiserSearchFraHisC import FundRaiserSearchFraHisC
from fund_raiser.controller.FundRaiserViewFraC import FundRaiserViewFraC
from fund_raiser.controller.FundRaiserViewFraFavC import FundRaiserViewFraFavC
from fund_raiser.controller.FundRaiserViewFraHisC import FundRaiserViewFraHisC
from fund_raiser.controller.FundRaiserViewFraViewC import FundRaiserViewFraViewC
from fund_raiser.boundary.FundRaisingActivityPg import FundRaisingActivityPg

view_fra_bp = Blueprint("view_fra_bp", __name__)


def get_current_owner_id():
    return session.get("user_id")


def get_back_route(source):
    if source == "ongoing":
        return url_for("view_fra_bp.view_fras_ongoing")
    if source == "completed":
        return url_for("view_fra_bp.view_fras_completed")
    return url_for("view_fra_bp.view_fras_page")


class FundRaiserResultFraPg:
    def showResult(self, fras, owner_id, search_query="", title="View Fund Raising Activities", source="all"):
        for fra in fras:
            fra["fra_views"] = self.viewNumOfViews(fra["fra_id"], owner_id)
            fra["fra_num_of_fav"] = self.viewNumOfFavourites(fra["fra_id"], owner_id)
        return render_template(
            "fund_raiser/view_fras.html",
            fras=fras,
            search_query=search_query,
            title=title,
            source=source,
        )

    def viewFra(self, owner_id):
        return FundRaiserViewFraC.viewFra(owner_id)

    def searchFra(self, query, owner_id):
        #print("Executing FundRaiserResultFraPg.searchFra")
        return FundRaiserSearchFraC.searchFra(query, owner_id)

    def searchOngoingFra(self, query, owner_id):
        return FundRaiserSearchFraC.searchOngoingFra(query, owner_id)

    def viewFraHistory(self, owner_id):
        return FundRaiserViewFraHisC.viewFraHistory(owner_id)

    def searchFraHistory(self, query, owner_id):
        return FundRaiserSearchFraHisC.searchFraHis(query, owner_id)

    def viewNumOfViews(self, fra_id, owner_id):
        return FundRaiserViewFraViewC.viewNumOfViews(fra_id, owner_id)

    def viewNumOfFavourites(self, fra_id, owner_id):
        return FundRaiserViewFraFavC.viewNumOfFavourites(fra_id, owner_id)


@view_fra_bp.route("/fund_raiser/view_fras_page", methods=["GET"])
def view_fras_page():
    owner_id = get_current_owner_id()
    if not owner_id:
        return redirect(url_for("login"))
    page = FundRaiserResultFraPg()
    search_query = request.args.get("q", "").strip()
    fras = page.searchFra(search_query, owner_id) if search_query else page.viewFra(owner_id)
    return page.showResult(fras, owner_id, search_query=search_query, title="View Fund Raising Activities", source="all")


@view_fra_bp.route("/fund_raiser/view_fras_ongoing", methods=["GET"])
def view_fras_ongoing():
    owner_id = get_current_owner_id()
    if not owner_id:
        return redirect(url_for("login"))
    page = FundRaiserResultFraPg()
    search_query = request.args.get("q", "").strip()
    fras = page.searchOngoingFra(search_query, owner_id) if search_query else FundRaiserViewFraC.viewOngoingFra(owner_id)
    return page.showResult(fras, owner_id, search_query=search_query, title="View Ongoing FRA", source="ongoing")


@view_fra_bp.route("/fund_raiser/view_fras_completed", methods=["GET"])
def view_fras_completed():
    owner_id = get_current_owner_id()
    if not owner_id:
        return redirect(url_for("login"))
    page = FundRaiserResultFraPg()
    search_query = request.args.get("q", "").strip()
    fras = page.searchFraHistory(search_query, owner_id) if search_query else page.viewFraHistory(owner_id)
    return page.showResult(fras, owner_id, search_query=search_query, title="View Completed FRA History", source="completed")


@view_fra_bp.route("/fund_raiser/view_fras/<int:fra_id>", methods=["GET", "POST"])
def view_fra_detail(fra_id):
    return FundRaisingActivityPg.suspendFra(fra_id)


@view_fra_bp.route("/fund_raiser/view_fras", methods=["GET"])
def view_all_fras():
    owner_id = get_current_owner_id()
    if not owner_id:
        return jsonify({"success": False, "data": []}), 401
    fras = FundRaiserResultFraPg().viewFra(owner_id)
    return jsonify({"success": True, "data": fras})
