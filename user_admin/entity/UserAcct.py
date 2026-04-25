from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db


class UserAcct(db.Model):
    __tablename__ = "user_accounts"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")

    @classmethod
    def seed_data(cls):
        demo_accounts = [
            ("admin@email.com", "admin123", "user admin"),
            ("fr@email.com", "fund123", "fund raiser"),
            ("donee@email.com", "donee123", "donee"),
        ]

        for email, password, role in demo_accounts:
            if cls.query.filter_by(email=email).first() is None:
                db.session.add(
                    cls(
                        email=email,
                        password_hash=generate_password_hash(password),
                        role=role,
                    )
                )

        db.session.commit()

    @classmethod
    def authenticate(cls, email, password):
        account = cls.query.filter_by(email=email).first()

        if account and check_password_hash(account.password_hash, password):
            return account

        return None
