from flask import render_template

from platform_management.controller.PMWeeklyReportGenC import PMWeeklyReportGenC
from datetime import datetime

class PMWeeklyReportGenPg:
    def __init__(self):
        self.control = PMWeeklyReportGenC()

    def get(self):
        return render_template("platform_management/weekly_report.html")

    def post(self):
        date = datetime.now().date()
        report = self.control.generateWeeklyReport(date)
        return render_template("platform_management/weekly_report.html", report=report)
