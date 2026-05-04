from project_manager.entity.FRC import FRC


class ViewFrcC:
    def get_frcs(self, query):
        if query:
            return FRC.search_frcs(query)
        return FRC.get_all_frcs()

    def get_all_frcs(self):
        return FRC.get_all_frcs()

    def get_frc_by_id(self, frc_id):
        return FRC.get_frc_by_id(frc_id)
