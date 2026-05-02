from flask import render_template
from project_manager.controller.MonthlyReportGenC import MonthlyReportGenC


class MonthlyReportPg:
    def __init__(self):
        self.control = MonthlyReportGenC()

    def get(self):
        return render_template("project_manager/monthly_report.html")

    def post(self):
        report = self.control.generate_monthly_report()
        return render_template("project_manager/monthly_report.html", report=report)
