from flask import render_template

from project_manager.controller.PMMonthlyReportGenC import PMMonthlyReportGenC


class PMMonthlyReportGenPg:
    def __init__(self):
        self.control = PMMonthlyReportGenC()

    def get(self):
        return render_template("project_manager/monthly_report.html")

    def post(self):
        report = self.control.generateMonthlyReport()
        return render_template("project_manager/monthly_report.html", report=report)
