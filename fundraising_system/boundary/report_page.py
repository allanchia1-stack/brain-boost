class ReportPage:
    def __init__(self, controller):
        self.controller = controller

    def generate_report(self, report_type):
        return self.controller.generate_report(report_type)