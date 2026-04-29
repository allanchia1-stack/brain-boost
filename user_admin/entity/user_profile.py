from datetime import datetime
from extensions import db


class UserProfile(db.Model):
    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default="active", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def configure_database(cls, app):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fundraising.db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)

    @classmethod
    def create_tables(cls):
        db.create_all()

    @classmethod
    def seed_data(cls):
        if not cls.query.first():
            profiles = [
                cls(full_name="Admin User", email="admin@email.com", role="user admin"),
                cls(full_name="Fund Raiser User", email="fr@email.com", role="fund raiser"),
                cls(full_name="Donee User", email="donee@email.com", role="donee"),
            ]
            db.session.add_all(profiles)
            db.session.commit()

    @classmethod
    def get_all_profiles(cls):
        return cls.query.all()

    @classmethod
    def get_profile_by_id(cls, profile_id):
        return cls.query.get(profile_id)