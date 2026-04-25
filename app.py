from flask import Flask, flash, redirect, request, session, url_for
from user_admin.boundary.LogInPg import LogInPg
from user_admin.boundary.LogOutPg import logout_bp
from user_admin.boundary.view_user_profile_pg import view_user_profile_bp
from user_admin.entity.UserAcct import UserAcct
from user_admin.entity.user_profile import UserProfile

app = Flask(__name__, template_folder="user_admin/boundary")
app.secret_key = "dev-secret-key"

UserProfile.configure_database(app)

with app.app_context():
    UserProfile.create_tables()
    UserProfile.seed_data()
    UserAcct.seed_data()

app.register_blueprint(logout_bp)
app.register_blueprint(view_user_profile_bp)

login_page = LogInPg()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        result, response, status_code = login_page.post()
        if result and result.success:
            session["user_id"] = result.user_id
            session["email"] = result.email
            session["role"] = result.role
            flash(result.message)
            return redirect(url_for("home"))
        return response, status_code
    return login_page.get()


@app.route("/home")
def home():
    return f"""
    <h1>Welcome to HelpFundUs!</h1>
    <button onclick="window.location.href='{url_for("view_user_profile_bp.view_user_profiles_page")}'">
    View User Profile
    </button>
    """
    
if __name__ == "__main__":
    app.run(debug=True)
