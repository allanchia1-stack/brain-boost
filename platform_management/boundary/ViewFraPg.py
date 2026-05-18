from flask import render_template

from platform_management.controller.ViewFraC import ViewFraC


class ViewFraPg:
    def __init__(self):
        self.control = ViewFraC()

    def get_by_category(self, frc_id):
        fras = self.control.get_fras_by_category(frc_id)
        return render_template("platform_management/view_fra_by_frc.html", fras=fras)

    def get_detail(self, fra_id):
        fra = self.control.get_fra_by_id(fra_id)
        if fra is None:
            return "Fund raising activity not found", 404
        return render_template("platform_management/view_fra_detail.html", fra=fra)
