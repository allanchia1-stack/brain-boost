from project_manager.entity.Donation import Donation


class DailyReportGenC:
    def generate_daily_report(self):
        return Donation.get_daily_summary()
