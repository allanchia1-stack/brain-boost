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
            user='root',
            password='brain-boost',
            host='localhost',
            port = 3307,
            database='fundraising_db'
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
                SELECT a.user_id, a.account_password, p.profile_role
                FROM UserAcct a
                JOIN UserProf p ON a.user_id = p.user_id
                WHERE a.account_email = %s
                  AND a.account_status = 1
                  AND p.profile_role = 'FundRaiser'
                """,
                (email,),
            )
            account = cursor.fetchone()
            if account and account["account_password"] == password:
                return AuthenticatedUser(
                    id=account["user_id"],
                    email=email,
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

