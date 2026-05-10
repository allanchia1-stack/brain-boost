from flask import Blueprint, render_template, request, session, redirect, url_for
from user_donee.controller.donee_search_don_c import DoneeSearchDonC
from user_donee.controller.donee_view_don_c import DoneeViewDonC


donee_donation_history_bp = Blueprint("donee_donation_history_bp", __name__)
search_don_control = DoneeSearchDonC()
view_don_control = DoneeViewDonC()


@donee_donation_history_bp.route("/donee/donation-history", methods=["GET"])
def donation_history_page():
    if session.get("role") != "Donee":
        return redirect(url_for("login"))

    search_query = request.args.get("q", "").strip()
    print("Executing search FRA donation history")
    donations = search_don_control.searchDon(session["user_id"], search_query)
    return render_template(
        "user_donee/donee_fra_history.html",
        donations=donations,
        search_query=search_query
    )


@donee_donation_history_bp.route("/donee/donation-history/<int:donation_id>", methods=["GET"])
def donation_detail_page(donation_id):
    if session.get("role") != "Donee":
        return redirect(url_for("login"))

    print("Executing View FRA Donation History")
    donation = view_don_control.viewDon(session["user_id"], donation_id)
    if donation is None:
        return redirect(url_for("donee_donation_history_bp.donation_history_page"))

    return render_template(
        "user_donee/donee_fra_history_detail.html",
        donation=donation
    )
