from flask import Flask, flash, redirect, request, session, url_for, render_template

# Admin Imports
from user_admin.boundary.LogInPg import LogInPg
from user_admin.boundary.LogOutPg import logout_bp
from user_admin.boundary.view_user_profile_pg import view_user_profile_bp
from user_admin.boundary.view_user_account_pg import view_user_account_bp
from user_admin.boundary.CreateUserPg import CreateUserPg

# FundRaiser Imports
from fund_raiser.boundary.CreateFRAPg import CreateFRAPg
from fund_raiser.boundary.view_fra_pg import view_fra_bp as fr_view_fra_bp

# Donee Imports
from user_donee.boundary.donee_view_fra_pg import donee_view_fra_bp
from user_donee.boundary.donee_save_fra_pg import donee_save_fra_bp
from user_donee.boundary.donee_view_fav_fra_pg import donee_view_fav_fra_bp
from user_donee.boundary.donee_donation_history_pg import donee_donation_history_bp
from user_donee.boundary.LogInPg import LogInPg as DoneeLogInPg
from user_donee.boundary.LogOutPg import donee_logout_bp

# Flask automatically looks for HTML files inside the root templates/ folder
app = Flask(__name__)
app.secret_key = "dev-secret-key"

# Register Blueprints
app.register_blueprint(logout_bp)
app.register_blueprint(view_user_profile_bp)
app.register_blueprint(view_user_account_bp)

# Registering the aliases so they don't overwrite each other
app.register_blueprint(fr_view_fra_bp)
app.register_blueprint(donee_view_fra_bp)
app.register_blueprint(donee_save_fra_bp)
app.register_blueprint(donee_view_fav_fra_bp)
app.register_blueprint(donee_donation_history_bp)
app.register_blueprint(donee_logout_bp)

# Instantiate the boundary
login_page = LogInPg()
create_user_page = CreateUserPg()
create_fra_page = CreateFRAPg()
donee_login_page = DoneeLogInPg()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        result, response, status_code = login_page.post()
        if result and result.success:
            session["user_id"] = result.user_id
            session["email"] = result.email
            session["role"] = result.role
            return redirect(url_for("home"))
        return response, status_code
    return login_page.get()


@app.route("/donee-login", methods=["GET", "POST"])
def donee_login():
    if request.method == "POST":
        result, response, status_code = donee_login_page.post()
        if result and result.success:
            session["user_id"] = result.user_id
            session["email"] = result.email
            session["role"] = result.role
            return redirect(url_for("home"))
        return response, status_code
    return donee_login_page.get()


@app.route("/home")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    role = session.get("role")
    email = session.get("email")

    if role == "Admin":
        return render_template("user_admin/admin_dashboard.html", admin_identifier=email)
    elif role == "Donee":
        return render_template("user_donee/donee_dashboard.html", user_name=email)
    elif role == "FundRaiser":
        return render_template("fund_raiser/fr_dashboard.html", user_name=email)
    else:
        return "Role not recognized or unauthorized."


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route("/create-user", methods=["GET", "POST"])
def create_user():
    if session.get("role") != "Admin":
        return redirect(url_for("home"))
    if request.method == "POST":
        return create_user_page.post()
    return create_user_page.get()


@app.route("/create-fra", methods=["GET", "POST"])
def create_fra():
    if session.get("role") != "FundRaiser":
        return redirect(url_for("home"))
    if request.method == "POST":
        return create_fra_page.post()
    return create_fra_page.get()


if __name__ == "__main__":
    app.run(debug=True)
