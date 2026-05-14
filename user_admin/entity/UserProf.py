import mysql.connector


class UserProf:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            user="root",
            password="brain-boost",
            host="localhost",
            database="fundraising_db",
        )

    def __init__(self, role=None, status=1, profile_id=None):
        self.profile_id = profile_id
        self.role = role
        self.status = status

    @classmethod
    def createProfile(cls, temp):
        #print("Running userprof.createProfile()")
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO UserProf (profile_role, profile_status)
                VALUES (%s, %s)
                """,
                (temp.role, temp.status),
            )
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error creating user profile: {err}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    @classmethod
    def get_all_profiles(cls):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT profile_id, profile_role, profile_status
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
    def queryUserProfile(cls, query):
        #print("Executing userprof.queryUserProfile()")
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
                ORDER BY profile_id
                """,
                (like, like)
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
    def view(cls, profile_id):
        
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT profile_id, profile_role, profile_status
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
    def get_profile_id_by_role(cls, role):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT profile_id FROM UserProf WHERE profile_role = %s LIMIT 1", (role,))
            row = cursor.fetchone()
            if row:
                return row["profile_id"]
            cursor.execute("INSERT INTO UserProf (profile_role, profile_status) VALUES (%s, 1)", (role,))
            conn.commit()
            return cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            if conn:
                conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    @classmethod
    def updateProf(cls, temp):
        #print("Executing userprof.updateProf()")
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE UserProf SET profile_role = %s WHERE profile_id = %s",
                (temp.role, temp.profile_id),
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
    def suspendProf(cls, profile_id):
        
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE UserProf
                SET profile_status = CASE WHEN profile_status = 1 THEN 0 ELSE 1 END
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

# Backward-compatible name for older imports.
UserProfile = UserProf
