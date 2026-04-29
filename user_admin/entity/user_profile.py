import mysql.connector


class UserProfile:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            user='root',
            password='brain-boost',
            host='localhost',
            database='fundraising_db'
        )

    @classmethod
    def get_all_profiles(cls):
        conn = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT profile_id, profile_name, phone, address, profile_role, profile_status
                FROM UserProf
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
    def search_profiles(cls, query):
        conn = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            like = f"%{query}%"
            cursor.execute("""
                SELECT profile_id, profile_name, phone, address, profile_role, profile_status
                FROM UserProf
                WHERE profile_id LIKE %s
                   OR profile_name LIKE %s
                   OR phone LIKE %s
                   OR address LIKE %s
                   OR profile_role LIKE %s
            """, (like, like, like, like, like))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return []
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @classmethod
    def get_profile_by_id(cls, profile_id):
        conn = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT profile_id, profile_name, phone, address, profile_role, profile_status
                FROM UserProf
                WHERE profile_id = %s
            """, (profile_id,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return None
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
