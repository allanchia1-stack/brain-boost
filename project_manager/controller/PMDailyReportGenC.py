from project_manager.entity.Donation import Donation


class PMDailyReportGenC:
    def generateDailyReport(self, date):
        return Donation.generateDailyReport(date)
