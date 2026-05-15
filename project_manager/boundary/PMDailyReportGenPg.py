from flask import render_template

from project_manager.controller.PMDailyReportGenC import PMDailyReportGenC
from datetime import datetime

class PMDailyReportGenPg:
    def __init__(self):
        self.control = PMDailyReportGenC()

    def get(self):
        return render_template("project_manager/daily_report.html")

    def post(self):
        date = datetime.now().date()
        report = self.control.generateDailyReport(date)
        return render_template("project_manager/daily_report.html", report=report)
