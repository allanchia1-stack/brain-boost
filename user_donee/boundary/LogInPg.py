from flask import request, render_template
from user_donee.controller.LogInC import LogInC


class LogInPg:
    def __init__(self):
        self.control = LogInC()

    def get(self):
        return render_template("user_donee/login.html", error=None, email=""), 200

    def post(self):
        username = request.form.get("email", "").strip()
        password_hash = request.form.get("password", "").strip()

        result = self.control.userLogin(username, password_hash)
        if result.success:
            return result, None, 200

        return (
            result,
            render_template("user_donee/login.html", email=username, error=result.message),
            401,
        )
