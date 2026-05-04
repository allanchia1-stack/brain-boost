from flask import request, render_template, redirect, url_for
from user_admin.controller.UserAdminCreateProfileC import UserAdminCreateProfileC
from user_admin.entity.UserProf import UserProf


class UserAdminCreatePg:
    def __init__(self):
        self.control = UserAdminCreateProfileC()

    def displayProfileCreationForm(self):
        return render_template("user_admin/create_profile.html")

    def get(self):
        return self.displayProfileCreationForm()

    def createProfile(self, tempProfile):
        return self.control.createProfile(tempProfile)

    def post(self):
        role = request.form.get("role", "").strip()
        status = int(request.form.get("status", "1"))
        tempProfile = UserProf(role=role, status=status)
        if self.createProfile(tempProfile):
            return redirect(url_for("view_user_profile_bp.view_user_profiles_page"))
        return "Error creating profile", 400
