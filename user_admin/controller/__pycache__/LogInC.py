from dataclasses import dataclass
from user_admin.entity.UserAcct import UserAcct

@dataclass
class LoginResult:
    success: bool
    user_id: int = None
    message: str = ""

class LogInC:

    def authenticate(self, email: str, password: str) -> LoginResult:
        
        user = UserAcct.find_by_email(email)

        if user is None:
            return LoginResult(
                success=False,
                message="Invalid email or password."
            )

        if not user.verify_password(password):
            return LoginResult(
                success=False,
                message="Invalid email or password."
            )

        if not user.is_active:
            return LoginResult(
                success=False,
                message="Your account has been deactivated. Please contact support."
            )

        return LoginResult(
            success=True,
            user_id=user.id
        )