from flask import Blueprint, session, redirect, url_for
from user_donee.controller.DoneeSaveFraFavC import DoneeSaveFraFavC


donee_save_fra_bp = Blueprint("donee_save_fra_bp", __name__)


class DoneeFraPg:
    def __init__(self):
        self.control = DoneeSaveFraFavC()

    def doneeOnly(self):
        return session.get("role") == "Donee"

    def saveFra(self, user_id, fra_id):
        print("Executing DoneeFraPg.saveFra()")
        return self.control.saveFra(user_id, fra_id)


@donee_save_fra_bp.route("/donee/save-fra/<int:fra_id>", methods=["POST"])
def toggle_save_fra(fra_id):
    page = DoneeFraPg()
    if not page.doneeOnly():
        return redirect(url_for("login"))

    page.saveFra(session["user_id"], fra_id)
    return redirect(url_for("donee_view_fra_bp.view_fra_detail_page", fra_id=fra_id))
