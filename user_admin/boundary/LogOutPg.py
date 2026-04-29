from flask import Blueprint, flash, redirect, session, url_for

logout_bp = Blueprint("logout_bp", __name__)

@logout_bp.route("/logout", methods=["GET"])
def logout():
    # Clear the session data
    session.clear()
    flash("You have been logged out.")
    # Route back to login page
    return redirect(url_for("login")) 