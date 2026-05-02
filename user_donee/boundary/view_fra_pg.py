from flask import Blueprint, render_template, session, redirect, url_for
from user_donee.controller.view_frac import ViewFRAC

view_fra_bp = Blueprint("donee_view_fra_bp", __name__)
control = ViewFRAC()

@view_fra_bp.route("/view-fra")
def view_fra_page():
    # Security Check: Ensure only logged-in Donees can view this page
    if session.get("role") != "Donee":
        return redirect(url_for("login"))
    
    # Grab the data from the controller
    fra_data = control.get_all_fras()
    
    # Render the HTML template, passing the data into the 'fras' variable
    return render_template("user_donee/donee_viewfra.html", fras=fra_data)