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
    def get_all_fras(cls):
        conn = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Join FRA and FRC so we get the actual Category Name
            query = """
                SELECT f.fra_id, f.fra_title, c.frc_name AS category_name, 
                       f.fra_start_date, f.fra_end_date, f.fra_donation_goal, 
                       f.fra_views, f.fra_num_of_fav
                FROM FRA f
                JOIN FRC c ON f.fra_category = c.frc_id
            """
            cursor.execute(query)
            return cursor.fetchall()
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return []
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()