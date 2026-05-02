from user_donee.entity.fra import FRA

class ViewFRAC:
    def get_all_fras(self):
        # Fetches the list of dictionaries from the Entity layer
        return FRA.get_all_fras()