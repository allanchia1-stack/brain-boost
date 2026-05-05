from project_manager.entity.Donation import Donation


class PMWeeklyReportGenC:
    def generateWeeklyReport(self):
        return Donation.get_weekly_summary()
