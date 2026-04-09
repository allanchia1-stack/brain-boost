from flask import Flask
from extensions import db
from user_admin.boundary.view_user_profiles_pg import view_user_profiles_bp
from user_admin.entity.user_profiles import UserProfiles

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fundraising.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(view_user_profiles_bp)


@app.route("/")
def home():
    return """
    <h1>User Admin Home</h1>
    <button onclick="window.location.href='/user_admin/view_user_profiles_page'">
        View User Profiles
    </button>
    """


@app.route("/setup")
def setup():
    db.create_all()

    if not UserProfiles.query.first():
        profiles = [
            UserProfiles(full_name="Admin User", email="admin@email.com", role="user admin"),
            UserProfiles(full_name="Fund Raiser User", email="fr@email.com", role="fund raiser"),
            UserProfiles(full_name="Donee User", email="donee@email.com", role="donee"),
        ]
        db.session.add_all(profiles)
        db.session.commit()

    return "Setup complete"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)