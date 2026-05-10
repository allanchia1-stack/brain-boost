from project_manager.entity.FRC import FRC


class PMSearchFrcC:
    def searchFrc(self, query):
        if query:
            return FRC.queryFrc(query)
        return FRC.get_all_frcs()
