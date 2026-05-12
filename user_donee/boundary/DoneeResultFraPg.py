from flask import Blueprint, render_template, request, session, redirect, url_for
from user_donee.controller.DoneeSearchFraC import DoneeSearchFraC
from user_donee.controller.DoneeViewFraC import DoneeViewFraC
from user_donee.controller.DoneeViewFraFavC import DoneeViewFraFavC


donee_view_fra_bp = Blueprint("donee_view_fra_bp", __name__)
donee_view_fav_fra_bp = Blueprint("donee_view_fav_fra_bp", __name__)


class DoneeResultFraPg:
    def __init__(self):
        self.search_fra_control = DoneeSearchFraC()
        self.view_fra_control = DoneeViewFraC()
        self.view_fav_control = DoneeViewFraFavC()

    def doneeOnly(self):
        return session.get("role") == "Donee"

    def getSearchFraKey(self):
        return request.args.get("q", "").strip()

    def searchFra(self, query):
        print("Executing DoneeResultFraPg.searchFra()")
        return self.search_fra_control.searchFra(query)

    def view(self, fra_id, user_id):
        print("Executing DoneeResultFraPg.view()")
        return self.view_fra_control.view(fra_id, user_id)

    def doneeViewFavFra(self, fra_id):
        print("Executing DoneeResultFraPg.doneeViewFavFra()")
        return self.view_fav_control.doneeViewFavFra(fra_id)

    def viewFraFav(self, user_id):
        print("Executing DoneeResultFraPg.viewFraFav()")
        return self.view_fav_control.viewFraFav(user_id)

    def searchFraFav(self, user_id, query):
        print("Executing DoneeResultFraPg.searchFraFav()")
        return self.view_fav_control.searchFraFav(user_id, query)

    def showResult(self, fras, search_query="", page_title="View FRA", table_title="View FRA", source="all"):
        return render_template(
            "user_donee/donee_viewfra.html",
            fras=fras,
            search_query=search_query,
            page_title=page_title,
            table_title=table_title,
            source=source,
        )

    def showDetail(self, fra, saved, source="all"):
        return render_template(
            "user_donee/donee_viewfra_detail.html",
            fra=fra,
            saved=saved,
            source=source,
        )


@donee_view_fra_bp.route("/donee/view-fra", methods=["GET"])
def view_fra_page():
    page = DoneeResultFraPg()
    if not page.doneeOnly():
        return redirect(url_for("login"))

    query = page.getSearchFraKey()
    fras = page.searchFra(query)
    return page.showResult(fras, query, "View FRA", "View FRA", "all")


@donee_view_fra_bp.route("/donee/view-fra/<int:fra_id>", methods=["GET"])
def view_fra_detail_page(fra_id):
    page = DoneeResultFraPg()
    if not page.doneeOnly():
        return redirect(url_for("login"))

    source = request.args.get("source", "all").strip() or "all"
    fra, saved = page.view(fra_id, session["user_id"])
    if fra is None:
        if source == "favourited":
            return redirect(url_for("donee_view_fav_fra_bp.view_fav_fra_page"))
        return redirect(url_for("donee_view_fra_bp.view_fra_page"))

    return page.showDetail(fra, saved, source)


@donee_view_fav_fra_bp.route("/donee/favourited-fra", methods=["GET"])
def view_fav_fra_page():
    page = DoneeResultFraPg()
    if not page.doneeOnly():
        return redirect(url_for("login"))

    query = page.getSearchFraKey()
    fras = page.searchFraFav(session["user_id"], query) if query else page.viewFraFav(session["user_id"])
    return page.showResult(fras, query, "Favourited FRA", "Your Favourited FRA", "favourited")
