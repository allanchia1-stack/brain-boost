from fund_raiser.entity.FRA import FRA


class ViewFraC:
    def get_fras_by_category(self, frc_id):
        return FRA.get_fras_by_category(frc_id)

    def get_fra_by_id(self, fra_id):
        return FRA.get_fra_by_id_for_manager(fra_id)
