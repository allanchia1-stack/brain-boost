import mysql.connector


class FRC:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            user='root',
            password='brain-boost',
            host='localhost',
            port=3307,
            database='fundraising_db'
        )

    @classmethod
    def create_frc(cls, name, description, status=1):
        conn = cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO FRC (frc_name, frc_des, frc_status) VALUES (%s, %s, %s)",
                (name, description, status)
            )
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @classmethod
    def get_all_frcs(cls):
        conn = cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT frc_id AS id, frc_name AS name, frc_des AS description, "
                "frc_status AS status FROM FRC ORDER BY frc_name"
            )
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return []
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @classmethod
    def search_frcs(cls, query):
        conn = cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            like = f"%{query}%"
            cursor.execute(
                "SELECT frc_id AS id, frc_name AS name, frc_des AS description, "
                "frc_status AS status FROM FRC "
                "WHERE frc_name LIKE %s OR frc_des LIKE %s ORDER BY frc_name",
                (like, like)
            )
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return []
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @classmethod
    def get_frc_by_id(cls, frc_id):
        conn = cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT frc_id AS id, frc_name AS name, frc_des AS description, "
                "frc_status AS status FROM FRC WHERE frc_id = %s",
                (frc_id,)
            )
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return None
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @classmethod
    def update_frc(cls, frc_id, name, description, status):
        conn = cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE FRC SET frc_name = %s, frc_des = %s, frc_status = %s WHERE frc_id = %s",
                (name, description, status, frc_id)
            )
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            if conn: conn.rollback()
            return False
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @classmethod
    def suspend_frc(cls, frc_id):
        conn = cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE FRC SET frc_status = 0 WHERE frc_id = %s",
                (frc_id,)
            )
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            if conn: conn.rollback()
            return False
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @classmethod
    def unsuspend_frc(cls, frc_id):
        conn = cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE FRC SET frc_status = 1 WHERE frc_id = %s",
                (frc_id,)
            )
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            if conn: conn.rollback()
            return False
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()
