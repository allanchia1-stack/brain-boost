from project_manager.entity.FRC import FRC


class CreateFrcC:
    def create_frc(self, name, description, status):
        return FRC.create_frc(name, description, status)
