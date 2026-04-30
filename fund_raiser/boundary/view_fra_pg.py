from flask import Blueprint, jsonify, render_template, request
from fund_raiser.controller.view_fra_c import ViewFRAController


view_fra_bp = Blueprint("view_fra_bp", __name__)


@view_fra_bp.route("/fund_raiser/view_fras_page", methods=["GET"])
def view_fras_page():
    search_query = request.args.get("q", "").strip()

    if search_query:
        fras = ViewFRAController.search_fras(search_query)
    else:
        fras = ViewFRAController.view_all_fras()

    return render_template("view_fras.html", fras=fras, search_query=search_query)


@view_fra_bp.route("/fund_raiser/view_fras/<int:fra_id>", methods=["GET"])
def view_fra_detail(fra_id):
    fra = ViewFRAController.view_fra_by_id(fra_id)

    if fra is None:
        return "Fund raising activity not found", 404

    return render_template("view_fra_detail.html", fra=fra)


@view_fra_bp.route("/fund_raiser/view_fras", methods=["GET"])
def view_all_fras():
    fras = ViewFRAController.view_all_fras()
    return jsonify({"success": True, "data": fras})

