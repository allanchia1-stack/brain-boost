import mysql.connector


class FRA:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            user="root",
            password="brain-boost",
            host="localhost",
            database="fundraising_db"
        )

    @classmethod
    def get_all_fras(cls):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT f.fra_id, f.fra_title, f.fra_des,
                       c.frc_name AS category_name,
                       f.fra_start_date, f.fra_end_date,
                       f.fra_donation_goal, f.fra_donation_amt,
                       f.fra_views, f.fra_num_of_fav, f.fra_status
                FROM FRA f
                JOIN FRC c ON f.fra_category = c.frc_id
                ORDER BY f.fra_create_date DESC
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
    def searchFra(cls, query):
        #print("Executing FRA.searchFra()")
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            search_text = f"%{query}%"
            cursor.execute(
                """
                SELECT f.fra_id, f.fra_title, f.fra_des,
                       c.frc_name AS category_name,
                       f.fra_start_date, f.fra_end_date,
                       f.fra_donation_goal, f.fra_donation_amt,
                       f.fra_views, f.fra_num_of_fav, f.fra_status
                FROM FRA f
                JOIN FRC c ON f.fra_category = c.frc_id
                WHERE f.fra_title LIKE %s
                   OR f.fra_des LIKE %s
                   OR c.frc_name LIKE %s
                ORDER BY f.fra_create_date DESC
                """,
                (search_text, search_text, search_text)
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
    def view(cls, fra_id):
        #print("Executing FRA.view()")
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT f.fra_id, f.fra_title, f.fra_des,
                       c.frc_name AS category_name,
                       f.fra_start_date, f.fra_end_date,
                       f.fra_donation_goal, f.fra_donation_amt,
                       f.fra_views, f.fra_num_of_fav, f.fra_status
                FROM FRA f
                JOIN FRC c ON f.fra_category = c.frc_id
                WHERE f.fra_id = %s
                """,
                (fra_id,)
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
    def increment_fra_views(cls, fra_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE FRA
                SET fra_views = fra_views + 1
                WHERE fra_id = %s
                """,
                (fra_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
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
    def is_saved(cls, acct_id, fra_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT fav_id FROM FavouriteFRA WHERE user_id = %s AND fra_id = %s",
                (acct_id, fra_id)
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
    def saveFra(cls, acct_id, fra_id):
        #print("Executing FRA.saveFra()")
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT IGNORE INTO FavouriteFRA (user_id, fra_id) VALUES (%s, %s)",
                (acct_id, fra_id)
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
    def unsaveFra(cls, acct_id, fra_id):
        print("Executing FRA.unsaveFra()")
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM FavouriteFRA WHERE user_id = %s AND fra_id = %s",
                (acct_id, fra_id)
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
    def doneeViewFavFra(cls, fra_id):
        #print("Executing FRA.doneeViewFavFra()")
        return cls.view(fra_id)

    @classmethod
    def viewAllFraFav(cls, user_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
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
                """,
                (user_id,)
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
    def searchFraFav(cls, user_id, query):
        #print("Executing FRA.searchFraFav()")
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            search_text = f"%{query}%"
            cursor.execute(
                """
                SELECT f.fra_id, f.fra_title, f.fra_des,
                       c.frc_name AS category_name,
                       f.fra_start_date, f.fra_end_date,
                       f.fra_donation_goal, f.fra_donation_amt,
                       f.fra_views, f.fra_num_of_fav, fav.fav_saved_at
                FROM FavouriteFRA fav
                JOIN FRA f ON fav.fra_id = f.fra_id
                JOIN FRC c ON f.fra_category = c.frc_id
                WHERE fav.user_id = %s
                  AND (f.fra_title LIKE %s OR f.fra_des LIKE %s OR c.frc_name LIKE %s)
                ORDER BY fav.fav_saved_at DESC
                """,
                (user_id, search_text, search_text, search_text)
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
