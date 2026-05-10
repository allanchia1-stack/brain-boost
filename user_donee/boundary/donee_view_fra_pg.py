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

    query = request.args.get("q", "").strip()
    print("Executing Donee Search FRA")
    fras = search_control.searchFra(query)
    return render_template(
        "user_donee/donee_viewfra.html",
        fras=fras,
        search_query=query,
        page_title="View FRA",
        table_title="View FRA",
        source="all",
    )


@donee_view_fra_bp.route("/donee/view-fra/<int:fra_id>", methods=["GET"])
def view_fra_detail_page(fra_id):
    if not donee_only():
        return redirect(url_for("login"))

    source = request.args.get("source", "all").strip() or "all"
    view_control.update_num_of_views(fra_id)
    fra, saved = view_control.viewFra(fra_id, session["user_id"])
    if fra is None:
        if source == "favourited":
            return redirect(url_for("donee_view_fav_fra_bp.view_fav_fra_page"))
        return redirect(url_for("donee_view_fra_bp.view_fra_page"))

    return render_template(
        "user_donee/donee_viewfra_detail.html",
        fra=fra,
        saved=saved,
        source=source,
    )
