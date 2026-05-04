from flask import request, render_template
from user_admin.controller.LogInC import LogInC

class LogInPg:
    def __init__(self):
        self.control = LogInC()

    def get(self):
        # Pass empty/None values for the initial page load
        return render_template('user_admin/login.html', error=None, email=""), 200

    def post(self):
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        result = self.control.authenticate(email, password)
        if result.success:
            return result, None, 200

        # Pass the actual attempted email and error message back to the template
        return result, render_template("user_admin/login.html", email=email, error=result.message), 401