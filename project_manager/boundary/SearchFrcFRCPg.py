from flask import render_template, request
from project_manager.controller.SearchFrcC import SearchFrcC


class SearchFrcFRCPg:
    def __init__(self):
        self.control = SearchFrcC()

    def get(self):
        return render_template("project_manager/view_frc.html", frcs=self.control.search_frc(""))

    def post(self):
        query   = request.form.get("query", "").strip()
        results = self.control.search_frc(query)
        return render_template("project_manager/view_frc.html", frcs=results, query=query)
