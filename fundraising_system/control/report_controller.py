from entity.report import Report


class ReportController:
    def __init__(self, datastore):
        self.datastore = datastore

    def generate_report(self, report_type):
        content = {
            "total_users": len(self.datastore.users),
            "total_activities": len(self.datastore.activities),
            "total_donations": len(self.datastore.donations),
            "total_categories": len(self.datastore.categories),
        }

        report_id = self.datastore.generate_id("R", self.datastore.reports)
        report = Report(report_id, report_type, content)
        self.datastore.reports.append(report)
        return report