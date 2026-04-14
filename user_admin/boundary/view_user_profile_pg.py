from flask import Blueprint, jsonify, render_template_string
from user_admin.controller.view_user_profile_c import ViewUserProfileController

view_user_profile_bp = Blueprint("view_user_profile_bp", __name__)


@view_user_profile_bp.route("/user_admin/view_user_profiles_page", methods=["GET"])
def view_user_profiles_page():
    profiles = ViewUserProfileController.view_all_user_profiles()

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
                <td>{{ profile["id"] }}</td>
                <td>{{ profile["full_name"] }}</td>
                <td>{{ profile["email"] }}</td>
                <td>{{ profile["role"] }}</td>
                <td>{{ profile["status"] }}</td>
            </tr>
            {% endfor %}
        </table>

        <br>
        <button onclick="window.location.href='/'">
        Back to Home
        </button>
    </body>
    </html>
    """
    return render_template_string(html, profiles=profiles)


@view_user_profile_bp.route("/user_admin/view_user_profiles", methods=["GET"])
def view_all_user_profiles():
    profiles = ViewUserProfileController.view_all_user_profiles()
    return jsonify({
        "success": True,
        "data": profiles
    })


@view_user_profile_bp.route("/user_admin/view_user_profiles/<int:profile_id>", methods=["GET"])
def view_user_profile_by_id(profile_id):
    profile = ViewUserProfileController.view_user_profile_by_id(profile_id)

    if profile is None:
        return jsonify({
            "success": False,
            "message": "User profile not found"
        }), 404

    return jsonify({
        "success": True,
        "data": profile
    })