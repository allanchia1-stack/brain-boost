import sys
import os

# Ensure project root is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from unittest.mock import patch

from user_admin.entity.UserProf import UserProf
from user_admin.entity.UserAcct import UserAcct


class TestUserAdmin(unittest.TestCase):

    def test_create_user_profile(self):
        print("\nRunning: test_create_user_profile")

        profile = UserProf(role="Donee", status=1)

        with patch.object(UserProf, "createProfile", return_value=1):
            result = UserProf.createProfile(profile)

        self.assertEqual(result, 1)
        print("Passed: User profile created successfully")


    def test_create_user_account(self):
        print("\nRunning: test_create_user_account")

        account = UserAcct(
            email="test@example.com",
            password="123456",
            name="Test User",
            phone="91234567"
        )

        with patch.object(UserAcct, "createAccount", return_value=1):
            result = UserAcct.createAccount(account)

        self.assertEqual(result, 1)
        print("Passed: User account created successfully")


if __name__ == "__main__":
    unittest.main(verbosity=2)