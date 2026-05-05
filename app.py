from flask import Flask, redirect, request, session, url_for, render_template

# User Admin imports
from user_admin.boundary.LogInPg import LogInPg
from user_admin.boundary.LogOutPg import logout_bp
from user_admin.boundary.UserAdminCreateProfilePg import UserAdminCreateProfilePg
from user_admin.boundary.UserAdminCreateUserAccountPg import UserAdminCreateUserAccountPg
from user_admin.boundary.UserAdminResultUserProfilePg import view_user_profile_bp
from user_admin.boundary.UserAdminResultUserAccountPg import view_user_account_bp

# Fund Raiser imports
from fund_raiser.boundary.CreateFRAPg import CreateFRAPg
from fund_raiser.boundary.view_fra_pg import view_fra_bp as fr_view_fra_bp

# Project Manager imports
from project_manager.boundary.CreateFrcPg import CreateFrcPg
from project_manager.boundary.ViewFraPg import ViewFraPg
from project_manager.boundary.ViewFrcPg import ViewFrcPg
from project_manager.boundary.UpdateFrcPg import UpdateFrcPg
from project_manager.boundary.DailyReportGenPg import DailyReportGenPg
from project_manager.boundary.WeeklyReportPg import WeeklyReportPg
from project_manager.boundary.MonthlyReportPg import MonthlyReportPg

# Donee imports
from user_donee.boundary.donee_view_fra_pg import donee_view_fra_bp
from user_donee.boundary.donee_save_fra_pg import donee_save_fra_bp
from user_donee.boundary.donee_view_fav_fra_pg import donee_view_fav_fra_bp
from user_donee.boundary.donee_donation_history_pg import donee_donation_history_bp

app = Flask(__name__)
app.secret_key = "dev-secret-key"

# Register blueprints
app.register_blueprint(logout_bp)
app.register_blueprint(view_user_profile_bp)
app.register_blueprint(view_user_account_bp)
app.register_blueprint(fr_view_fra_bp)
app.register_blueprint(donee_view_fra_bp)
app.register_blueprint(donee_save_fra_bp)
app.register_blueprint(donee_view_fav_fra_bp)
app.register_blueprint(donee_donation_history_bp)

# Boundary objects
login_page = LogInPg()
create_profile_page = UserAdminCreateProfilePg()
create_account_page = UserAdminCreateUserAccountPg()
create_fra_page = CreateFRAPg()
create_frc_page = CreateFrcPg()
view_frc_page = ViewFrcPg()
view_fra_page = ViewFraPg()
update_frc_page = UpdateFrcPg()
daily_report_page = DailyReportGenPg()
weekly_report_page = WeeklyReportPg()
monthly_report_page = MonthlyReportPg()


def role_required(role_name):
    return session.get("role") == role_name


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


@app.route("/home")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    role = session.get("role")
    email = session.get("email")

    if role == "Admin":
        return render_template("user_admin/admin_dashboard.html", admin_identifier=email)
    if role == "Donee":
        return render_template("user_donee/donee_dashboard.html", user_name=email)
    if role == "FundRaiser":
        return render_template("fund_raiser/fr_dashboard.html", user_name=email)
    if role == "Manager":
        return render_template("project_manager/manager_dashboard.html", manager_identifier=email)

    return "Role not recognized or unauthorized.", 403


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route("/create-user", methods=["GET", "POST"])
def create_user():
    return create_account()


@app.route("/user_admin/create_account", methods=["GET", "POST"])
def create_account():
    if not role_required("Admin"):
        return redirect(url_for("home"))
    if request.method == "POST":
        return create_account_page.post()
    return create_account_page.get()


@app.route("/user_admin/create_profile", methods=["GET", "POST"])
def create_profile():
    if not role_required("Admin"):
        return redirect(url_for("home"))
    if request.method == "POST":
        return create_profile_page.post()
    return create_profile_page.get()


@app.route("/create-fra", methods=["GET", "POST"])
def create_fra():
    if not role_required("FundRaiser"):
        return redirect(url_for("home"))
    if request.method == "POST":
        return create_fra_page.post()
    return create_fra_page.get()


@app.route("/project-manager/create-frc", methods=["GET", "POST"])
def create_frc():
    if not role_required("Manager"):
        return redirect(url_for("home"))
    if request.method == "POST":
        return create_frc_page.post()
    return create_frc_page.get()


@app.route("/project-manager/view-frc", methods=["GET"])
def view_frc():
    if not role_required("Manager"):
        return redirect(url_for("home"))
    return view_frc_page.get()


@app.route("/project-manager/frc/<int:frc_id>/edit", methods=["GET", "POST"])
def update_frc(frc_id):
    if not role_required("Manager"):
        return redirect(url_for("home"))
    if request.method == "POST":
        return update_frc_page.post(frc_id)
    return update_frc_page.get(frc_id)


@app.route("/project-manager/view-frc/<int:frc_id>/fras", methods=["GET"])
def view_fra_by_frc(frc_id):
    if not role_required("Manager"):
        return redirect(url_for("home"))
    return view_fra_page.get_by_category(frc_id)


@app.route("/project-manager/view-fras/<int:fra_id>", methods=["GET"])
def view_fra_detail(fra_id):
    if not role_required("Manager"):
        return redirect(url_for("home"))
    return view_fra_page.get_detail(fra_id)


@app.route("/project-manager/daily-report", methods=["GET", "POST"])
def daily_report():
    if not role_required("Manager"):
        return redirect(url_for("home"))
    if request.method == "POST":
        return daily_report_page.post()
    return daily_report_page.get()


@app.route("/project-manager/weekly-report", methods=["GET", "POST"])
def weekly_report():
    if not role_required("Manager"):
        return redirect(url_for("home"))
    if request.method == "POST":
        return weekly_report_page.post()
    return weekly_report_page.get()


@app.route("/project-manager/monthly-report", methods=["GET", "POST"])
def monthly_report():
    if not role_required("Manager"):
        return redirect(url_for("home"))
    if request.method == "POST":
        return monthly_report_page.post()
    return monthly_report_page.get()


if __name__ == "__main__":
    app.run(debug=True)
