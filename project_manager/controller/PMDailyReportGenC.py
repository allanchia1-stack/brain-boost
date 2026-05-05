from project_manager.entity.Donation import Donation


class PMDailyReportGenC:
    def generateDailyReport(self):
        return Donation.get_daily_summary()
