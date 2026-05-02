from project_manager.entity.Donation import Donation


class WeeklyReportGenC:
    def generate_weekly_report(self):
        return Donation.get_weekly_summary()
