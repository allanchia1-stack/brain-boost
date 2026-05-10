from project_manager.entity.Donation import Donation


class PMMonthlyReportGenC:
    def generateMonthlyReport(self, date):
        return Donation.generateMonthlyReport(date)
