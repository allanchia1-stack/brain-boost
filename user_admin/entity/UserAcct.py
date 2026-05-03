import mysql.connector
from dataclasses import dataclass


@dataclass
class AuthenticatedUser:
    id: int
    email: str
    role: str


class UserAcct:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            user="root",
            password="brain-boost",
            host="localhost",
            port=3306,
            database="fundraising_db",
        )

    @classmethod
    def authenticate(cls, email, password):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT account_id, account_email, account_password, account_role, account_status
                FROM UserAcct
                WHERE LOWER(account_email) = LOWER(%s)
                """,
                (email,),
            )
            account = cursor.fetchone()

            # account_status = 0 means suspended, so suspended users cannot login
            if (
                account
                and account["account_password"] == password
                and int(account.get("account_status", 1)) == 1
            ):
                return AuthenticatedUser(
                    id=account["account_id"],
                    email=account["account_email"],
                    role=account["account_role"],
                )
            return None
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    @classmethod
    def create_user(cls, name, phone, address, role, email, password):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()

            # UserProf is the role/profile lookup table in your SQL schema.
            # This prevents FK errors if the role does not exist yet.
            cursor.execute(
                """
                INSERT IGNORE INTO UserProf (profile_role, profile_status)
                VALUES (%s, 1)
                """,
                (role,),
            )

            cursor.execute(
                """
                INSERT INTO UserAcct
                (account_email, account_password, account_name, account_phone, account_address, account_role, account_status)
                VALUES (%s, %s, %s, %s, %s, %s, 1)
                """,
                (email.strip().lower(), password, name, phone, address, role),
            )
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error creating user: {err}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    @classmethod
    def get_all_accounts(cls):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT
                    account_id AS user_id,
                    account_id AS profile_id,
                    account_email,
                    account_name,
                    account_role,
                    account_status
                FROM UserAcct
                ORDER BY account_id
                """
            )
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    @classmethod
    def search_accounts(cls, query):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            like = f"%{query}%"
            cursor.execute(
                """
                SELECT
                    account_id AS user_id,
                    account_id AS profile_id,
                    account_email,
                    account_name,
                    account_role,
                    account_status
                FROM UserAcct
                WHERE CAST(account_id AS CHAR) LIKE %s
                   OR account_role LIKE %s
                   OR account_email LIKE %s
                   OR account_name LIKE %s
                ORDER BY account_id
                """,
                (like, like, like, like),
            )
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    @classmethod
    def get_account_by_user_id(cls, account_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT
                    account_id AS user_id,
                    account_id AS profile_id,
                    account_email,
                    account_name,
                    account_role,
                    account_status
                FROM UserAcct
                WHERE account_id = %s
                """,
                (account_id,),
            )
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    @classmethod
    def update_account(cls, account_id, email, password=None):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()

            if password:
                cursor.execute(
                    """
                    UPDATE UserAcct
                    SET account_email = %s, account_password = %s
                    WHERE account_id = %s
                    """,
                    (email.strip().lower(), password, account_id),
                )
            else:
                cursor.execute(
                    """
                    UPDATE UserAcct
                    SET account_email = %s
                    WHERE account_id = %s
                    """,
                    (email.strip().lower(), account_id),
                )

            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    @classmethod
    def suspend_account(cls, account_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE UserAcct SET account_status = 0 WHERE account_id = %s",
                (account_id,),
            )
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
