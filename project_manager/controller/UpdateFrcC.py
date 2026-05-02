from project_manager.entity.FRC import FRC


class UpdateFrcC:
    def get_frc_by_id(self, frc_id):
        return FRC.get_frc_by_id(frc_id)

    def handle_action(self, frc_id, action, name, description, status):
        if action == "suspend":
            if not self.get_frc_by_id(frc_id):
                return False
            return FRC.suspend_frc(frc_id)

        if action == "unsuspend":
            if not self.get_frc_by_id(frc_id):
                return False
            return FRC.unsuspend_frc(frc_id)

        return self.update_frc(frc_id, name, description, status)

    def update_frc(self, frc_id, name, description, status):
        if not name:
            return False
        if status not in (0, 1):
            return False
        if not self.get_frc_by_id(frc_id):
            return False
        return FRC.update_frc(frc_id, name, description, status)
