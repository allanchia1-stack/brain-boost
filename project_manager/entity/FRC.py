import mysql.connector


class FRC:

    def __init__(self, name, description, status):
        self.name = name
        self.description = description
        self.status = status

    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            user='root',
            password='brain-boost',
            host='localhost',
            database='fundraising_db'
        )

    @classmethod
    def _fetch_all(cls, query, params=()):
        conn = cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
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
    def _fetch_one(cls, query, params=()):
        conn = cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
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
    def _execute_write(cls, query, params=()):
        conn = cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
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
    def createFrc(cls, temp):
        print("Executing FRC.createFrc()")
        return cls._execute_write(
            "INSERT INTO FRC (frc_name, frc_des, frc_status) VALUES (%s, %s, %s)",
            (temp.name, temp.description, temp.status),
        )

    @classmethod
    def get_all_frcs(cls):
        return cls._fetch_all(
            "SELECT frc_id AS id, frc_name AS name, frc_des AS description, "
            "frc_status AS status FROM FRC ORDER BY frc_name"
        )

    @classmethod
    def search_frcs(cls, query):
        like = f"%{query}%"
        return cls._fetch_all(
            "SELECT frc_id AS id, frc_name AS name, frc_des AS description, "
            "frc_status AS status FROM FRC "
            "WHERE frc_name LIKE %s OR frc_des LIKE %s ORDER BY frc_name",
            (like, like),
        )

    @classmethod
    def get_frc_by_id(cls, frc_id):
        return cls._fetch_one(
            "SELECT frc_id AS id, frc_name AS name, frc_des AS description, "
            "frc_status AS status FROM FRC WHERE frc_id = %s",
            (frc_id,),
        )

    @classmethod
    def update_frc(cls, frc_id, name, description, status):
        return cls._execute_write(
            "UPDATE FRC SET frc_name = %s, frc_des = %s, frc_status = %s WHERE frc_id = %s",
            (name, description, status, frc_id),
        )

    @classmethod
    def suspend_frc(cls, frc_id):
        return cls._execute_write(
            "UPDATE FRC SET frc_status = 0 WHERE frc_id = %s",
            (frc_id,),
        )

    @classmethod
    def unsuspend_frc(cls, frc_id):
        return cls._execute_write(
            "UPDATE FRC SET frc_status = 1 WHERE frc_id = %s",
            (frc_id,),
        )
