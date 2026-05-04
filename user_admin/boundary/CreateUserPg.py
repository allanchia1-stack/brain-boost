from flask import request, render_template, redirect, url_for
from user_admin.controller.CreateUserC import CreateUserC

class CreateUserPg:
    def __init__(self):
        self.control = CreateUserC()

    def get(self):
        return render_template("user_admin/create_user.html")

    def post(self):
        name = request.form.get("name")
        phone = request.form.get("phone")
        address = request.form.get("address")
        role = request.form.get("role")
        email = request.form.get("email")
        password = request.form.get("password")
        
        if self.control.create_user(name, phone, address, role, email, password):
            return redirect(url_for("home"))
        return "Error creating user", 400