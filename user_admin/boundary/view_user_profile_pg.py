from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from user_admin.controller.view_user_profile_c import ViewUserProfileController

view_user_profile_bp = Blueprint("view_user_profile_bp", __name__)


class UserAdminResultUserProfilePg:
    def displaySearchUPForm(self):
        return render_template("user_admin/view_user_profiles.html", profiles=[], search_query="")

    def getSearchUPKey(self):
        return request.args.get("q", "").strip()

    def showSearchUPResult(self, profile):
        return render_template("user_admin/view_user_profiles.html", profiles=profile, search_query=self.getSearchUPKey())


class UserAdminUpdateUserProfilePg:
    def updateUserForm(self, profile, success=False):
        return render_template("user_admin/view_user_profile_detail.html", profile=profile, success=success)


class UserAdminUserProfilePg:
    def SuspendUserProfile(self, profile_id):
        return ViewUserProfileController.toggle_suspend_user_profile(profile_id)


@view_user_profile_bp.route("/user_admin/view_user_profiles_page", methods=["GET"])
def view_user_profiles_page():
    page = UserAdminResultUserProfilePg()
    search_query = page.getSearchUPKey()
    if search_query:
        profiles = ViewUserProfileController.search_user_profiles(search_query)
    else:
        profiles = ViewUserProfileController.view_all_user_profiles()
    return render_template("user_admin/view_user_profiles.html", profiles=profiles, search_query=search_query)


@view_user_profile_bp.route("/user_admin/view_user_profiles/<int:profile_id>", methods=["GET", "POST"])
def view_user_profile_detail(profile_id):
    success = False
    if request.method == "POST":
        action = request.form.get("action")
        if action == "toggle_suspend":
            UserAdminUserProfilePg().SuspendUserProfile(profile_id)
            return redirect(url_for("view_user_profile_bp.view_user_profile_detail", profile_id=profile_id))
        if action == "update":
            role = request.form.get("role", "").strip()
            ViewUserProfileController.update_user_profile(profile_id, role)
            success = True
    profile = ViewUserProfileController.view_user_profile_by_id(profile_id)
    if profile is None:
        return "Profile not found", 404
    return UserAdminUpdateUserProfilePg().updateUserForm(profile, success)


@view_user_profile_bp.route("/user_admin/view_user_profiles", methods=["GET"])
def view_all_user_profiles():
    profiles = ViewUserProfileController.view_all_user_profiles()
    return jsonify({"success": True, "data": profiles})
