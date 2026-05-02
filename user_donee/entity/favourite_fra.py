import mysql.connector
from user_donee.entity.fra import FRA


class FavouriteFRA:
    @staticmethod
    def get_connection():
        return FRA.get_connection()

    @classmethod
    def is_saved(cls, user_id, fra_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT fav_id FROM FavouriteFRA WHERE user_id = %s AND fra_id = %s",
                (user_id, fra_id)
            )
            return cursor.fetchone() is not None
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    @classmethod
    def save_fra(cls, user_id, fra_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT IGNORE INTO FavouriteFRA (user_id, fra_id) VALUES (%s, %s)",
                (user_id, fra_id)
            )
            if cursor.rowcount > 0:
                cursor.execute(
                    "UPDATE FRA SET fra_num_of_fav = fra_num_of_fav + 1 WHERE fra_id = %s",
                    (fra_id,)
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
    def unsave_fra(cls, user_id, fra_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM FavouriteFRA WHERE user_id = %s AND fra_id = %s",
                (user_id, fra_id)
            )
            if cursor.rowcount > 0:
                cursor.execute(
                    "UPDATE FRA SET fra_num_of_fav = GREATEST(fra_num_of_fav - 1, 0) WHERE fra_id = %s",
                    (fra_id,)
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
    def get_favourite_fras(cls, user_id):
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
                       f.fra_views, f.fra_num_of_fav, fav.fav_saved_at
                FROM FavouriteFRA fav
                JOIN FRA f ON fav.fra_id = f.fra_id
                JOIN FRC c ON f.fra_category = c.frc_id
                WHERE fav.user_id = %s
                ORDER BY fav.fav_saved_at DESC
            """
            cursor.execute(query, (user_id,))
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
    def search_favourite_fras(cls, user_id, keyword):
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
                       f.fra_views, f.fra_num_of_fav, fav.fav_saved_at
                FROM FavouriteFRA fav
                JOIN FRA f ON fav.fra_id = f.fra_id
                JOIN FRC c ON f.fra_category = c.frc_id
                WHERE fav.user_id = %s
                  AND (f.fra_title LIKE %s OR c.frc_name LIKE %s)
                ORDER BY fav.fav_saved_at DESC
            """
            cursor.execute(query, (user_id, search_text, search_text))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
