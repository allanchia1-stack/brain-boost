from datetime import datetime
import mysql.connector


class FRA:

    def __init__(self, title, category_id, start_date, end_date, goal, description, owner_id):
        self.title = title
        self.category_id = category_id
        self.start_date = start_date
        self.end_date = end_date
        self.goal = goal
        self.description = description
        self.owner_id = owner_id

    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            user='root',
            password='brain-boost',
            host='localhost',
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
    def createFra(cls, temp):
        print("Executing FRA.createFra()")
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
                    temp.title,
                    temp.description,
                    temp.goal,
                    datetime.combine(temp.start_date, datetime.min.time()),
                    datetime.combine(temp.end_date, datetime.min.time()),
                    temp.category_id,
                    temp.owner_id,
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
    def viewFraHistory(cls, owner_id):
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
    def searchFra(cls, query, owner_id):
        print("Executing FRA.searchFra()")
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
    def viewFraById(cls, fra_id, owner_id):
        print("Executing FRA.viewFraById")
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
                       ua.account_name AS owner_name
                FROM FRA f
                JOIN FRC c ON f.fra_category = c.frc_id
                JOIN UserAcct ua ON f.fra_owner_id = ua.account_id
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
                       ua.account_name AS owner_name
                FROM FRA f
                JOIN FRC c ON f.fra_category = c.frc_id
                JOIN UserAcct ua ON f.fra_owner_id = ua.account_id
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
    def updateFra(cls, fra_id, temp, owner_id):
        print("Executing FRA.updateFRA()")
        title = temp.title
        description = temp.description
        try:
            category_id = int(temp.category_id)
            start_date = temp.start_date
            end_date = temp.end_date
            goal = int(temp.goal)
        except ValueError:
            return False, "Please enter a valid category, date range, and donation goal."
        
        print("start_date : ", start_date)
        print("end_date : ", end_date)
        if not title or not category_id or not start_date or not end_date or not goal:
            return None
        if not owner_id:
            return None
        if end_date < start_date:
            return None
        if goal <= 0:
            return None

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
            return temp
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
    def suspendFra(cls, fra_id, owner_id):
        print("Executing FRA.suspendFra()")
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

            row = cursor.fetchone()

            if not row:
                return None

            temp = FRA(
                title=row["fra_title"],
                category_id=row["fra_category"],
                start_date=row["fra_start_date"],
                end_date=row["fra_end_date"],
                goal=row["fra_donation_goal"],
                description=row["fra_des"],
                owner_id=row["fra_owner_id"]
            )

            return temp

            #return True
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
    def searchFraHis(cls,query, owner_id):
        pass

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
                (fra_id,),
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
        
