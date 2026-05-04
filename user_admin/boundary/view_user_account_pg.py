from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from user_admin.controller.UserAdminViewAccountC import UserAdminViewAccountC
from user_admin.controller.UserAdminSearchAccountC import UserAdminSearchAccountC
from user_admin.controller.UserAdminUpdateAccountC import UserAdminUpdateAccountC
from user_admin.controller.UserAdminSuspendAccountC import UserAdminSuspendAccountC
from user_admin.entity.UserAcct import UserAcct
from user_admin.entity.UserProf import UserProf

view_user_account_bp = Blueprint("view_user_account_bp", __name__)


class UserAdminResultUserAccountPg:
    def getSearchUAKey(self):
        return request.args.get("q", "").strip()

    def view_all(self):
        return UserAdminViewAccountC.view_all_user_accounts()

    def search(self, search_query):
        return UserAdminSearchAccountC.searchUserAccount(search_query)

    def view(self, user_id):
        return UserAdminViewAccountC.view(user_id)

    def showResult(self, accounts, search_query=""):
        return render_template(
            "user_admin/view_user_accounts.html",
            accounts=accounts,
            search_query=search_query,
        )


class UserAdminUpdateUserAccountPg:
    def updateUserForm(self, account, success=False):
        profiles = [p for p in UserProf.get_all_profiles() if int(p.get("profile_status", 1)) == 1]
        return render_template(
            "user_admin/view_user_account_detail.html",
            account=account,
            success=success,
            profiles=profiles,
        )


class UserAccountPg:
    def updateUserAccount(self, user_id, email, password=None, name=None, phone=None, address=None, role=None):
        account = UserAcct(
            account_id=user_id,
            email=email,
            password=password,
            name=name,
            phone=phone,
            address=address,
            role=role,
        )
        return UserAdminUpdateAccountC.updateUser(account)

    def SuspendUserAccount(self, user_id):
        return UserAdminSuspendAccountC.SuspendUserAccount(user_id)


@view_user_account_bp.route("/user_admin/view_user_accounts_page", methods=["GET"])
def view_user_accounts_page():
    page = UserAdminResultUserAccountPg()
    search_query = page.getSearchUAKey()
    accounts = page.search(search_query) if search_query else page.view_all()
    return page.showResult(accounts, search_query)


@view_user_account_bp.route("/user_admin/view_user_accounts/<int:user_id>", methods=["GET", "POST"])
def view_user_account_detail(user_id):
    success = False
    action_page = UserAccountPg()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "toggle_suspend":
            action_page.SuspendUserAccount(user_id)
            return redirect(url_for("view_user_account_bp.view_user_account_detail", user_id=user_id))

        if action == "update":
            action_page.updateUserAccount(
                user_id=user_id,
                email=request.form.get("email", "").strip(),
                password=request.form.get("password", ""),
                name=request.form.get("name", "").strip(),
                phone=request.form.get("phone", "").strip(),
                address=request.form.get("address", "").strip(),
                role=request.form.get("role", "").strip(),
            )
            success = True

    account = UserAdminResultUserAccountPg().view(user_id)
    if account is None:
        return "Account not found", 404

    return UserAdminUpdateUserAccountPg().updateUserForm(account, success)


@view_user_account_bp.route("/user_admin/view_user_accounts", methods=["GET"])
def view_all_user_accounts():
    accounts = UserAdminResultUserAccountPg().view_all()
    return jsonify({"success": True, "data": accounts})
