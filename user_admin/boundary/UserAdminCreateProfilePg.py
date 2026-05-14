from flask import request, render_template, redirect, url_for
from user_admin.controller.UserAdminCreateProfileC import UserAdminCreateProfileC
from user_admin.entity.UserProf import UserProf


class UserAdminCreateProfilePg:
    def __init__(self):
        self.control = UserAdminCreateProfileC()

    def displayProfileCreationForm(self):
        return render_template("user_admin/create_profile.html")

    def get(self):
        return self.displayProfileCreationForm()

    def createProfile(self, temp):
        #print("Running UserAdminCreateProfilePg.createProfile()")
        return self.control.createProfile(temp)

    def post(self):
        role = request.form.get("role", "").strip()
        status = int(request.form.get("status", "1"))
        if not role:
            return "Profile role cannot be empty", 400
        temp = UserProf(role=role, status=status)
        if self.createProfile(temp):
            return redirect(url_for("view_user_profile_bp.view_user_profiles_page"))
        return "Error creating profile. This profile may already exist.", 400
