from flask import Flask
from user_admin.boundary.view_user_profile_pg import view_user_profile_bp
from user_admin.entity.user_profile import UserProfile

app = Flask(__name__)

UserProfile.configure_database(app)

with app.app_context():
    UserProfile.create_tables()
    UserProfile.seed_data()

app.register_blueprint(view_user_profile_bp)


@app.route("/")
def home():
    return """
    <h1>User Admin Home</h1>
    <button onclick="window.location.href='/user_admin/view_user_profiles_page'">
    View User Profiles
    </button>
    """


if __name__ == "__main__":
    app.run(debug=True)