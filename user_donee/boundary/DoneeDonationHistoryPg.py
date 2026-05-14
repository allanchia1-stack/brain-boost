from flask import Blueprint, render_template, request, session, redirect, url_for
from user_donee.controller.DoneeSearchDonC import DoneeSearchDonC
from user_donee.controller.DoneeViewDonC import DoneeViewDonC


donee_donation_history_bp = Blueprint("donee_donation_history_bp", __name__)


class DoneeDonationHistoryPg:
    def __init__(self):
        self.search_don_control = DoneeSearchDonC()
        self.view_don_control = DoneeViewDonC()

    def doneeOnly(self):
        return session.get("role") == "Donee"

    def getSearchDonKey(self):
        return request.args.get("q", "").strip()

    def searchDon(self, user_id, query):
        #print("Executing DoneeDonationHistoryPg.searchDon()")
        return self.search_don_control.searchDon(user_id, query)

    def viewDon(self, user_id, donation_id):
        p#rint("Executing DoneeDonationHistoryPg.viewDon()")
        return self.view_don_control.viewDon(user_id, donation_id)

    def showResult(self, donations, search_query=""):
        return render_template(
            "user_donee/donee_fra_history.html",
            donations=donations,
            search_query=search_query,
        )

    def showDetail(self, donation):
        return render_template(
            "user_donee/donee_fra_history_detail.html",
            donation=donation,
        )


@donee_donation_history_bp.route("/donee/donation-history", methods=["GET"])
def donation_history_page():
    page = DoneeDonationHistoryPg()
    if not page.doneeOnly():
        return redirect(url_for("login"))

    query = page.getSearchDonKey()
    donations = page.searchDon(session["user_id"], query)
    return page.showResult(donations, query)


@donee_donation_history_bp.route("/donee/donation-history/<int:donation_id>", methods=["GET"])
def donation_detail_page(donation_id):
    page = DoneeDonationHistoryPg()
    if not page.doneeOnly():
        return redirect(url_for("login"))

    donation = page.viewDon(session["user_id"], donation_id)
    if donation is None:
        return redirect(url_for("donee_donation_history_bp.donation_history_page"))

    return page.showDetail(donation)
