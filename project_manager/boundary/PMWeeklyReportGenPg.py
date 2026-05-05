from flask import render_template

from project_manager.controller.PMWeeklyReportGenC import PMWeeklyReportGenC


class PMWeeklyReportGenPg:
    def __init__(self):
        self.control = PMWeeklyReportGenC()

    def get(self):
        return render_template("project_manager/weekly_report.html")

    def post(self):
        report = self.control.generateWeeklyReport()
        return render_template("project_manager/weekly_report.html", report=report)
