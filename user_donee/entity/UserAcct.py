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
            database="fundraising_db"
        )

    @classmethod
    def userLogin(cls, username, password_hash):
        """Entity method for Donee login.
        In your current database, username = account_email and password_hash = account_password.
        """
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT a.user_id, a.account_email, a.account_password, p.profile_role
                FROM UserAcct a
                JOIN UserProf p ON a.user_id = p.user_id
                WHERE a.account_email = %s
                  AND a.account_status = 1
                  AND p.profile_role = 'Donee'
                """,
                (username,),
            )
            account = cursor.fetchone()

            if account and account["account_password"] == password_hash:
                return AuthenticatedUser(
                    id=account["user_id"],
                    email=account["account_email"],
                    role=account["profile_role"],
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
    def authenticate(cls, email, password):
        return cls.userLogin(email, password)
