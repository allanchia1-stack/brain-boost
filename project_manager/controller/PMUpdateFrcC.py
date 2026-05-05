from project_manager.entity.FRC import FRC


class PMUpdateFrcC:
    def viewFrc(self, frc_id):
        return FRC.get_frc_by_id(frc_id)

    def updateFrc(self, frc_id, name, description):
        frc = self.viewFrc(frc_id)
        if not frc or not name:
            return False
        return FRC.update_frc(frc_id, name, description, frc["status"])
