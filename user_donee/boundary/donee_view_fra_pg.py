from flask import Blueprint, render_template, request, session, redirect, url_for
from user_donee.controller.donee_search_fra_c import DoneeSearchFraC
from user_donee.controller.donee_view_fra_c import DoneeViewFraC


donee_view_fra_bp = Blueprint("donee_view_fra_bp", __name__)
search_control = DoneeSearchFraC()
view_control = DoneeViewFraC()


def donee_only():
    return session.get("role") == "Donee"


@donee_view_fra_bp.route("/donee/view-fra", methods=["GET"])
def view_fra_page():
    if not donee_only():
        return redirect(url_for("login"))

    search_query = request.args.get("q", "").strip()
    fras = search_control.search_fra(search_query)
    return render_template(
        "user_donee/donee_viewfra.html",
        fras=fras,
        search_query=search_query,
        page_title="View FRA",
        table_title="View FRA"
    )


@donee_view_fra_bp.route("/donee/view-fra/<int:fra_id>", methods=["GET"])
def view_fra_detail_page(fra_id):
    if not donee_only():
        return redirect(url_for("login"))

    fra, saved = view_control.view_fra(fra_id, session["user_id"])
    if fra is None:
        return redirect(url_for("donee_view_fra_bp.view_fra_page"))

    return render_template(
        "user_donee/donee_viewfra_detail.html",
        fra=fra,
        saved=saved
    )
