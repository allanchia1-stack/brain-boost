from flask import Blueprint, jsonify, render_template_string
from user_admin.controller.view_user_profiles_c import ViewUserProfilesController

view_user_profiles_bp = Blueprint("view_user_profiles_bp", __name__)


@view_user_profiles_bp.route("/user_admin/view_user_profiles_page", methods=["GET"])
def view_user_profiles_page():
    profiles = ViewUserProfilesController.view_all_user_profiles()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>View User Profiles</title>
    </head>
    <body>
        <h1>View User Profiles</h1>

        <table border="1" cellpadding="8">
            <tr>
                <th>ID</th>
                <th>Full Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>Status</th>
            </tr>
            {% for profile in profiles %}
            <tr>
                <td>{{ profile.id }}</td>
                <td>{{ profile.full_name }}</td>
                <td>{{ profile.email }}</td>
                <td>{{ profile.role }}</td>
                <td>{{ profile.status }}</td>
            </tr>
            {% endfor %}
        </table>

        <br>
        <a href="/">Back to Home</a>
    </body>
    </html>
    """
    return render_template_string(html, profiles=profiles)


@view_user_profiles_bp.route("/user_admin/view_user_profiles", methods=["GET"])
def view_all_user_profiles():
    profiles = ViewUserProfilesController.view_all_user_profiles()
    return jsonify({
        "success": True,
        "data": profiles
    })


@view_user_profiles_bp.route("/user_admin/view_user_profiles/<int:profile_id>", methods=["GET"])
def view_user_profile_by_id(profile_id):
    profile = ViewUserProfilesController.view_user_profile_by_id(profile_id)

    if not profile:
        return jsonify({
            "success": False,
            "message": "User profile not found"
        }), 404

    return jsonify({
        "success": True,
        "data": profile
    })