from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from user_admin.controller.view_user_account_c import ViewUserAccountController
from user_admin.entity.UserProf import UserProf

view_user_account_bp = Blueprint("view_user_account_bp", __name__)


class UserAdminResultUserAccountPg:
    def displaySearchUAForm(self):
        return render_template("user_admin/view_user_accounts.html", accounts=[], search_query="")

    def getSearchUAKey(self):
        return request.args.get("q", "").strip()

    def showSearchUAResult(self, account):
        return render_template("user_admin/view_user_accounts.html", accounts=account, search_query=self.getSearchUAKey())


class UserAdminUpdateUserAccountPg:
    def updateUserForm(self, account, success=False):
        profiles = [p for p in UserProf.get_all_profiles() if int(p.get("profile_status", 1)) == 1]
        return render_template("user_admin/view_user_account_detail.html", account=account, success=success, profiles=profiles)


class UserAccountPg:
    def SuspendUserAccount(self, idNum):
        return ViewUserAccountController.toggle_suspend_user_account(idNum)


@view_user_account_bp.route("/user_admin/view_user_accounts_page", methods=["GET"])
def view_user_accounts_page():
    page = UserAdminResultUserAccountPg()
    search_query = page.getSearchUAKey()
    if search_query:
        accounts = ViewUserAccountController.search_user_accounts(search_query)
    else:
        accounts = ViewUserAccountController.view_all_user_accounts()
    return render_template("user_admin/view_user_accounts.html", accounts=accounts, search_query=search_query)


@view_user_account_bp.route("/user_admin/view_user_accounts/<int:user_id>", methods=["GET", "POST"])
def view_user_account_detail(user_id):
    success = False
    if request.method == "POST":
        action = request.form.get("action")
        if action == "toggle_suspend":
            UserAccountPg().SuspendUserAccount(user_id)
            return redirect(url_for("view_user_account_bp.view_user_account_detail", user_id=user_id))
        if action == "update":
            ViewUserAccountController.update_user_account(
                user_id=user_id,
                email=request.form.get("email", "").strip(),
                password=request.form.get("password", ""),
                name=request.form.get("name", "").strip(),
                phone=request.form.get("phone", "").strip(),
                address=request.form.get("address", "").strip(),
                role=request.form.get("role", "").strip(),
            )
            success = True
    account = ViewUserAccountController.view_user_account_by_id(user_id)
    if account is None:
        return "Account not found", 404
    return UserAdminUpdateUserAccountPg().updateUserForm(account, success)


@view_user_account_bp.route("/user_admin/view_user_accounts", methods=["GET"])
def view_all_user_accounts():
    accounts = ViewUserAccountController.view_all_user_accounts()
    return jsonify({"success": True, "data": accounts})
