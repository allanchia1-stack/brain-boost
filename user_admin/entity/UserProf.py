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
            cursor.execute(
                """
                SELECT
                    profile_id,
                    profile_role,
                    profile_status
                FROM UserProf
                ORDER BY profile_id
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
                    profile_id,
                    profile_role,
                    profile_status
                FROM UserProf
                WHERE CAST(profile_id AS CHAR) LIKE %s
                   OR profile_role LIKE %s
                   OR CAST(profile_status AS CHAR) LIKE %s
                ORDER BY profile_id
                """,
                (like, like, like),
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
                    profile_id,
                    profile_role,
                    profile_status
                FROM UserProf
                WHERE profile_id = %s
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
    def update_profile(cls, profile_id, role):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE UserProf
                SET profile_role = %s
                WHERE profile_id = %s
                """,
                (role, profile_id),
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
    def toggle_suspend_profile(cls, profile_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE UserProf
                SET profile_status = CASE
                    WHEN profile_status = 1 THEN 0
                    ELSE 1
                END
                WHERE profile_id = %s
                """,
                (profile_id,),
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
