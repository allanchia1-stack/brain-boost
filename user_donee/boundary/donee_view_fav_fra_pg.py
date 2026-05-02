from flask import Blueprint, render_template, request, session, redirect, url_for
from user_donee.controller.donee_view_fra_fav_c import DoneeViewFraFavC


donee_view_fav_fra_bp = Blueprint("donee_view_fav_fra_bp", __name__)
fav_control = DoneeViewFraFavC()


@donee_view_fav_fra_bp.route("/donee/favourited-fra", methods=["GET"])
def view_fav_fra_page():
    if session.get("role") != "Donee":
        return redirect(url_for("login"))

    search_query = request.args.get("q", "").strip()
    fras = fav_control.donee_search_fav_fra(session["user_id"], search_query)
    return render_template(
        "user_donee/donee_viewfra.html",
        fras=fras,
        search_query=search_query,
        page_title="Favourited FRA",
        table_title="Your Favourited FRA"
    )
