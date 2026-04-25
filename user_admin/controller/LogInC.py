from dataclasses import dataclass
from user_admin.entity.UserAcct import UserAcct


@dataclass
class LogInResult:
    success: bool
    message: str
    user_id: int | None = None
    email: str | None = None
    role: str | None = None


class LogInC:
    @staticmethod
    def authenticate(email, password):
        normalized_email = email.strip().lower()
        cleaned_password = password or ""

        if not normalized_email or not cleaned_password:
            return LogInResult(
                success=False,
                message="Email and password are required.",
            )

        account = UserAcct.authenticate(normalized_email, cleaned_password)
        if account is None:
            return LogInResult(
                success=False,
                message="Invalid email or password.",
            )

        return LogInResult(
            success=True,
            message="Login successful.",
            user_id=account.id,
            email=account.email,
            role=account.role,
        )
