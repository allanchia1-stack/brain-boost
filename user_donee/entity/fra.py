import mysql.connector


class FRA:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            user="root",
            password="brain-boost",
            host="localhost",
            port = 3307,
            database="fundraising_db"
        )

    @classmethod
    def get_all_fras(cls):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT f.fra_id, f.fra_title, f.fra_des,
                       c.frc_name AS category_name,
                       f.fra_start_date, f.fra_end_date,
                       f.fra_donation_goal, f.fra_donation_amt,
                       f.fra_views, f.fra_num_of_fav, f.fra_status
                FROM FRA f
                JOIN FRC c ON f.fra_category = c.frc_id
                ORDER BY f.fra_create_date DESC
            """
            cursor.execute(query)
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
    def search_fras(cls, keyword):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            search_text = f"%{keyword}%"
            query = """
                SELECT f.fra_id, f.fra_title, f.fra_des,
                       c.frc_name AS category_name,
                       f.fra_start_date, f.fra_end_date,
                       f.fra_donation_goal, f.fra_donation_amt,
                       f.fra_views, f.fra_num_of_fav, f.fra_status
                FROM FRA f
                JOIN FRC c ON f.fra_category = c.frc_id
                WHERE f.fra_title LIKE %s OR c.frc_name LIKE %s
                ORDER BY f.fra_create_date DESC
            """
            cursor.execute(query, (search_text, search_text))
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
    def get_fra_by_id(cls, fra_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT f.fra_id, f.fra_title, f.fra_des,
                       c.frc_name AS category_name,
                       f.fra_start_date, f.fra_end_date,
                       f.fra_donation_goal, f.fra_donation_amt,
                       f.fra_views, f.fra_num_of_fav, f.fra_status
                FROM FRA f
                JOIN FRC c ON f.fra_category = c.frc_id
                WHERE f.fra_id = %s
            """
            cursor.execute(query, (fra_id,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
