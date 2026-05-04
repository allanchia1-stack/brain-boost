from flask import request, render_template, redirect, url_for
from user_admin.controller.UserAdminCreateAccountC import UserAdminCreateAccountC
from user_admin.entity.UserAcct import UserAcct


class UserAdminCreateUserAccountPg:
    def __init__(self):
        self.control = UserAdminCreateAccountC()

    def displayAccountCreationForm(self):
        return render_template("user_admin/create_account.html")

    def get(self):
        return self.displayAccountCreationForm()

    def createAccount(self, tempAccount):
        return self.control.createAccount(tempAccount)

    def post(self):
        tempAccount = UserAcct(
            name=request.form.get("name", "").strip(),
            phone=request.form.get("phone", "").strip(),
            address=request.form.get("address", "").strip(),
            role=request.form.get("role", "").strip(),
            email=request.form.get("email", "").strip(),
            password=request.form.get("password", ""),
        )
        if self.createAccount(tempAccount):
            return redirect(url_for("view_user_account_bp.view_user_accounts_page"))
        return "Error creating account", 400
