from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from fund_raiser.controller.view_fra_c import ViewFRAController


view_fra_bp = Blueprint("view_fra_bp", __name__)


@view_fra_bp.route("/fund_raiser/view_fras_page", methods=["GET"])
def view_fras_page():
    search_query = request.args.get("q", "").strip()

    if search_query:
        fras = ViewFRAController.search_fras(search_query)
    else:
        fras = ViewFRAController.view_all_fras()

    return render_template("fund_raiser/view_fras.html", fras=fras, search_query=search_query)


@view_fra_bp.route("/fund_raiser/view_fras/<int:fra_id>", methods=["GET", "POST"])
def view_fra_detail(fra_id):
    success = False
    error = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "suspend":
            ViewFRAController.suspend_fra(fra_id)
            return redirect(url_for("view_fra_bp.view_fras_page"))

        if action == "update":
            success, error = ViewFRAController.update_fra_from_form(fra_id, request.form)

    fra = ViewFRAController.view_fra_by_id(fra_id)
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
    fras = ViewFRAController.view_ongoing_fras()
    title = "View Ongoing FRA"
    return render_template("fund_raiser/view_fras.html", fras=fras, title=title)

@view_fra_bp.route("/fund_raiser/view_fras_completed", methods=["GET"])
def view_fras_completed():
    fras = ViewFRAController.view_completed_fras()
    title = "View Completed FRA History"
    return render_template("fund_raiser/view_fras.html", fras=fras, title=title)
    return render_template("fund_raiser/view_fras.html", fras=fras)

@view_fra_bp.route("/fund_raiser/view_fras", methods=["GET"])
def view_all_fras():
    fras = ViewFRAController.view_all_fras()
    return jsonify({"success": True, "data": fras})
