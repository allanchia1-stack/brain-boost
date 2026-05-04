from project_manager.entity.FRC import FRC


class SearchFrcC:
    def search_frc(self, query):
        if query:
            return FRC.search_frcs(query)
        return FRC.get_all_frcs()
