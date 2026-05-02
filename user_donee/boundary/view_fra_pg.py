from flask import Blueprint, render_template, session, redirect, url_for, request, abort
from user_donee.controller.view_frac import ViewFRAC

view_fra_bp = Blueprint("donee_view_fra_bp", __name__)
control = ViewFRAC()


def require_donee():
    if session.get("role") != "Donee":
        return False
    return True


@view_fra_bp.route("/view-fra")
def view_fra_page():
    if not require_donee():
        return redirect(url_for("login"))

    search_query = request.args.get("q", "").strip()
    fra_data = control.get_all_fras(
        user_id=session.get("user_id"),
        search_query=search_query
    )
    return render_template(
        "user_donee/donee_viewfra.html",
        fras=fra_data,
        search_query=search_query,
        page_title="View FRA",
        heading="View FRA"
    )


@view_fra_bp.route("/view-fra/<int:fra_id>")
def view_fra_detail_page(fra_id):
    if not require_donee():
        return redirect(url_for("login"))

    fra = control.get_fra_by_id(fra_id, user_id=session.get("user_id"))
    if not fra:
        abort(404)

    return render_template("user_donee/donee_viewfra_detail.html", fra=fra)


@view_fra_bp.route("/view-fra/<int:fra_id>/toggle-save", methods=["POST"])
def toggle_save_fra(fra_id):
    if not require_donee():
        return redirect(url_for("login"))

    control.toggle_favourite(session.get("user_id"), fra_id)
    return redirect(request.referrer or url_for("donee_view_fra_bp.view_fra_detail_page", fra_id=fra_id))


@view_fra_bp.route("/favourite-fra")
def favourite_fra_page():
    if not require_donee():
        return redirect(url_for("login"))

    search_query = request.args.get("q", "").strip()
    fra_data = control.get_favourite_fras(
        user_id=session.get("user_id"),
        search_query=search_query
    )
    return render_template(
        "user_donee/donee_viewfra.html",
        fras=fra_data,
        search_query=search_query,
        page_title="Your Favourited FRA",
        heading="Your Favourited FRA"
    )


@view_fra_bp.route("/fra-history")
def fra_history_page():
    if not require_donee():
        return redirect(url_for("login"))

    search_query = request.args.get("q", "").strip()
    history = control.get_fra_history(
        user_id=session.get("user_id"),
        search_query=search_query
    )
    return render_template(
        "user_donee/donee_fra_history.html",
        history=history,
        search_query=search_query
    )


@view_fra_bp.route("/fra-history/<int:donation_id>")
def fra_history_detail_page(donation_id):
    if not require_donee():
        return redirect(url_for("login"))

    history = control.get_fra_history(user_id=session.get("user_id"))
    selected = next((item for item in history if item["donation_id"] == donation_id), None)
    if not selected:
        abort(404)

    return render_template("user_donee/donee_fra_history_detail.html", item=selected)
