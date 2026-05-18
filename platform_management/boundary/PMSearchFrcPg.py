from flask import render_template, request

from platform_management.controller.PMSearchFrcC import PMSearchFrcC


class PMSearchFrcPg:
    def __init__(self):
        self.control = PMSearchFrcC()

    def get(self):
        query = request.args.get("query", "").strip()
        frcs = self.control.searchFrc(query)
        return render_template("platform_management/view_frc.html", frcs=frcs, query=query)
