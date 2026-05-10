from project_manager.entity.Donation import Donation


class PMDailyReportGenC:
    def fetchDailyDon(self, date):
        return Donation.fetchDailyDon(date)
