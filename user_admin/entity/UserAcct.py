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
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.account_id, a.account_password, a.account_role
                FROM UserAcct a
                WHERE a.account_email = %s
            """, (email,))
            account = cursor.fetchone()
            if account and account['account_password'] == password:
                return AuthenticatedUser(id=account['account_id'], email=email, role=account['account_role'])
            return None
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return None
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @classmethod
    def create_user(cls, name, phone, address, role, email, password):
        conn = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            #cursor.execute("INSERT INTO User (user_name, user_email, user_password_hash) VALUES (%s, %s, %s)",
            #               (name, email, password))
            #user_id = cursor.lastrowid
            cursor.execute("INSERT INTO UserAcct (account_email, account_password, account_name, account_phone, account_address, account_role) VALUES (%s, %s, %s, %s, %s, %s)",
                           (email, password, name, phone, address, role))
            #cursor.execute("INSERT INTO UserProf (user_id, profile_name, phone, address, profile_role) VALUES (%s, %s, %s, %s, %s)",
            #               (user_id, name, phone, address, role))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @classmethod
    def get_all_accounts(cls):
        conn = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.account_email, a.account_name, a.account_role, a.account_status
                FROM UserAcct a;
            """)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return []
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @classmethod
    def search_accounts(cls, query):
        conn = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            like = f"%{query}%"
            cursor.execute("""
                SELECT a.account_id, a.account_role, a.account_email, a.account_name, a.account_status
                FROM UserAcct a
                WHERE CAST(a.account_id AS CHAR) LIKE %s
                   OR a.account_role LIKE %s
                   OR a.account_email LIKE %s
                   OR a.account_name LIKE %s
            """, (like, like, like, like))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return []
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @classmethod
    def get_account_by_user_id(cls, account_id):
        conn = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.account_id, a.account_email, a.account_name, a.account_status
                FROM UserAcct a
                WHERE a.account_id = %s
            """, (account_id,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return None
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @classmethod
    def update_account(cls, account_id, email, password, name, phone, address, role):
        conn = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE UserAcct SET account_email = %s, account_password = %s, account_name = %s, account_phone = %s, account_address = %s, account_status = %s
                WHERE account_id = %s
            """, (email, password, name, phone, address, role, account_id))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @classmethod
    def suspend_account(cls, account_id):
        conn = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE UserAcct SET account_status = 0 WHERE account_id = %s
            """, (account_id,))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
