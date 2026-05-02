from flask import render_template, request, redirect, url_for
from project_manager.controller.SuspendFrcC import SuspendFrcC


class SuspendFRCPg:
    def __init__(self):
        self.control = SuspendFrcC()

    def get(self, frc_id):
        return render_template("project_manager/suspend_frc.html", frc_id=frc_id)

    def post(self):
        frc_id = request.form.get("frc_id")
        if self.control.suspend_frc(frc_id):
            return redirect(url_for("view_frc"))
        return "Error suspending FRC", 400
