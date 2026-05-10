from flask import render_template, request, redirect, url_for
from project_manager.controller.CreateFrcC import PMCreateFrcC
from project_manager.entity.FRC import FRC

class PMCreateFrcPg:
    def __init__(self):
        self.control = PMCreateFrcC()

    def get(self):
        return render_template("project_manager/create_frc.html")

    def post(self):
        name        = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        status      = int(request.form.get("status", "1"))
        temp = FRC(name,description,status)
        if self.control.createFrc(temp):
            return redirect(url_for("view_frc"))
        return self.get(), 400
