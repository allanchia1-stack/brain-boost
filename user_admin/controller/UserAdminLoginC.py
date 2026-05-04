from dataclasses import dataclass
from user_admin.entity.UserAcct import UserAcct


@dataclass
class LogInResult:
    success: bool
    message: str
    user_id: int | None = None
    email: str | None = None
    role: str | None = None


class UserAdminLoginC:
    @staticmethod
    def userLogin(username, password_hash):
        normalized_email = username.strip().lower()
        cleaned_password = password_hash or ""
        if not normalized_email or not cleaned_password:
            return LogInResult(False, "Email and password are required.")
        account = UserAcct.userLogin(normalized_email, cleaned_password)
        if account is None:
            return LogInResult(False, "Invalid email or password.")
        return LogInResult(True, "Login successful.", account.id, account.email, account.role)

    @staticmethod
    def authenticate(email, password):
        return UserAdminLoginC.userLogin(email, password)
