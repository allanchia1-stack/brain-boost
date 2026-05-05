from project_manager.entity.FRC import FRC


class PMSuspendFrcC:
    def suspendFrc(self, frc_id):
        if not FRC.get_frc_by_id(frc_id):
            return False
        return FRC.suspend_frc(frc_id)

    def unsuspendFrc(self, frc_id):
        if not FRC.get_frc_by_id(frc_id):
            return False
        return FRC.unsuspend_frc(frc_id)
