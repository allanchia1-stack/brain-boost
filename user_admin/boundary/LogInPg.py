from flask import request, render_template
from user_admin.controller.LogInC import LogInC


class LogInPg:
    def __init__(self):
        self.control = LogInC()

    def get(self):
        return render_template("login.html", email="", error=""), 200

    def post(self):
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        result = self.control.authenticate(email, password)
        if result.success:
            return result, None, 200

        return result, render_template("login.html", email=email, error=result.message), 401
