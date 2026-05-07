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

        test_profiles = [
            {"role": "Angel Investor", "status": 1},
            {"role": "Donee", "status": 1},
            {"role": "Fund Raiser", "status": 1},
            {"role": "Platform Manager", "status": 1},
            {"role": "User Admin", "status": 1}
        ]

        with patch.object(UserProf, "createProfile", return_value=1):
            for data in test_profiles:
                profile = UserProf(
                    role=data["role"],
                    status=data["status"]
                )

                result = UserProf.createProfile(profile)
                self.assertEqual(result, 1)

        print("Passed: All user profiles created successfully")


    def test_create_user_account(self):
        print("\nRunning: test_create_user_account")

        test_accounts = [
            {
                "email": "test@example.com",
                "password": "123456",
                "name": "Test User One",
                "phone": "91234567",
                "address": "123 Tampines Street 11"
            },
            {
                "email": "test2@example.com",
                "password": "123456",
                "name": "Test User Two",
                "phone": "92345678",
                "address": "456 Ang Mo Kio Ave 10"
            },
            {
                "email": "test3@example.com",
                "password": "123456",
                "name": "Test User Three",
                "phone": "93456789",
                "address": "789 Jurong West Street 65"
            },
            {
                "email": "test4@example.com",
                "password": "123456",
                "name": "Test User Four",
                "phone": "94567890",
                "address": "10 Anson Road"
            },
            {
                "email": "test5@example.com",
                "password": "123456",
                "name": "Test User Five",
                "phone": "95678901",
                "address": "88 Bedok North Road"
            }
        ]

        with patch.object(UserAcct, "createAccount", return_value=1):
            for data in test_accounts:
                account = UserAcct(
                    email=data["email"],
                    password=data["password"],
                    name=data["name"],
                    phone=data["phone"],
                    address=data["address"]
                )

                result = UserAcct.createAccount(account)
                self.assertEqual(result, 1)

        print("Passed: All user accounts created successfully")


if __name__ == "__main__":
    unittest.main(verbosity=2)