from flask import render_template, request

from project_manager.boundary.PMSuspendFrcPg import PMSuspendFrcPg
from project_manager.controller.PMViewFrcC import PMViewFrcC
from project_manager.controller.PMUpdateFrcC import PMUpdateFrcC
from project_manager.entity.FRC import FRC


class PMUpdateFrcPg:
    def __init__(self):
        self.controlView = PMViewFrcC()
        self.controlUpdate = PMUpdateFrcC()
        self.suspend_page = PMSuspendFrcPg()

    def get(self, frc_id):
        frc = self.controlView.viewFrc(frc_id)
        if frc is None:
            return "Fund raising category not found", 404
        return render_template("project_manager/update_frc.html", frc=frc)

    def post(self, frc_id):
        action = request.form.get("action", "update")
        if action in ("suspend", "unsuspend"):
            suspend_response = self.suspend_page.post(frc_id)
            if suspend_response:
                return suspend_response

        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        if self.controlUpdate.updateFrc(frc_id, name, description):
            from flask import redirect, url_for
            return redirect(url_for("view_frc"))

        frc = self.controlView.viewFrc(frc_id)
        return render_template("project_manager/update_frc.html", frc=frc), 400
