from project_manager.entity.Donation import Donation


class PMWeeklyReportGenC:
    def generateWeeklyReport(self, date):
        return Donation.generateWeeklyReport(date)
