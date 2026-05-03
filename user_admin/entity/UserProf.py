import mysql.connector


class UserProfile:
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
    def get_all_profiles(cls):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            # In your current SQL, the real user details are stored in UserAcct.
            # We alias them as UserProf fields so your boundary/template can follow the BCE diagram names.
            cursor.execute(
                """
                SELECT
                    account_id AS profile_id,
                    account_name AS profile_name,
                    account_phone AS phone,
                    account_address AS address,
                    account_role AS profile_role,
                    account_status AS profile_status
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
    def search_profiles(cls, query):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            like = f"%{query}%"
            cursor.execute(
                """
                SELECT
                    account_id AS profile_id,
                    account_name AS profile_name,
                    account_phone AS phone,
                    account_address AS address,
                    account_role AS profile_role,
                    account_status AS profile_status
                FROM UserAcct
                WHERE CAST(account_id AS CHAR) LIKE %s
                   OR account_name LIKE %s
                   OR account_phone LIKE %s
                   OR account_address LIKE %s
                   OR account_role LIKE %s
                ORDER BY account_id
                """,
                (like, like, like, like, like),
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
    def get_profile_by_id(cls, profile_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT
                    account_id AS profile_id,
                    account_name AS profile_name,
                    account_phone AS phone,
                    account_address AS address,
                    account_role AS profile_role,
                    account_status AS profile_status
                FROM UserAcct
                WHERE account_id = %s
                """,
                (profile_id,),
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
    def update_profile(cls, profile_id, name, phone, address, role):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT IGNORE INTO UserProf (profile_role, profile_status)
                VALUES (%s, 1)
                """,
                (role,),
            )

            cursor.execute(
                """
                UPDATE UserAcct
                SET account_name = %s,
                    account_phone = %s,
                    account_address = %s,
                    account_role = %s
                WHERE account_id = %s
                """,
                (name, phone, address, role, profile_id),
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
    def suspend_profile(cls, profile_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE UserAcct SET account_status = 0 WHERE account_id = %s",
                (profile_id,),
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
