from platform_management.entity.Donation import Donation


class PMDailyReportGenC:
    def generateDailyReport(self, date):
        return Donation.generateDailyReport(date)
