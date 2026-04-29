from flask import Flask, flash, redirect, request, session, url_for, render_template
from user_admin.boundary.LogInPg import LogInPg
from user_admin.boundary.LogOutPg import logout_bp
from user_admin.boundary.view_user_profile_pg import view_user_profile_bp
from user_admin.boundary.view_user_account_pg import view_user_account_bp
from user_admin.boundary.CreateUserPg import CreateUserPg

# Pointer for flask to the boundary folder for HTML files
app = Flask(__name__, template_folder="user_admin/boundary")
app.secret_key = "dev-secret-key"

# Register Blueprints
app.register_blueprint(logout_bp)
app.register_blueprint(view_user_profile_bp)
app.register_blueprint(view_user_account_bp)

# Instantiate the boundary
login_page = LogInPg()
create_user_page = CreateUserPg()


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
        return render_template("admin_dashboard.html", admin_identifier=email)
    elif role == "Donee":
        return render_template("user-donee/donee_dashboard.html", user_name=email)
    elif role == "FundRaiser":
        return render_template("fundraiser_dashboard.html", user_name=email)
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


if __name__ == "__main__":
    app.run(debug=True)
