from project_manager.entity.Donation import Donation


class PMMonthlyReportGenC:
    def generateMonthlyReport(self):
        return Donation.get_monthly_summary()
