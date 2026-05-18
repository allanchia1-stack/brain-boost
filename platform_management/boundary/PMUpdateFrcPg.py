from flask import render_template, request

from platform_management.boundary.PMSuspendFrcPg import PMSuspendFrcPg
from platform_management.controller.PMViewFrcC import PMViewFrcC
from platform_management.controller.PMUpdateFrcC import PMUpdateFrcC
from platform_management.entity.FRC import FRC


class PMUpdateFrcPg:
    def __init__(self):
        self.controlView = PMViewFrcC()
        self.controlUpdate = PMUpdateFrcC()
        self.suspend_page = PMSuspendFrcPg()

    def get(self, frc_id):
        frc = self.controlView.viewFrc(frc_id)
        if frc is None:
            return "Fund raising category not found", 404
        return render_template("platform_management/update_frc.html", frc=frc)

    def post(self, frc_id):
        action = request.form.get("action", "update")
        if action in ("suspend", "unsuspend"):
            suspend_response = self.suspend_page.post(frc_id)
            if suspend_response:
                return suspend_response

        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        frc = self.controlView.viewFrc(frc_id)
        temp = FRC(name,description,frc["status"])
        if self.controlUpdate.updateFrc(frc_id, temp):
            from flask import redirect, url_for
            return redirect(url_for("view_frc"))

        frc = self.controlView.viewFrc(frc_id)
        return render_template("platform_management/update_frc.html", frc=frc), 400
