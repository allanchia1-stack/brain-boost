"""
PyUnit real SQL tests for Brain Boost.

Run this from the project root:
    python -m unittest discover -s tests -p "test_brain_boost.py" -v

What this file does:
    1. Connects to the real MySQL database `fundraising_db`.
    2. Creates temporary test records with the prefix BBTEST_.
    3. Tests the backend/entity functions for all actors.
    4. Deletes only BBTEST_ data after testing.

Important:
    This is backend PyUnit testing. It tests the logic behind the buttons,
    not the actual HTML button click.
"""

import os  # Used to read database login settings from environment variables.
import sys  # Used to add the project root folder to Python's import path.
import unittest  # Python's built-in unit testing framework, also called PyUnit.
from datetime import date, datetime, timedelta  # Used for predictable FRA dates.

import mysql.connector  # MySQL connector used to connect to the real database.

# This makes sure Python can import your project files even when the test is run from the tests folder.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Finds the main brain-boost folder.
if PROJECT_ROOT not in sys.path:  # If Python does not already know the project folder,
    sys.path.insert(0, PROJECT_ROOT)  # add it so imports like user_admin.entity.UserAcct will work.

# Import the real entity classes from your project.
# These are the same classes used by your Flask routes/controllers.
from user_admin.entity.UserProf import UserProf  # User Admin profile functions.
from user_admin.entity.UserAcct import UserAcct  # User Admin account functions.
from user_donee.entity.donation import Donation as DoneeDonation  # Donee donation history functions.
from user_donee.entity.favourite_fra import FavouriteFRA  # Donee favourite FRA functions.
from user_donee.entity.fra import FRA as DoneeFRA  # Donee FRA browsing/search functions.
from fund_raiser.entity.FRA import FRA as FundraiserFRA  # Fundraiser FRA management functions.
from project_manager.entity.FRC import FRC  # Platform Manager fundraising category functions.
from project_manager.entity.Donation import Donation as ManagerDonation  # Platform Manager donation report functions.


TEST_PREFIX = "BBTEST_"  # Every test-created record starts with this so cleanup is safe.


class RealSQLBase(unittest.TestCase):
    """Shared database setup, seed data, and cleanup used by all test classes."""

    @staticmethod
    def get_connection():
        """Open a connection to the real MySQL database."""
        return mysql.connector.connect(
            user=os.getenv("BB_DB_USER", "root"),  # Uses BB_DB_USER if available, otherwise root.
            password=os.getenv("BB_DB_PASSWORD", "brain-boost"),  # Uses BB_DB_PASSWORD if available.
            host=os.getenv("BB_DB_HOST", "localhost"),  # Local MySQL by default.
            database=os.getenv("BB_DB_NAME", "fundraising_db"),  # Your real project database.
        )

    @classmethod
    def setUpClass(cls):
        """Runs once before each test class starts."""
        # Force all entity classes to use this same test connection method.
        # This prevents different entity files from connecting with different settings.
        for entity in [UserProf, UserAcct, DoneeFRA, DoneeDonation, FavouriteFRA, FundraiserFRA, FRC, ManagerDonation]:
            entity.get_connection = staticmethod(cls.get_connection)  # Replace entity get_connection with this test connection.

        cls.cleanup_test_data()  # Remove old BBTEST_ rows from previous test runs.
        cls.seed_large_test_data()  # Create fresh BBTEST_ rows for this test class.

    @classmethod
    def tearDownClass(cls):
        """Runs once after each test class finishes."""
        cls.cleanup_test_data()  # Clean test rows so your real database is not polluted.

    @classmethod
    def cleanup_test_data(cls):
        """Delete only rows that were created by this test file."""
        conn = cls.get_connection()  # Open database connection.
        cursor = conn.cursor()  # Create cursor to run SQL.
        try:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")  # Temporarily allows child/parent rows to be deleted safely.

            # Delete test donations by special amounts and by BBTEST_ related FRAs/users.
            cursor.execute("DELETE FROM Donation WHERE donation_amt IN (101, 202, 303, 404)")
            cursor.execute(
                "DELETE FROM Donation WHERE donation_user_id IN (SELECT account_id FROM UserAcct WHERE account_email LIKE %s)",
                (f"{TEST_PREFIX.lower()}%",),
            )
            cursor.execute(
                "DELETE FROM Donation WHERE fra_id IN (SELECT fra_id FROM FRA WHERE fra_title LIKE %s)",
                (f"{TEST_PREFIX}%",),
            )

            # Delete test favourites linked to BBTEST_ users or BBTEST_ FRAs.
            cursor.execute(
                "DELETE FROM FavouriteFRA WHERE user_id IN (SELECT account_id FROM UserAcct WHERE account_email LIKE %s)",
                (f"{TEST_PREFIX.lower()}%",),
            )
            cursor.execute(
                "DELETE FROM FavouriteFRA WHERE fra_id IN (SELECT fra_id FROM FRA WHERE fra_title LIKE %s)",
                (f"{TEST_PREFIX}%",),
            )

            # Delete main BBTEST_ records.
            cursor.execute("DELETE FROM FRA WHERE fra_title LIKE %s", (f"{TEST_PREFIX}%",))  # Test fundraising activities.
            cursor.execute("DELETE FROM UserAcct WHERE account_email LIKE %s", (f"{TEST_PREFIX.lower()}%",))  # Test accounts.
            cursor.execute("DELETE FROM UserProf WHERE profile_role LIKE %s", (f"{TEST_PREFIX}%",))  # Test profiles.
            cursor.execute("DELETE FROM FRC WHERE frc_name LIKE %s", (f"{TEST_PREFIX}%",))  # Test categories.

            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")  # Turn foreign key checks back on.
            conn.commit()  # Save all delete operations.
        finally:
            cursor.close()  # Always close cursor.
            conn.close()  # Always close connection.

    @classmethod
    def seed_large_test_data(cls):
        """Create enough controlled test data to simulate a realistic system size."""
        conn = cls.get_connection()  # Open database connection.
        cursor = conn.cursor(dictionary=True)  # Dictionary cursor lets us use row["column_name"].
        try:
            # Make sure the four real system roles exist.
            base_profiles = ["Admin", "Manager", "FundRaiser", "Donee"]  # Required actor roles.
            for role in base_profiles:
                cursor.execute(
                    "INSERT IGNORE INTO UserProf (profile_role, profile_status) VALUES (%s, 1)",
                    (role,),  # INSERT IGNORE avoids duplicate roles.
                )

            # Get role IDs for creating accounts.
            cursor.execute("SELECT profile_id FROM UserProf WHERE profile_role = 'Donee'")
            cls.donee_profile_id = cursor.fetchone()["profile_id"]  # Store Donee role ID.
            cursor.execute("SELECT profile_id FROM UserProf WHERE profile_role = 'FundRaiser'")
            cls.fundraiser_profile_id = cursor.fetchone()["profile_id"]  # Store FundRaiser role ID.

            # Create one active test category.
            cursor.execute(
                "INSERT INTO FRC (frc_name, frc_des, frc_status) VALUES (%s, %s, 1)",
                (f"{TEST_PREFIX}Education Scale", "PyUnit test category"),
            )
            cls.test_frc_id = cursor.lastrowid  # Save category ID for FRA creation.

            # Create 120 test accounts: 80 Donees and 40 Fundraisers.
            cls.donee_ids = []  # Stores created Donee account IDs.
            cls.fundraiser_ids = []  # Stores created Fundraiser account IDs.
            for i in range(1, 121):
                is_donee = i <= 80  # First 80 accounts are Donees.
                role_id = cls.donee_profile_id if is_donee else cls.fundraiser_profile_id  # Pick correct role.
                cursor.execute(
                    """
                    INSERT INTO UserAcct
                    (account_email, account_password, account_name, account_phone, account_address, account_role_id, account_status)
                    VALUES (%s, %s, %s, %s, %s, %s, 1)
                    """,
                    (
                        f"{TEST_PREFIX.lower()}user{i}@example.com",  # Unique test email.
                        "hashed_pass_placeholder",  # Test password placeholder.
                        f"{TEST_PREFIX}User {i}",  # Test name.
                        f"9{i:07d}"[:8],  # Simple 8 digit phone number.
                        f"{TEST_PREFIX}Address {i}",  # Test address.
                        role_id,  # Donee or FundRaiser profile ID.
                    ),
                )
                if is_donee:
                    cls.donee_ids.append(cursor.lastrowid)  # Save Donee ID.
                else:
                    cls.fundraiser_ids.append(cursor.lastrowid)  # Save Fundraiser ID.

            # Create 30 test fundraising activities owned by test fundraisers.
            cls.fra_ids = []  # Stores created FRA IDs.
            statuses = ["ongoing", "completed", "cancelled"]  # Mix statuses for filter tests.
            for i in range(1, 31):
                owner_id = cls.fundraiser_ids[i % len(cls.fundraiser_ids)]  # Spread FRAs across owners.
                status = statuses[i % len(statuses)]  # Rotate status.
                cursor.execute(
                    """
                    INSERT INTO FRA
                    (fra_title, fra_des, fra_donation_goal, fra_donation_amt, fra_start_date,
                     fra_end_date, fra_views, fra_num_of_fav, fra_category, fra_owner_id, fra_status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        f"{TEST_PREFIX}FRA {i}",  # Test FRA title.
                        f"PyUnit seeded FRA {i}",  # Test FRA description.
                        1000 + i,  # Donation goal.
                        i * 10,  # Current donation amount.
                        datetime(2026, 1, 1),  # Fixed start date.
                        datetime(2026, 12, 31),  # Fixed end date.
                        i,  # Starting views.
                        0,  # Starting favourites.
                        cls.test_frc_id,  # Test category.
                        owner_id,  # Test owner.
                        status,  # Status.
                    ),
                )
                cls.fra_ids.append(cursor.lastrowid)  # Save FRA ID.

            # Create donations for Donee donation history and Platform Manager donation summaries.
            for i, amount in enumerate([101, 202, 303]):
                cursor.execute(
                    "INSERT INTO Donation (fra_id, donation_user_id, donation_amt, donation_date) VALUES (%s, %s, %s, NOW())",
                    (cls.fra_ids[i], cls.donee_ids[0], amount),
                )

            # Create favourite records for favourite list/search tests.
            for i in range(10):
                cursor.execute(
                    "INSERT IGNORE INTO FavouriteFRA (user_id, fra_id) VALUES (%s, %s)",
                    (cls.donee_ids[i], cls.fra_ids[i]),
                )

            conn.commit()  # Save all inserted data.
        finally:
            cursor.close()  # Close cursor.
            conn.close()  # Close connection.


class Test01RealSQLBaselineData(RealSQLBase):
    """Tests that the real SQL database has the expected basic data shape."""

    def test_core_tables_have_real_data(self):
        """Checks that important tables are not empty."""
        conn = self.get_connection()  # Open DB connection.
        cursor = conn.cursor(dictionary=True)  # Use dictionary row output.
        try:
            for table in ["UserProf", "UserAcct", "FRC", "FRA", "Donation", "FavouriteFRA"]:
                cursor.execute(f"SELECT COUNT(*) AS total FROM {table}")  # Count rows in each table.
                self.assertGreater(cursor.fetchone()["total"], 0, f"{table} should not be empty")  # Pass only if table has rows.
        finally:
            cursor.close()  # Close cursor.
            conn.close()  # Close connection.

    def test_real_profile_roles_exist(self):
        """Checks that the four actor roles exist."""
        profiles = UserProf.get_all_profiles()  # Calls real entity method.
        roles = {row["profile_role"] for row in profiles}  # Collect role names.
        self.assertTrue({"Admin", "Manager", "FundRaiser", "Donee"}.issubset(roles))  # Required roles must exist.


class Test02UserAdminProfileFunctions(RealSQLBase):
    """Tests all important UserProf profile functions."""

    def test_create_view_update_search_suspend_profile_wrappers(self):
        """Tests createProfile, view, updateProf/updateUser, query/search, and suspend wrappers."""
        profile = UserProf(role=f"{TEST_PREFIX}TempRole", status=1)  # Create profile object.
        profile_id = UserProf.createProfile(profile)  # Test createProfile.
        self.assertTrue(profile_id)  # New profile ID should be returned.

        viewed = UserProf.view(profile_id)  # Test view wrapper.
        self.assertEqual(viewed["profile_role"], f"{TEST_PREFIX}TempRole")  # Confirm created role.

        profile.profile_id = profile_id  # Add ID to object for update.
        profile.role = f"{TEST_PREFIX}UpdatedRole"  # New role name.
        self.assertTrue(UserProf.updateProf(profile))  # Test updateProf.
        self.assertTrue(UserProf.updateUser(profile))  # Test older updateUser wrapper too.

        searched = UserProf.queryUserProfile("UpdatedRole")  # Test queryUserProfile wrapper.
        self.assertTrue(any(row["profile_id"] == profile_id for row in searched))  # Updated role should be searchable.

        before = UserProf.get_profile_by_id(profile_id)["profile_status"]  # Status before suspend.
        self.assertTrue(UserProf.SuspendProf(profile_id))  # Test SuspendProf wrapper.
        after = UserProf.get_profile_by_id(profile_id)["profile_status"]  # Status after suspend.
        self.assertNotEqual(before, after)  # Status should toggle.
        self.assertTrue(UserProf.SuspendUserProfile(profile_id))  # Test SuspendUserProfile wrapper.
        restored = UserProf.get_profile_by_id(profile_id)["profile_status"]  # Status after second toggle.
        self.assertEqual(before, restored)  # Should return to original status.

    def test_get_profile_id_by_role_existing_and_new(self):
        """Tests role ID lookup for an existing role and a newly created test role."""
        existing_id = UserProf.get_profile_id_by_role("Donee")  # Existing role lookup.
        self.assertIsNotNone(existing_id)  # Donee role should exist.

        new_id = UserProf.get_profile_id_by_role(f"{TEST_PREFIX}LookupRole")  # Missing role should be created.
        self.assertIsNotNone(new_id)  # New role ID should be returned.
        self.assertEqual(UserProf.get_profile_by_id(new_id)["profile_role"], f"{TEST_PREFIX}LookupRole")  # Confirm inserted role.


class Test03UserAdminAccountFunctions(RealSQLBase):
    """Tests all important UserAcct account functions."""

    def test_create_view_search_update_suspend_and_login_account(self):
        """Tests create_user/createAccount, view, query/search, updateUser/update_account, suspend, authenticate and userLogin."""
        created_ok = UserAcct.create_user(  # Test simplified create_user wrapper.
            name=f"{TEST_PREFIX}Created Account",
            phone="91234567",
            address=f"{TEST_PREFIX}Created Address",
            role="Donee",
            email=f"{TEST_PREFIX.lower()}created_account@example.com",
            password="secret123",
        )
        self.assertTrue(created_ok)  # Account should be created.

        found = UserAcct.search_accounts("created_account@example.com")  # Test search_accounts.
        self.assertEqual(len(found), 1)  # Should find exactly one new account.
        account_id = found[0]["account_id"]  # Store account ID.

        viewed = UserAcct.view(account_id)  # Test view wrapper.
        self.assertEqual(viewed["account_email"], f"{TEST_PREFIX.lower()}created_account@example.com")  # Confirm email.
        self.assertEqual(viewed["profile_role"], "Donee")  # Confirm joined role name.

        login_user = UserAcct.authenticate(f"{TEST_PREFIX.lower()}created_account@example.com", "secret123")  # Test authenticate.
        self.assertIsNotNone(login_user)  # Login should succeed while active.
        self.assertEqual(login_user.role, "Donee")  # Authenticated role should be Donee.

        wrapper_login = UserAcct.userLogin(f"{TEST_PREFIX.lower()}created_account@example.com", "secret123")  # Test userLogin wrapper.
        self.assertIsNotNone(wrapper_login)  # Wrapper should also succeed.

        temp = UserAcct(  # Build object for older updateUser method.
            account_id=account_id,
            email=f"{TEST_PREFIX.lower()}created_updated@example.com",
            password=None,
            name=f"{TEST_PREFIX}Created Updated",
            phone="97654321",
            address=f"{TEST_PREFIX}Updated Address",
            role="Donee",
        )
        self.assertTrue(UserAcct.updateUser(temp))  # Test updateUser wrapper.
        updated = UserAcct.get_account_by_user_id(account_id)  # Fetch updated account.
        self.assertEqual(updated["account_name"], f"{TEST_PREFIX}Created Updated")  # Confirm name update.

        query_result = UserAcct.queryUserAccount("created_updated@example.com")  # Test queryUserAccount wrapper.
        self.assertEqual(len(query_result), 1)  # Should find updated email.

        before = updated["account_status"]  # Save original status.
        self.assertTrue(UserAcct.SuspendUserAccount(account_id))  # Test SuspendUserAccount wrapper.
        after = UserAcct.get_account_by_user_id(account_id)["account_status"]  # Read status after toggle.
        self.assertNotEqual(before, after)  # Status should change.
        self.assertIsNone(UserAcct.authenticate(f"{TEST_PREFIX.lower()}created_updated@example.com", "secret123"))  # Suspended login should fail.

        self.assertTrue(UserAcct.toggle_suspend_account(account_id))  # Test direct toggle back to active.
        restored = UserAcct.get_account_by_user_id(account_id)["account_status"]  # Read restored status.
        self.assertEqual(before, restored)  # Should be active again.

    def test_get_all_accounts_and_search_returns_profile_role(self):
        """Tests list account and email search result shape."""
        all_accounts = UserAcct.get_all_accounts()  # Test get_all_accounts.
        self.assertGreaterEqual(len(all_accounts), 120)  # Should include seeded scale accounts.

        result = UserAcct.search_accounts(f"{TEST_PREFIX.lower()}user1@example.com")  # Search a seeded account.
        self.assertEqual(len(result), 1)  # Should find one exact test account.
        self.assertIn("profile_role", result[0])  # Search must return readable role name.
        self.assertEqual(result[0]["profile_role"], "Donee")  # User 1 is a Donee.


class Test04DoneeFRAFunctions(RealSQLBase):
    """Tests Donee FRA browsing functions."""

    def test_view_search_get_by_id_and_increment_views(self):
        """Tests get_all_fras, search_fras, get_fra_by_id and increment_fra_views."""
        fras = DoneeFRA.get_all_fras()  # Test Donee view all FRAs.
        self.assertGreaterEqual(len(fras), 30)  # Should show at least seeded FRAs.
        self.assertTrue(any(row["fra_title"].startswith(TEST_PREFIX) for row in fras))  # Seeded FRAs should appear.

        search_result = DoneeFRA.search_fras(f"{TEST_PREFIX}FRA 1")  # Test Donee search by title.
        self.assertGreaterEqual(len(search_result), 1)  # Should find FRA 1 related rows.

        fra_id = self.fra_ids[0]  # Use first seeded FRA.
        before = DoneeFRA.get_fra_by_id(fra_id)  # Test get_fra_by_id before view increment.
        self.assertEqual(before["fra_id"], fra_id)  # Confirm correct FRA.

        self.assertTrue(DoneeFRA.increment_fra_views(fra_id))  # Test Donee increment view count.
        after = DoneeFRA.get_fra_by_id(fra_id)  # Read after increment.
        self.assertEqual(after["fra_views"], before["fra_views"] + 1)  # View count should increase by 1.


class Test05DoneeDonationFunctions(RealSQLBase):
    """Tests Donee donation history functions."""

    def test_donation_history_search_and_detail(self):
        """Tests get_donation_history, search_donation_history and get_donation_by_id."""
        user_id = self.donee_ids[0]  # First seeded Donee has 3 seeded donations.
        history = DoneeDonation.get_donation_history(user_id)  # Test donation history.
        amounts = {row["donation_amt"] for row in history}  # Extract donation amounts.
        self.assertTrue({101, 202, 303}.issubset(amounts))  # Seeded donations must be present.
        self.assertIn("fra_title", history[0])  # Joined FRA title should be included.
        self.assertIn("category_name", history[0])  # Joined category name should be included.

        search_result = DoneeDonation.search_donation_history(user_id, TEST_PREFIX)  # Test donation search.
        self.assertGreaterEqual(len(search_result), 3)  # Should find the three seeded donations.

        donation_id = history[0]["donation_id"]  # Pick one donation ID.
        detail = DoneeDonation.get_donation_by_id(user_id, donation_id)  # Test donation detail.
        self.assertEqual(detail["donation_id"], donation_id)  # Should fetch the same donation.
        self.assertIn("fra_des", detail)  # Detail includes more FRA information.


class Test06DoneeFavouriteFunctions(RealSQLBase):
    """Tests Donee favourite FRA functions."""

    def test_save_unsave_get_and_search_favourite_fras(self):
        """Tests is_saved, save_fra, unsave_fra, get_favourite_fras and search_favourite_fras."""
        user_id = self.donee_ids[20]  # Pick a seeded Donee.
        fra_id = self.fra_ids[20]  # Pick a seeded FRA.

        FavouriteFRA.unsave_fra(user_id, fra_id)  # Start clean in case already saved.
        self.assertFalse(FavouriteFRA.is_saved(user_id, fra_id))  # Should not be saved.

        self.assertTrue(FavouriteFRA.save_fra(user_id, fra_id))  # Test save_fra.
        self.assertTrue(FavouriteFRA.is_saved(user_id, fra_id))  # is_saved should now return True.

        favourites = FavouriteFRA.get_favourite_fras(user_id)  # Test get_favourite_fras.
        self.assertTrue(any(row["fra_id"] == fra_id for row in favourites))  # Saved FRA should appear.

        search_result = FavouriteFRA.search_favourite_fras(user_id, TEST_PREFIX)  # Test search_favourite_fras.
        self.assertTrue(any(row["fra_id"] == fra_id for row in search_result))  # Saved FRA should be searchable.

        self.assertTrue(FavouriteFRA.unsave_fra(user_id, fra_id))  # Test unsave_fra.
        self.assertFalse(FavouriteFRA.is_saved(user_id, fra_id))  # Should no longer be saved.


class Test07FundraiserFRAFunctions(RealSQLBase):
    """Tests Fundraiser FRA management functions."""

    def test_categories_and_filtered_fra_lists(self):
        """Tests get_categories, get_all_fras, get_ongoing_fras and get_completed_fras."""
        categories = FundraiserFRA.get_categories()  # Test category dropdown/list function.
        self.assertTrue(any(row["frc_id"] == self.test_frc_id for row in categories))  # Active test category should appear.

        owner_id = self.fundraiser_ids[1]  # This owner has seeded FRAs.
        all_fras = FundraiserFRA.get_all_fras(owner_id)  # Test all own FRAs.
        self.assertGreaterEqual(len(all_fras), 1)  # Owner should have at least one FRA.

        ongoing = FundraiserFRA.get_ongoing_fras(owner_id)  # Test ongoing filter.
        self.assertTrue(all(row["fra_status"] == "ongoing" for row in ongoing))  # Every returned row must be ongoing.

        completed = FundraiserFRA.get_completed_fras(owner_id)  # Test completed filter.
        self.assertTrue(all(row["fra_status"] == "completed" for row in completed))  # Every returned row must be completed.

    def test_search_get_update_suspend_category_and_manager_get(self):
        """Tests search_fras, get_fra_by_id, update_fra, suspend_fra, get_fras_by_category, get_fra_by_id_for_manager."""
        owner_id = self.fundraiser_ids[1]  # Pick seeded fundraiser.
        result = FundraiserFRA.search_fras(TEST_PREFIX, owner_id)  # Test search own FRAs.
        self.assertGreaterEqual(len(result), 1)  # Should find at least one own FRA.
        fra_id = result[0]["fra_id"]  # Pick one FRA to update.

        fetched = FundraiserFRA.get_fra_by_id(fra_id, owner_id)  # Test owner-specific get by ID.
        self.assertEqual(fetched["fra_id"], fra_id)  # Must return correct FRA.

        self.assertTrue(FundraiserFRA.update_fra(  # Test actual update_fra function.
            fra_id=fra_id,
            owner_id=owner_id,
            title=f"{TEST_PREFIX}Updated Fundraiser FRA",
            category_id=self.test_frc_id,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=60),
            goal=8888,
            description="Updated by PyUnit",
        ))
        updated = FundraiserFRA.get_fra_by_id(fra_id, owner_id)  # Fetch after update.
        self.assertEqual(updated["fra_title"], f"{TEST_PREFIX}Updated Fundraiser FRA")  # Confirm title update.
        self.assertEqual(int(updated["fra_donation_goal"]), 8888)  # Confirm goal update.

        by_category = FundraiserFRA.get_fras_by_category(self.test_frc_id)  # Test get by category.
        self.assertTrue(any(row["fra_id"] == fra_id for row in by_category))  # Updated FRA should be in category list.

        manager_view = FundraiserFRA.get_fra_by_id_for_manager(fra_id)  # Test manager get by FRA ID.
        self.assertEqual(manager_view["fra_id"], fra_id)  # Manager view should fetch the same FRA.

        self.assertTrue(FundraiserFRA.suspend_fra(fra_id, owner_id))  # Test suspend/cancel FRA.
        suspended = FundraiserFRA.get_fra_by_id(fra_id, owner_id)  # Fetch after suspend.
        self.assertEqual(suspended["fra_status"], "cancelled")  # Status should become cancelled.

    def test_create_fra_and_increment_view_count(self):
        """Tests create_fra and Fundraiser increment_fra_views."""
        owner_id = self.fundraiser_ids[0]  # Pick first seeded Fundraiser.
        self.assertTrue(FundraiserFRA.create_fra(  # Test creating an FRA, same backend logic as Create button.
            title=f"{TEST_PREFIX}Created From PyUnit",
            category_id=self.test_frc_id,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            goal=5000,
            description="Created by PyUnit real SQL test",
            owner_id=owner_id,
        ))

        created = FundraiserFRA.search_fras("Created From PyUnit", owner_id)  # Search for newly created FRA.
        self.assertGreaterEqual(len(created), 1)  # It should exist in DB.
        fra_id = created[0]["fra_id"]  # Get created FRA ID.
        fetched = FundraiserFRA.get_fra_by_id(fra_id, owner_id)  # Fetch by ID.
        self.assertEqual(fetched["fra_title"], f"{TEST_PREFIX}Created From PyUnit")  # Confirm title was saved.

        before_views = fetched["fra_views"]  # Store old view count.
        self.assertTrue(FundraiserFRA.increment_fra_views(fra_id))  # Test view increment.
        after = FundraiserFRA.get_fra_by_id(fra_id, owner_id)  # Fetch after increment.
        self.assertEqual(after["fra_views"], before_views + 1)  # View count should increase by exactly 1.


class Test08PlatformManagerFRCFunctions(RealSQLBase):
    """Tests Platform Manager FRC category functions."""

    def test_get_all_search_get_create_update_suspend_unsuspend_frc(self):
        """Tests get_all_frcs, search_frcs, get_frc_by_id, create_frc, update_frc, suspend_frc and unsuspend_frc."""
        all_categories = FRC.get_all_frcs()  # Test get_all_frcs.
        self.assertGreaterEqual(len(all_categories), 1)  # Should have at least one category.

        search_existing = FRC.search_frcs(TEST_PREFIX)  # Test search_frcs.
        self.assertGreaterEqual(len(search_existing), 1)  # Should find seeded category.

        category = FRC.get_frc_by_id(self.test_frc_id)  # Test get_frc_by_id.
        self.assertEqual(category["id"], self.test_frc_id)  # Should fetch correct category.

        self.assertTrue(FRC.create_frc(f"{TEST_PREFIX}Medical PyUnit", "Created by PyUnit", 1))  # Test create_frc.
        created = FRC.search_frcs("Medical PyUnit")  # Search created category.
        self.assertGreaterEqual(len(created), 1)  # Created category should be found.
        frc_id = created[0]["id"]  # Store new category ID.

        self.assertTrue(FRC.update_frc(frc_id, f"{TEST_PREFIX}Medical Updated", "Updated by PyUnit", 1))  # Test update_frc.
        updated = FRC.get_frc_by_id(frc_id)  # Fetch updated category.
        self.assertEqual(updated["name"], f"{TEST_PREFIX}Medical Updated")  # Confirm update.

        self.assertTrue(FRC.suspend_frc(frc_id))  # Test suspend_frc.
        suspended = FRC.get_frc_by_id(frc_id)  # Fetch after suspend.
        self.assertEqual(suspended["status"], 0)  # Suspended status should be 0.

        self.assertTrue(FRC.unsuspend_frc(frc_id))  # Test unsuspend_frc.
        active = FRC.get_frc_by_id(frc_id)  # Fetch after unsuspend.
        self.assertEqual(active["status"], 1)  # Active status should be 1.


class Test09PlatformManagerDonationReportFunctions(RealSQLBase):
    """Tests Platform Manager donation report functions."""

    def test_daily_weekly_monthly_donation_summaries(self):
        """Tests get_daily_summary, get_weekly_summary and get_monthly_summary."""
        daily = ManagerDonation.get_daily_summary()  # Test daily donation summary.
        self.assertIn("period", daily)  # Summary should include period label.
        self.assertIn("donations", daily)  # Summary should include donation rows.
        self.assertIn("total_donations", daily)  # Summary should include count.
        self.assertIn("total_amount", daily)  # Summary should include amount.
        self.assertGreaterEqual(daily["total_amount"], 606)  # Seeded 101+202+303 donations are created today.

        weekly = ManagerDonation.get_weekly_summary()  # Test weekly donation summary.
        self.assertIn("period", weekly)  # Weekly summary should include period.
        self.assertGreaterEqual(weekly["total_amount"], 606)  # Seeded donations should be included this week.

        monthly = ManagerDonation.get_monthly_summary()  # Test monthly donation summary.
        self.assertIn("period", monthly)  # Monthly summary should include period.
        self.assertGreaterEqual(monthly["total_amount"], 606)  # Seeded donations should be included this month.


if __name__ == "__main__":  # Only runs when this file is executed directly.
    unittest.main(verbosity=2)  # Start PyUnit and print detailed test results.
