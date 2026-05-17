from user_admin.controller.UserAdminLoginC import UserAdminLoginC, LogInResult
from user_admin.entity.UserAcct import UserAcct

#class LogInC(UserAdminLoginC):
#    pass

class LogInC():

    @staticmethod
    def userLogIn(username, password_hash):
        # print("Executing LogInC.userLogIn()")
        normalized_email = username.strip().lower()
        cleaned_password = password_hash or ""
        if not normalized_email or not cleaned_password:
            return LogInResult(False, "Email and password are required.")
        account = UserAcct.userLogIn(normalized_email, cleaned_password)
        if account is None:
            return LogInResult(False, "Invalid email or password.")
        return LogInResult(True, "Login successful.", account.id, account.email, account.role)