from user_donee.controller.donee_view_fra_c import DoneeViewFraC


class ViewFRAC:
    def get_all_fras(self):
        return DoneeViewFraC().view_all_fra()
