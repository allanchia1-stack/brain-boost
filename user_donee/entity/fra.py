import mysql.connector


class FRA:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            user='root',
            password='brain-boost',
            host='localhost',
            database='fundraising_db'
        )

    @classmethod
    def get_all_fras(cls, user_id=None, search_query=""):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)

            saved_join = """
                LEFT JOIN FavouriteFRA fav
                    ON fav.fra_id = f.fra_id AND fav.user_id = %s
            """ if user_id else ""

            params = []
            if user_id:
                params.append(user_id)

            where_sql = "WHERE f.fra_status = 'ongoing'"
            if search_query:
                where_sql += " AND (f.fra_title LIKE %s OR c.frc_name LIKE %s)"
                like_value = f"%{search_query}%"
                params.extend([like_value, like_value])

            query = f"""
                SELECT
                    f.fra_id,
                    f.fra_title,
                    f.fra_des,
                    c.frc_name AS category_name,
                    f.fra_start_date,
                    f.fra_end_date,
                    f.fra_donation_goal,
                    f.fra_donation_amt,
                    f.fra_views,
                    COUNT(allfav.fav_id) AS fra_num_of_fav,
                    {"CASE WHEN fav.fav_id IS NULL THEN 0 ELSE 1 END AS is_saved" if user_id else "0 AS is_saved"}
                FROM FRA f
                JOIN FRC c ON f.fra_category = c.frc_id
                LEFT JOIN FavouriteFRA allfav ON allfav.fra_id = f.fra_id
                {saved_join}
                {where_sql}
                GROUP BY
                    f.fra_id, f.fra_title, f.fra_des, c.frc_name,
                    f.fra_start_date, f.fra_end_date, f.fra_donation_goal,
                    f.fra_donation_amt, f.fra_views
                    {", fav.fav_id" if user_id else ""}
                ORDER BY f.fra_start_date DESC
            """
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
    def get_fra_by_id(cls, fra_id, user_id=None):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)

            saved_join = """
                LEFT JOIN FavouriteFRA fav
                    ON fav.fra_id = f.fra_id AND fav.user_id = %s
            """ if user_id else ""

            params = []
            if user_id:
                params.append(user_id)
            params.append(fra_id)

            query = f"""
                SELECT
                    f.fra_id,
                    f.fra_title,
                    f.fra_des,
                    c.frc_name AS category_name,
                    f.fra_start_date,
                    f.fra_end_date,
                    f.fra_donation_goal,
                    f.fra_donation_amt,
                    f.fra_views,
                    COUNT(allfav.fav_id) AS fra_num_of_fav,
                    {"CASE WHEN fav.fav_id IS NULL THEN 0 ELSE 1 END AS is_saved" if user_id else "0 AS is_saved"}
                FROM FRA f
                JOIN FRC c ON f.fra_category = c.frc_id
                LEFT JOIN FavouriteFRA allfav ON allfav.fra_id = f.fra_id
                {saved_join}
                WHERE f.fra_id = %s
                GROUP BY
                    f.fra_id, f.fra_title, f.fra_des, c.frc_name,
                    f.fra_start_date, f.fra_end_date, f.fra_donation_goal,
                    f.fra_donation_amt, f.fra_views
                    {", fav.fav_id" if user_id else ""}
            """
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
    def toggle_favourite(cls, user_id, fra_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT fav_id FROM FavouriteFRA WHERE user_id = %s AND fra_id = %s",
                (user_id, fra_id)
            )
            existing = cursor.fetchone()

            if existing:
                cursor.execute(
                    "DELETE FROM FavouriteFRA WHERE user_id = %s AND fra_id = %s",
                    (user_id, fra_id)
                )
                saved = False
            else:
                cursor.execute(
                    "INSERT INTO FavouriteFRA (user_id, fra_id) VALUES (%s, %s)",
                    (user_id, fra_id)
                )
                saved = True

            cursor.execute(
                """
                UPDATE FRA
                SET fra_num_of_fav = (
                    SELECT COUNT(*) FROM FavouriteFRA WHERE FavouriteFRA.fra_id = FRA.fra_id
                )
                WHERE fra_id = %s
                """,
                (fra_id,)
            )
            conn.commit()
            return saved

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
    def get_favourite_fras(cls, user_id, search_query=""):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)

            params = [user_id]
            where_sql = "WHERE fav.user_id = %s"
            if search_query:
                where_sql += " AND (f.fra_title LIKE %s OR c.frc_name LIKE %s)"
                like_value = f"%{search_query}%"
                params.extend([like_value, like_value])

            query = f"""
                SELECT
                    f.fra_id,
                    f.fra_title,
                    c.frc_name AS category_name,
                    f.fra_start_date,
                    f.fra_end_date,
                    f.fra_donation_goal,
                    f.fra_views,
                    COUNT(allfav.fav_id) AS fra_num_of_fav,
                    1 AS is_saved
                FROM FavouriteFRA fav
                JOIN FRA f ON fav.fra_id = f.fra_id
                JOIN FRC c ON f.fra_category = c.frc_id
                LEFT JOIN FavouriteFRA allfav ON allfav.fra_id = f.fra_id
                {where_sql}
                GROUP BY
                    f.fra_id, f.fra_title, c.frc_name, f.fra_start_date,
                    f.fra_end_date, f.fra_donation_goal, f.fra_views
                ORDER BY fav.fav_saved_at DESC
            """
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
    def get_fra_history(cls, user_id, search_query=""):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)

            params = [user_id]
            where_sql = "WHERE d.donation_user_id = %s"
            if search_query:
                where_sql += " AND (f.fra_title LIKE %s OR c.frc_name LIKE %s)"
                like_value = f"%{search_query}%"
                params.extend([like_value, like_value])

            query = f"""
                SELECT
                    d.donation_id,
                    d.donation_amt,
                    d.donation_date,
                    f.fra_id,
                    f.fra_title,
                    c.frc_name AS category_name
                FROM Donation d
                JOIN FRA f ON d.fra_id = f.fra_id
                JOIN FRC c ON f.fra_category = c.frc_id
                {where_sql}
                ORDER BY d.donation_date DESC
            """
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
