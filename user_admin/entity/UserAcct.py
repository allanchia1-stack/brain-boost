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
            database='fundraising_db'
        )

    @classmethod
    def authenticate(cls, email, password):
        conn = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)

            # Join UserAcct and UserProf to get password AND role at once
            query = """
                SELECT a.user_id, a.account_password, p.profile_role 
                FROM UserAcct a
                JOIN UserProf p ON a.user_id = p.user_id
                WHERE a.account_email = %s
            """
            cursor.execute(query, (email,))
            account = cursor.fetchone()

            # Password and account existence check 
            if account and account['account_password'] == password:
                return AuthenticatedUser(
                    id=account['user_id'],
                    email=email,
                    role=account['profile_role']
                )
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
            
            # Insert into User table
            cursor.execute("INSERT INTO User (user_name, user_email, user_password_hash) VALUES (%s, %s, %s)",
                           (name, email, password))
            user_id = cursor.lastrowid
            
            # Insert into UserAcct
            cursor.execute("INSERT INTO UserAcct (user_id, account_password, account_email) VALUES (%s, %s, %s)",
                           (user_id, password, email))
            
            # Insert into UserProf
            cursor.execute("INSERT INTO UserProf (user_id, profile_name, phone, address, profile_role) VALUES (%s, %s, %s, %s, %s)",
                           (user_id, name, phone, address, role))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error creating user: {e}")
            if conn:
                # Fail safe function in case it doesnt work, undo all database inserts
                conn.rollback()
            return False
            
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()