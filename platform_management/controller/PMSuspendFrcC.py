from platform_management.entity.FRC import FRC


class PMSuspendFrcC:
    def suspendFrc(self, frc_id):
        if not FRC.viewFrc(frc_id):
            return False
        return FRC.suspendFrc(frc_id)

    def unsuspendFrc(self, frc_id):
        if not FRC.viewFrc(frc_id):
            return False
        return FRC.unsuspend_frc(frc_id)
