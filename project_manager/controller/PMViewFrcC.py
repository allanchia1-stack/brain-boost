from project_manager.entity.FRC import FRC


class PMViewFrcC:
    def __init__(self):
        self.search_control = None

    def getFrcs(self, query):
        if query:
            return FRC.search_frcs(query)
        return FRC.get_all_frcs()

    def viewFrc(self, frc_id):
        return FRC.get_frc_by_id(frc_id)
