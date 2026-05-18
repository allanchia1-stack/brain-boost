from flask import render_template

from platform_management.controller.PMMonthlyReportGenC import PMMonthlyReportGenC
from datetime import datetime

class PMMonthlyReportGenPg:
    def __init__(self):
        self.control = PMMonthlyReportGenC()

    def get(self):
        return render_template("project_manager/monthly_report.html")

    def post(self):
        date = datetime.now().date()
        report = self.control.generateMonthlyReport(date)
        return render_template("project_manager/monthly_report.html", report=report)
