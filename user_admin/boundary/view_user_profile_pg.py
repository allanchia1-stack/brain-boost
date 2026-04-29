from flask import Blueprint, render_template, request, jsonify
from user_admin.controller.view_user_profile_c import ViewUserProfileController

view_user_profile_bp = Blueprint("view_user_profile_bp", __name__)


@view_user_profile_bp.route("/user_admin/view_user_profiles_page", methods=["GET"])
def view_user_profiles_page():
    search_query = request.args.get("q", "").strip()

    if search_query:
        profiles = ViewUserProfileController.search_user_profiles(search_query)
    else:
        profiles = ViewUserProfileController.view_all_user_profiles()

    return render_template("view_user_profiles.html", profiles=profiles, search_query=search_query)


@view_user_profile_bp.route("/user_admin/view_user_profiles/<int:profile_id>", methods=["GET"])
def view_user_profile_detail(profile_id):
    profile = ViewUserProfileController.view_user_profile_by_id(profile_id)

    if profile is None:
        return "Profile not found", 404

    return render_template("view_user_profile_detail.html", profile=profile)


@view_user_profile_bp.route("/user_admin/view_user_profiles", methods=["GET"])
def view_all_user_profiles():
    profiles = ViewUserProfileController.view_all_user_profiles()
    return jsonify({"success": True, "data": profiles})
