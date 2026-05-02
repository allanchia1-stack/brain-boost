from user_donee.entity.fra import FRA


class ViewFRAC:
    def get_all_fras(self, user_id=None, search_query=""):
        return FRA.get_all_fras(user_id=user_id, search_query=search_query)

    def get_fra_by_id(self, fra_id, user_id=None):
        return FRA.get_fra_by_id(fra_id=fra_id, user_id=user_id)

    def toggle_favourite(self, user_id, fra_id):
        return FRA.toggle_favourite(user_id=user_id, fra_id=fra_id)

    def get_favourite_fras(self, user_id, search_query=""):
        return FRA.get_favourite_fras(user_id=user_id, search_query=search_query)

    def get_fra_history(self, user_id, search_query=""):
        return FRA.get_fra_history(user_id=user_id, search_query=search_query)
