from flask import Blueprint, session, redirect, url_for
from user_donee.controller.donee_save_fra_fav_c import DoneeSaveFraFavC


donee_save_fra_bp = Blueprint("donee_save_fra_bp", __name__)
save_control = DoneeSaveFraFavC()


@donee_save_fra_bp.route("/donee/save-fra/<int:fra_id>", methods=["POST"])
def toggle_save_fra(fra_id):
    if session.get("role") != "Donee":
        return redirect(url_for("login"))

    save_control.toggle_save_fra(session["user_id"], fra_id)
    return redirect(url_for("donee_view_fra_bp.view_fra_detail_page", fra_id=fra_id))
