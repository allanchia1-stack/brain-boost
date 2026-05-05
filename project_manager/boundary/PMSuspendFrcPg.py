from flask import redirect, request, url_for

from project_manager.controller.PMSuspendFrcC import PMSuspendFrcC


class PMSuspendFrcPg:
    def __init__(self):
        self.control = PMSuspendFrcC()

    def post(self, frc_id):
        action = request.form.get("action", "")
        if action == "suspend" and self.control.suspendFrc(frc_id):
            return redirect(url_for("view_frc"))
        if action == "unsuspend" and self.control.unsuspendFrc(frc_id):
            return redirect(url_for("view_frc"))
        return False
