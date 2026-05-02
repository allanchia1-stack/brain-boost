from dataclasses import dataclass
from user_donee.entity.UserAcct import UserAcct


@dataclass
class LogInResult:
    success: bool
    message: str
    user_id: int | None = None
    email: str | None = None
    role: str | None = None


class LogInC:
    @staticmethod
    def userLogin(username, password_hash):
        username = (username or "").strip().lower()
        password_hash = password_hash or ""

        if not username or not password_hash:
            return LogInResult(False, "Username and password are required.")

        account = UserAcct.userLogin(username, password_hash)
        if account is None:
            return LogInResult(False, "Invalid Donee username or password.")

        return LogInResult(
            success=True,
            message="Donee login successful.",
            user_id=account.id,
            email=account.email,
            role=account.role,
        )

    @staticmethod
    def authenticate(email, password):
        return LogInC.userLogin(email, password)
