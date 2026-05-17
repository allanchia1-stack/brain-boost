from flask import Blueprint, flash, redirect, session, url_for

logout_bp = Blueprint("logout_bp", __name__)


class LogOutPg:
    def userLogOut(self):
        # print("Executing LogOutPg.userLogOut()")
        session.clear()
        return True


@logout_bp.route("/logout", methods=["GET"])
def logout():
    page = LogOutPg()
    page.userLogOut()
    flash("You have been logged out.")
    return redirect(url_for("login"))
