from flask import redirect, render_template, request, url_for

from project_manager.controller.UpdateFrcC import UpdateFrcC


class UpdateFrcPg:
    def __init__(self):
        self.control = UpdateFrcC()

    def get(self, frc_id):
        frc = self.control.get_frc_by_id(frc_id)
        if frc is None:
            return "Fund raising category not found", 404
        return render_template("project_manager/update_frc.html", frc=frc)

    def post(self, frc_id):
        action = request.form.get("action", "update")
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        try:
            status = int(request.form.get("status", "1"))
        except ValueError:
            status = -1

        if self.control.handle_action(frc_id, action, name, description, status):
            return redirect(url_for("view_frc"))

        frc = self.control.get_frc_by_id(frc_id)
        return render_template("project_manager/update_frc.html", frc=frc), 400
