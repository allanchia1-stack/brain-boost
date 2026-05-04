from flask import render_template, request
from project_manager.controller.ViewFrcC import ViewFrcC


class ViewFrcPg:
    def __init__(self):
        self.control = ViewFrcC()

    def get(self):
        query = request.args.get("query", "").strip()
        frcs = self.control.get_frcs(query)
        return render_template("project_manager/view_frc.html", frcs=frcs, query=query)
