from project_manager.entity.Donation import Donation


class MonthlyReportGenC:
    def generate_monthly_report(self):
        return Donation.get_monthly_summary()
