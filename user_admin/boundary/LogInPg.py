from flask import request, render_template
from user_admin.controller.LogInC import LogInC


class LogInPg:
    def __init__(self):
        self.control = LogInC()

    def get(self):
        return render_template("user_admin/login.html", error=None, email=""), 200

    def userLogIn(self, username, password_hash):
        # print("Executing LogInPg.userLogIn()")
        return self.control.userLogIn(username, password_hash)

    def post(self):
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        result = self.userLogIn(email, password)
        if result.success:
            return result, None, 200
        return result, render_template("user_admin/login.html", email=email, error=result.message), 401
