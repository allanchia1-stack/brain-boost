from flask import render_template
from project_manager.controller.WeeklyReportGenC import WeeklyReportGenC


class WeeklyReportPg:
    def __init__(self):
        self.control = WeeklyReportGenC()

    def get(self):
        return render_template("project_manager/weekly_report.html")

    def post(self):
        report = self.control.generate_weekly_report()
        return render_template("project_manager/weekly_report.html", report=report)
