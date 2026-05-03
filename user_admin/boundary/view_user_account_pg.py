from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from user_admin.controller.view_user_account_c import ViewUserAccountController

view_user_account_bp = Blueprint("view_user_account_bp", __name__)


@view_user_account_bp.route("/user_admin/view_user_accounts_page", methods=["GET"])
def view_user_accounts_page():
    search_query = request.args.get("q", "").strip()
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
            ViewUserAccountController.toggle_suspend_user_account(user_id)
            return redirect(url_for("view_user_account_bp.view_user_account_detail", user_id=user_id))

        if action == "update":
            email    = request.form.get("email", "").strip()
            password = request.form.get("password", "").strip()
            ViewUserAccountController.update_user_account(user_id, email, password)
            success = True

    account = ViewUserAccountController.view_user_account_by_id(user_id)
    if account is None:
        return "Account not found", 404
    return render_template("user_admin/view_user_account_detail.html", account=account, success=success)


@view_user_account_bp.route("/user_admin/view_user_accounts", methods=["GET"])
def view_all_user_accounts():
    accounts = ViewUserAccountController.view_all_user_accounts()
    return jsonify({"success": True, "data": accounts})
