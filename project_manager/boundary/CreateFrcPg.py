from flask import render_template, request, redirect, url_for
from project_manager.controller.CreateFrcC import CreateFrcC


class CreateFrcPg:
    def __init__(self):
        self.control = CreateFrcC()

    def get(self):
        return render_template("project_manager/create_frc.html")

    def post(self):
        name        = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        status      = int(request.form.get("status", "1"))
        if self.control.create_frc(name, description, status):
            return redirect(url_for("view_frc"))
        return self.get(), 400
