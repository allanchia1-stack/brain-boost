from project_manager.entity.FRC import FRC


class PMUpdateFrcC:
    def viewFrc(self, frc_id):
        return FRC.viewFrc(frc_id)

    def updateFrc(self, frc_id,temp):
        #frc = self.viewFrc(frc_id)
        #if not frc or not name:
            #return False
        return FRC.updateFrc(frc_id, temp)
