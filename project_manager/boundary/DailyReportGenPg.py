from flask import render_template
from project_manager.controller.DailyReportGenC import DailyReportGenC


class DailyReportGenPg:
    def __init__(self):
        self.control = DailyReportGenC()

    def get(self):
        return render_template("project_manager/daily_report.html")

    def post(self):
        report = self.control.generate_daily_report()
        return render_template("project_manager/daily_report.html", report=report)
