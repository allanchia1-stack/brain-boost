from flask import Blueprint, redirect, session, url_for


donee_logout_bp = Blueprint("donee_logout_bp", __name__)


@donee_logout_bp.route("/donee/logout")
def userLogOut():
    session.clear()
    return redirect(url_for("donee_login"))
