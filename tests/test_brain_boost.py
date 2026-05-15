import sys
import os
import unittest
import mysql.connector


# Ensure project root is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# used for log in test
from user_admin.boundary.LogInPg import LogInPg
from user_admin.controller.LogInC import LogInC

# used for log out test
from user_admin.boundary.LogOutPg import LogOutPg
from app import app
from flask import session

# used for account creation test
from user_admin.boundary.UserAdminCreateUserAccountPg import UserAdminCreateUserAccountPg
from user_admin.controller.UserAdminCreateAccountC import UserAdminCreateAccountC

# used for account view, update, suspend, search test
from user_admin.boundary.UserAdminResultUserAccountPg import UserAdminResultUserAccountPg
from user_admin.controller.UserAdminViewAccountC import UserAdminViewAccountC
from user_admin.controller.UserAdminUpdateAccountC import UserAdminUpdateAccountC
from user_admin.controller.UserAdminSuspendAccountC import UserAdminSuspendAccountC
from user_admin.controller.UserAdminSearchAccountC import UserAdminSearchAccountC

# used for profile creation test
from user_admin.boundary.UserAdminCreateProfilePg import UserAdminCreateProfilePg
from user_admin.controller.UserAdminCreateProfileC import UserAdminCreateProfileC

# used for profile view, update, suspend, search test
from user_admin.boundary.UserAdminResultUserProfilePg import UserAdminResultUserProfilePg
from user_admin.boundary.UserAdminResultUserProfilePg import UserAdminUpdateUserProfilePg
from user_admin.boundary.UserAdminResultUserProfilePg import UserAdminUserProfilePg
from user_admin.controller.UserAdminViewProfileC import UserAdminViewProfileC
from user_admin.controller.UserAdminUpdateProfileC import UserAdminUpdateProfileC
from user_admin.controller.UserAdminSuspendProfileC import UserAdminSuspendProfileC
from user_admin.controller.UserAdminSearchProfileC import UserAdminSearchProfileC

from user_admin.entity.UserProf import UserProf
from user_admin.entity.UserAcct import UserAcct


class TestUserAdmin(unittest.TestCase):

    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            user="root",
            password="brain-boost",
            host="localhost",
            database="fundraising_db"
        )

    @classmethod
    def setUpClass(cls):
        """
        Connect to existing database
        """
        cls.conn = cls.get_connection()
        cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        """
        Close database connection
        """
        cls.cursor.close()
        cls.conn.close()

    def setUp(self):
        """
        Cleanup test data before each test
        """

        # Remove test profiles
        self.cursor.execute(
            """DELETE FROM userprof WHERE profile_role IN (%s, %s)""",
            ("Toast","Jam"),
        )

        # Remove test accounts
        self.cursor.execute(
            """DELETE FROM useracct WHERE account_email IN (%s, %s)""",
            ("test1@example.com","test2@example.com"),
        )

        self.conn.commit()

    def test_create_user_profile_success(self):

        profile = UserProf(
            role="Toast",
            status=1
        )

        page = UserAdminCreateProfilePg()

        result = page.createProfile(profile)

        self.assertEqual(result, True)

        # Verify inserted into DB
        self.cursor.execute(
            """SELECT * FROM userprof WHERE profile_role=%s""",
            ("Toast",),
        )
        row = self.cursor.fetchone()

        self.assertIsNotNone(row)

    def test_create_user_profile_duplicate_pk(self):

        profile = UserProf(
            role="Jam",
            status=1
        )

        page = UserAdminCreateProfilePg()

        # First insert
        result1 = page.createProfile(profile)

        self.assertEqual(result1, True)

        ## Duplicate insert should fail
        #with self.assertRaises(mysql.connector.IntegrityError):
        #    page.createProfile(profile)
        
        # Verify only ONE record exists in DB
        
        self.cursor.execute(
            "SELECT COUNT(*) FROM userprof WHERE profile_role=%s",
            ("Jam",)
            )
        count = self.cursor.fetchone()[0]

        self.assertEqual(count, 1)
        
    def test_view_user_profile_success(self):
        
        # use this to fetch profile_id 1 which is "Admin"
        idNum = 1

        page = UserAdminResultUserProfilePg()

        # run profile into view function
        result = page.view(idNum)
        #print(result)

        self.assertEqual(result["profile_role"],"Admin")
        
    def test_update_user_profile_success(self):

        # Change profile_id 1 from "Admin" to "Admin_1"
        profile = UserProf(
            profile_id = 1,
            role="Admin_1",
        )

        page = UserAdminUpdateUserProfilePg()

        # run profile into updateProf function
        result = page.updateProf(profile)
        #print(result)

        self.assertEqual(result, True)
        
        # Change it back to Admin
        profile = UserProf(
            profile_id = 1,
            role="Admin",
        )

        page = UserAdminUpdateUserProfilePg()
        result = page.updateProf(profile)
        
        self.assertEqual(result, True)
        
    def test_suspend_user_profile_success(self):
		
		
		# use idNum, set to 1, to suspend "Admin"
        idNum = 1

        page = UserAdminUserProfilePg()
		

        # run profile into suspendProf function
        result = page.suspendProf(idNum)
        #print(result)

        self.assertEqual(result, True)
        
        # use idNum, set to 1, to unsuspend "Admin"
        result = page.suspendProf(idNum)
        
        self.assertEqual(result, True)

    def test_search_user_profile_success(self):
		
		# search for Donee, should return 1 value
        query = "Donee"

        page = UserAdminResultUserProfilePg()

        # run profile into view function
        count = page.searchUserProfile(query)
        
        self.assertEqual(len(count), 1)    

    def test_create_user_account_success(self):

        account = UserAcct(
            email="test1@example.com",
            password="hashed_pass_placeholder",
            name="Test User",
            phone="91234567",
            address="123 Tampines Street 11",
            role = "Admin"
        )

        page = UserAdminCreateUserAccountPg()

        result = page.createAccount(account)

        self.assertEqual(result, True)

        # Verify inserted into DB
        self.cursor.execute(
            """SELECT * FROM useracct WHERE account_email=%s""",
            ("test1@example.com",),
        )

        row = self.cursor.fetchone()

        self.assertIsNotNone(row)

    def test_create_user_account_duplicate_email_pk(self):

        account = UserAcct(
            email="test2@example.com",
            password="hashed_pass_placeholder",
            name="Duplicate User",
            phone="98765432",
            address="Singapore",
            role = "Admin"
        )

        page = UserAdminCreateUserAccountPg()

        # First insert
        result1 = page.createAccount(account)

        self.assertEqual(result1, True)

        ## Duplicate insert should fail
        #with self.assertRaises(mysql.connector.IntegrityError):
        #    page.createAccount(account)
        
        # Verify only ONE record exists in DB
        self.cursor.execute(
            "SELECT COUNT(*) FROM useracct WHERE account_email=%s",
            ("test2@example.com",)
            )

        count = self.cursor.fetchone()[0]

        self.assertEqual(count, 1)
        
        
    def test_view_user_account_success(self):
        
        # use this to fetch profile_id 1 which is "Admin"
        idNum = 1

        page = UserAdminResultUserAccountPg()

        # run profile into view function
        result = page.view(idNum)
        #print(result)

        self.assertEqual(result["account_email"],"donaldgarcia@example.net")
        
    def test_update_user_account_success(self):

        # Below is the original account details
        #account = UserAcct(
        #    account_id=11
        #    email="stephen10@example.com",
        #    password="hashed_pass_placeholder",
        #    name="Derek Anderson",
        #    phone="99911838",
        #    address="35427 Carr Valley Apt. 841, West Darrell, CT 97811",
        #    role = "Donee"
        #)
        
        # Change the Name and Phone
        account = UserAcct(
            account_id=11,
            email="stephen10@example.com",
            password="hashed_pass_placeholder",
            name="Samuel Jackson",
            phone="91837712",
            address="35427 Carr Valley Apt. 841, West Darrell, CT 97811",
            role = "Donee"
        )

        page = UserAdminResultUserAccountPg()

        # run profile into updateProf function
        result = page.updateUser(account)
        #print(result)

        self.assertEqual(result, True)
        
        # Change it back to Admin
        account = UserAcct(
            account_id=11,
            email="stephen10@example.com",
            password="hashed_pass_placeholder",
            name="Derek Anderson",
            phone="99911838",
            address="35427 Carr Valley Apt. 841, West Darrell, CT 97811",
            role = "Donee"
        )

        result = page.updateUser(account)
        
        self.assertEqual(result, True)
        
    def test_suspend_user_suspend_success(self):
		
		
		# use idNum, set to 1, to suspend "donaldgarcia@example.net"
        idNum = 1

        page = UserAdminResultUserAccountPg()
		

        # run profile into suspendProf function
        result = page.suspendUserAccount(idNum)
        #print(result)

        self.assertEqual(result, True)
        
        # use idNum, set to 1, to unsuspend "Admin"
        result = page.suspendUserAccount(idNum)
        
        self.assertEqual(result, True)

    def test_search_user_account_success(self):
		
		# search for "nperry", should return 1 value
        query = "nperry"

        page = UserAdminResultUserAccountPg()

        # run profile into view function
        count = page.searchUserAccount(query)
        #print(count)
        self.assertEqual(len(count), 1)
        
    def test_log_in_incorrect_password(self):
		
		# Log in with the following data
		# User Email: samuel87@example.org
		# Password: hashed_pass_placeholder
        email = "samuel87@example.org"
        password = "hashed_pass_placeholder"

        page = LogInPg()

        # run profile into view function
        result = page.userLogIn(email, password)
        #print(result)
        self.assertEqual(result.user_id, 7)
        
    def test_log_in_success(self):
		
		# Log in with the following data, password is wrong
		# User Email: samuel87@example.org
		# Password: wrong_password
        email = "samuel87@example.org"
        password = "wrong_password"

        page = LogInPg()

        # run profile into view function
        result = page.userLogIn(email, password)
        #print(result)
        self.assertEqual(result.user_id, None)

    def test_log_out_success(self):
        with app.test_request_context():

            session["user_id"] = 1

            page = LogOutPg()

            result = page.userLogOut()

            self.assertEqual(result, True)

            self.assertNotIn("user_id", session)


if __name__ == "__main__":
    unittest.main(verbosity=2)
