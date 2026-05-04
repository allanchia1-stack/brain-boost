from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from user_admin.controller.UserAdminViewProfileC import UserAdminViewProfileC
from user_admin.controller.UserAdminSearchProfileC import UserAdminSearchProfileC
from user_admin.controller.UserAdminUpdateProfileC import UserAdminUpdateProfileC
from user_admin.controller.UserAdminSuspendProfileC import UserAdminSuspendProfileC
from user_admin.entity.UserProf import UserProf

view_user_profile_bp = Blueprint("view_user_profile_bp", __name__)


class UserAdminResultUserProfilePg:
    def getSearchUPKey(self):
        return request.args.get("q", "").strip()

    def view_all(self):
        return UserAdminViewProfileC.view_all_user_profiles()

    def search(self, search_query):
        return UserAdminSearchProfileC.searchUserProfile(search_query)

    # Boundary method for the sequence diagram:
    # UserAdminResultUserProfilePg.view(profile_id) -> UserAdminViewProfileC.view(profile_id) -> UserProf.view(profile_id)
    def view(self, profile_id):
        return UserAdminViewProfileC.view(profile_id)

    def showResult(self, profiles, search_query=""):
        return render_template(
            "user_admin/view_user_profiles.html",
            profiles=profiles,
            search_query=search_query,
        )


class UserAdminUpdateUserProfilePg:
    def updateUserForm(self, profile, success=False):
        return render_template(
            "user_admin/view_user_profile_detail.html",
            profile=profile,
            success=success,
        )


class UserAdminUserProfilePg:
    def updateUserProfile(self, profile_id, role):
        return UserAdminUpdateProfileC.updateUser(UserProf(role=role, profile_id=profile_id))

    def SuspendUserProfile(self, profile_id):
        return UserAdminSuspendProfileC.SuspendUserProfile(profile_id)


@view_user_profile_bp.route("/user_admin/view_user_profiles_page", methods=["GET"])
def view_user_profiles_page():
    page = UserAdminResultUserProfilePg()
    search_query = page.getSearchUPKey()
    profiles = page.search(search_query) if search_query else page.view_all()
    return page.showResult(profiles, search_query)


@view_user_profile_bp.route("/user_admin/view_user_profiles/<int:profile_id>", methods=["GET", "POST"])
def view_user_profile_detail(profile_id):
    success = False
    action_page = UserAdminUserProfilePg()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "toggle_suspend":
            action_page.SuspendUserProfile(profile_id)
            return redirect(url_for("view_user_profile_bp.view_user_profile_detail", profile_id=profile_id))

        if action == "update":
            role = request.form.get("role", "").strip()
            action_page.updateUserProfile(profile_id, role)
            success = True

    profile = UserAdminResultUserProfilePg().view(profile_id)
    if profile is None:
        return "Profile not found", 404

    return UserAdminUpdateUserProfilePg().updateUserForm(profile, success)


@view_user_profile_bp.route("/user_admin/view_user_profiles", methods=["GET"])
def view_all_user_profiles():
    profiles = UserAdminResultUserProfilePg().view_all()
    return jsonify({"success": True, "data": profiles})
