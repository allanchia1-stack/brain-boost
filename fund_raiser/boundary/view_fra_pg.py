from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from fund_raiser.controller.view_fra_c import ViewFRAController


view_fra_bp = Blueprint("view_fra_bp", __name__)


def get_current_owner_id():
    return session.get("user_id")


@view_fra_bp.route("/fund_raiser/view_fras_page", methods=["GET"])
def view_fras_page():
    owner_id = get_current_owner_id()
    if not owner_id:
        return redirect(url_for("login"))

    search_query = request.args.get("q", "").strip()

    if search_query:
        fras = ViewFRAController.search_fras(search_query, owner_id)
    else:
        fras = ViewFRAController.view_all_fras(owner_id)

    return render_template(
        "fund_raiser/view_fras.html",
        fras=fras,
        search_query=search_query,
        title="View Fund Raising Activities",
    )


@view_fra_bp.route("/fund_raiser/view_fras/<int:fra_id>", methods=["GET", "POST"])
def view_fra_detail(fra_id):
    owner_id = get_current_owner_id()
    if not owner_id:
        return redirect(url_for("login"))

    success = False
    error = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "suspend":
            ViewFRAController.suspend_fra(fra_id, owner_id)
            return redirect(url_for("view_fra_bp.view_fras_page"))

        if action == "update":
            success, error = ViewFRAController.update_fra_from_form(fra_id, request.form, owner_id)

    fra = ViewFRAController.view_fra_by_id(fra_id, owner_id)
    categories = ViewFRAController.get_categories()

    if fra is None:
        return "Fund raising activity not found", 404

    return render_template(
        "fund_raiser/view_fra_detail.html",
        fra=fra,
        categories=categories,
        success=success,
        error=error,
    )

@view_fra_bp.route("/fund_raiser/view_fras_ongoing", methods=["GET"])
def view_fras_ongoing():
    owner_id = get_current_owner_id()
    if not owner_id:
        return redirect(url_for("login"))

    fras = ViewFRAController.view_ongoing_fras(owner_id)
    title = "View Ongoing FRA"
    return render_template("fund_raiser/view_fras.html", fras=fras, title=title, search_query="")

@view_fra_bp.route("/fund_raiser/view_fras_completed", methods=["GET"])
def view_fras_completed():
    owner_id = get_current_owner_id()
    if not owner_id:
        return redirect(url_for("login"))

    fras = ViewFRAController.view_completed_fras(owner_id)
    title = "View Completed FRA History"
    return render_template("fund_raiser/view_fras.html", fras=fras, title=title, search_query="")

@view_fra_bp.route("/fund_raiser/view_fras", methods=["GET"])
def view_all_fras():
    owner_id = get_current_owner_id()
    if not owner_id:
        return jsonify({"success": False, "data": []}), 401

    fras = ViewFRAController.view_all_fras(owner_id)
    return jsonify({"success": True, "data": fras})
