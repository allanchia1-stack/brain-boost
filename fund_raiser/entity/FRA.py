from datetime import datetime
import mysql.connector


class FRA:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            user='root',
            password='brain-boost',
            host='localhost',
            port = 3307,
            database='fundraising_db'
        )

    @classmethod
    def get_categories(cls):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT frc_id, frc_name
                FROM FRC
                WHERE frc_status = 1
                ORDER BY frc_name
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
    def create_fra(
        cls,
        title,
        category_id,
        start_date,
        end_date,
        goal,
        description,
        owner_id,
    ):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO FRA (
                    fra_title, fra_des, fra_donation_goal, fra_start_date,
                    fra_end_date, fra_category, fra_owner_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    title,
                    description,
                    goal,
                    datetime.combine(start_date, datetime.min.time()),
                    datetime.combine(end_date, datetime.min.time()),
                    category_id,
                    owner_id,
                ),
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
    def get_all_fras(cls, owner_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT f.fra_id, f.fra_title, c.frc_name, f.fra_donation_goal,
                       f.fra_donation_amt, f.fra_start_date, f.fra_end_date,
                       f.fra_status
                FROM FRA f
                JOIN FRC c ON f.fra_category = c.frc_id
                WHERE f.fra_owner_id = %s
                ORDER BY f.fra_create_date DESC
                """,
                (owner_id,),
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
    def get_ongoing_fras(cls, owner_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT f.fra_id, f.fra_title, c.frc_name, f.fra_donation_goal,
                    f.fra_donation_amt, f.fra_start_date, f.fra_end_date,
                    f.fra_status
                FROM FRA f
                JOIN FRC c ON f.fra_category = c.frc_id
                WHERE f.fra_status = 'ongoing'
                  AND f.fra_owner_id = %s
                ORDER BY f.fra_create_date DESC
                """,
                (owner_id,),
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
    def get_completed_fras(cls, owner_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT f.fra_id, f.fra_title, c.frc_name, f.fra_donation_goal,
                    f.fra_donation_amt, f.fra_start_date, f.fra_end_date,
                    f.fra_status
                FROM FRA f
                JOIN FRC c ON f.fra_category = c.frc_id
                WHERE f.fra_status = 'completed'
                  AND f.fra_owner_id = %s
                ORDER BY f.fra_create_date DESC
                """,
                (owner_id,),
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
    def search_fras(cls, query, owner_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            like = f"%{query}%"
            cursor.execute(
                """
                SELECT f.fra_id, f.fra_title, c.frc_name, f.fra_donation_goal,
                       f.fra_donation_amt, f.fra_start_date, f.fra_end_date,
                       f.fra_status
                FROM FRA f
                JOIN FRC c ON f.fra_category = c.frc_id
                WHERE f.fra_owner_id = %s
                  AND (
                    CAST(f.fra_id AS CHAR) LIKE %s
                    OR f.fra_title LIKE %s
                    OR c.frc_name LIKE %s
                    OR f.fra_status LIKE %s
                  )
                ORDER BY f.fra_create_date DESC
                """,
                (owner_id, like, like, like, like),
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
    def get_fra_by_id(cls, fra_id, owner_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT f.fra_id, f.fra_title, f.fra_des, f.fra_category,
                       c.frc_name,
                       f.fra_donation_goal, f.fra_donation_amt,
                       f.fra_create_date, f.fra_start_date, f.fra_end_date,
                       f.fra_views, f.fra_num_of_fav, f.fra_status,
                       u.user_name AS owner_name
                FROM FRA f
                JOIN FRC c ON f.fra_category = c.frc_id
                JOIN User u ON f.fra_owner_id = u.user_id
                WHERE f.fra_id = %s
                  AND f.fra_owner_id = %s
                """,
                (fra_id, owner_id),
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
    def get_fras_by_category(cls, category_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT f.fra_id, f.fra_title, f.fra_start_date, f.fra_end_date,
                       f.fra_donation_goal, f.fra_category
                FROM FRA f
                WHERE f.fra_category = %s
                ORDER BY f.fra_create_date DESC
                """,
                (category_id,),
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
    def get_fra_by_id_for_manager(cls, fra_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT f.fra_id, f.fra_title, f.fra_des, f.fra_category,
                       c.frc_name, f.fra_donation_goal, f.fra_donation_amt,
                       f.fra_create_date, f.fra_start_date, f.fra_end_date,
                       f.fra_views, f.fra_num_of_fav, f.fra_status,
                       u.user_name AS owner_name
                FROM FRA f
                JOIN FRC c ON f.fra_category = c.frc_id
                JOIN User u ON f.fra_owner_id = u.user_id
                WHERE f.fra_id = %s
                """,
                (fra_id,),
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
    def update_fra(
        cls,
        fra_id,
        owner_id,
        title,
        category_id,
        start_date,
        end_date,
        goal,
        description,
    ):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE FRA
                SET fra_title = %s,
                    fra_des = %s,
                    fra_donation_goal = %s,
                    fra_start_date = %s,
                    fra_end_date = %s,
                    fra_category = %s
                WHERE fra_id = %s
                  AND fra_owner_id = %s
                """,
                (
                    title,
                    description,
                    goal,
                    datetime.combine(start_date, datetime.min.time()),
                    datetime.combine(end_date, datetime.min.time()),
                    category_id,
                    fra_id,
                    owner_id,
                ),
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
    def suspend_fra(cls, fra_id, owner_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE FRA
                SET fra_status = 'cancelled'
                WHERE fra_id = %s
                  AND fra_owner_id = %s
                """,
                (fra_id, owner_id),
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
