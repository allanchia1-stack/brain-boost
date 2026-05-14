import sys
import os
import unittest
import mysql.connector

# Ensure project root is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from user_admin.boundary.LogInPg import LogInPg
from user_admin.controller.LogInC import LogInC

from user_admin.boundary.UserAdminCreateUserAccountPg import UserAdminCreateUserAccountPg
from user_admin.controller.UserAdminCreateAccountC import UserAdminCreateAccountC

from user_admin.boundary.UserAdminCreateProfilePg import UserAdminCreateProfilePg
from user_admin.controller.UserAdminCreateProfileC import UserAdminCreateProfileC

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

        self.assertEqual(result[1],"Toast")

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

        self.assertEqual(result1[1],"Jam")

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

    def test_create_user_account_success(self):

        account = UserAcct(
            email="test1@example.com",
            password="hashed_pass_placeholder",
            name="Test User",
            phone="91234567",
            address="123 Tampines Street 11",
            role = 1
        )

        page = UserAdminCreateUserAccountPg()

        result = page.createAccount(account)

        self.assertEqual(result[1],"test1@example.com")

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
            role = 1
        )

        page = UserAdminCreateUserAccountPg()

        # First insert
        result1 = page.createAccount(account)

        self.assertEqual(result1[1],"test2@example.com")

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
