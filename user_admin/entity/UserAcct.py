import mysql.connector
from dataclasses import dataclass
from user_admin.entity.UserProf import UserProf


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
            database="fundraising_db",
        )

    def __init__(self, email=None, password=None, name=None, phone=None, address=None, role=None, account_id=None):
        self.account_id = account_id
        self.email = email
        self.password = password
        self.name = name
        self.phone = phone
        self.address = address
        self.role = role

    @classmethod
    def userLogin(cls, username, password_hash):
        return cls.authenticate(username, password_hash)

    @classmethod
    def authenticate(cls, email, password):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT a.account_id, a.account_email, a.account_password, p.profile_role, a.account_status
                FROM UserAcct a
                INNER JOIN UserProf p ON a.account_role_id = p.profile_id
                WHERE LOWER(a.account_email) = LOWER(%s)
                """,
                (email,),
            )
            account = cursor.fetchone()
            if account and account["account_password"] == password and int(account.get("account_status", 1)) == 1:
                return AuthenticatedUser(
                    id=account["account_id"],
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
    def create_user(cls, name, phone, address, role, email, password):
        return cls.createAccount(cls(email=email, password=password, name=name, phone=phone, address=address, role=role))

    @classmethod
    def createAccount(cls, temp):
        print("Executing UserAcct.createAccount()")
        conn = None
        cursor = None
        try:
            role_id = UserProf.get_profile_id_by_role(temp.role)
            if role_id is None:
                return False
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO UserAcct
                (account_email, account_password, account_name, account_phone, account_address, account_role_id, account_status)
                VALUES (%s, %s, %s, %s, %s, %s, 1)
                """,
                (temp.email.strip().lower(), temp.password, temp.name, temp.phone, temp.address, role_id),
            )
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error creating user account: {err}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    @classmethod
    def view(cls, accountId):
        return cls.get_account_by_user_id(accountId)

    @classmethod
    def updateUser(cls, temp):
        return cls.update_account(temp.account_id, temp.email, temp.password, temp.name, temp.phone, temp.address, temp.role)

    @classmethod
    def SuspendUserAccount(cls, idNum):
        return cls.toggle_suspend_account(idNum)

    @classmethod
    def queryUserAccount(cls, user_id_match):
        return cls.search_accounts(user_id_match)

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
                    a.account_id AS user_id,
                    a.account_id,
                    a.account_role_id AS profile_id,
                    a.account_email,
                    a.account_name,
                    a.account_phone,
                    a.account_address,
                    p.profile_role,
                    a.account_status
                FROM UserAcct a
                INNER JOIN UserProf p ON a.account_role_id = p.profile_id
                ORDER BY a.account_id
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
    def search_accounts(cls, user_email):
        conn = None
        cursor = None

        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT
                    a.account_id AS user_id,
                    a.account_id,
                    a.account_role_id AS profile_id,
                    a.account_email,
                    a.account_name,
                    a.account_phone,
                    a.account_address,
                    p.profile_role,
                    a.account_status
                FROM UserAcct a
                INNER JOIN UserProf p 
                    ON a.account_role_id = p.profile_id
                WHERE a.account_email LIKE %s
                """,
                (f"%{user_email}%",)
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
                    a.account_id AS user_id,
                    a.account_id,
                    a.account_role_id AS profile_id,
                    a.account_email,
                    a.account_name,
                    a.account_phone,
                    a.account_address,
                    p.profile_role,
                    a.account_status
                FROM UserAcct a
                INNER JOIN UserProf p ON a.account_role_id = p.profile_id
                WHERE a.account_id = %s
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
    def update_account(cls, account_id, email, password=None, name=None, phone=None, address=None, role=None):
        conn = None
        cursor = None
        try:
            role_id = UserProf.get_profile_id_by_role(role) if role else None
            conn = cls.get_connection()
            cursor = conn.cursor()
            fields = ["account_email = %s"]
            values = [email.strip().lower()]
            if password:
                fields.append("account_password = %s")
                values.append(password)
            if name is not None:
                fields.append("account_name = %s")
                values.append(name)
            if phone is not None:
                fields.append("account_phone = %s")
                values.append(phone)
            if address is not None:
                fields.append("account_address = %s")
                values.append(address)
            if role_id is not None:
                fields.append("account_role_id = %s")
                values.append(role_id)
            values.append(account_id)
            cursor.execute(f"UPDATE UserAcct SET {', '.join(fields)} WHERE account_id = %s", tuple(values))
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
    def toggle_suspend_account(cls, account_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE UserAcct
                SET account_status = CASE WHEN account_status = 1 THEN 0 ELSE 1 END
                WHERE account_id = %s
                """,
                (account_id,),
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
