from data.datastore import DataStore

from control.user_profile_controller import UserProfileController
from control.user_account_controller import UserAccountController
from control.auth_controller import AuthController
from control.fundraising_activity_controller import FundRaisingActivityController
from control.favourite_controller import FavouriteController
from control.donation_controller import DonationController
from control.category_controller import CategoryController
from control.report_controller import ReportController

from boundary.user_profile_page import UserProfilePage
from boundary.fundraising_activity_page import FundRaisingActivityPage
from boundary.favourite_page import FavouritePage
from boundary.donation_history_page import DonationHistoryPage
from boundary.category_page import CategoryPage
from boundary.report_page import ReportPage
from boundary.login_page import LoginPage
from boundary.user_account_page import UserAccountPage

from entity.user import User


def main():
    datastore = DataStore()

    # sample users
    user1 = User("U1", "Admin User", "admin@email.com", "admin")
    user2 = User("U2", "Fund Raiser", "fundraiser@email.com", "fundraiser")
    user3 = User("U3", "Donee User", "donee@email.com", "donee")

    datastore.users.extend([user1, user2, user3])

    # controllers
    user_profile_controller = UserProfileController(datastore)
    user_account_controller = UserAccountController(datastore)
    auth_controller = AuthController(datastore)
    activity_controller = FundRaisingActivityController(datastore)
    favourite_controller = FavouriteController(datastore)
    donation_controller = DonationController(datastore)
    category_controller = CategoryController(datastore)
    report_controller = ReportController(datastore)

    # boundaries
    user_profile_page = UserProfilePage(user_profile_controller)
    user_account_page = UserAccountPage(user_account_controller)
    login_page = LoginPage(auth_controller)
    activity_page = FundRaisingActivityPage(activity_controller)
    favourite_page = FavouritePage(favourite_controller)
    donation_page = DonationHistoryPage(donation_controller)
    category_page = CategoryPage(category_controller)
    report_page = ReportPage(report_controller)

    # create user profiles
    user_profile_page.create_profile("U1", "Singapore", "91234567")
    user_profile_page.create_profile("U2", "Singapore", "92345678")
    user_profile_page.create_profile("U3", "Singapore", "93456789")

    # create accounts
    user_account_page.create_account("admin1", "1234", "U1")
    user_account_page.create_account("fundraiser1", "1234", "U2")
    user_account_page.create_account("donee1", "1234", "U3")

    # login test
    logged_in_account = login_page.login("donee1", "1234")

    if logged_in_account:
        print("=== Login Successful ===")
        print(f"Welcome, {logged_in_account.username}")
    else:
        print("Login failed")

    # categories
    category_page.create_category("Medical")
    category_page.create_category("Education")

    # fundraiser creates activity
    activity = activity_page.create_activity(
        "Help Cancer Patient",
        "Raising funds for treatment",
        10000,
        "Medical",
        "U2"
    )

    # donee saves favourite and donates
    favourite_page.save_activity("U3", activity.activity_id)
    donation_controller.make_donation("U3", activity.activity_id, 200)

    # generate report
    report = report_page.generate_report("Daily")

    print("\n=== Activities ===")
    for act in activity_page.view_activities():
        print(act.title, act.amount_raised, act.status)

    print("\n=== Donation History ===")
    for donation in donation_page.view_history("U3"):
        print(donation.donation_id, donation.amount)

    print("\n=== Report ===")
    print(report.content)

    print("\n=== Logout ===")
    print(login_page.logout())


if __name__ == "__main__":
    main()