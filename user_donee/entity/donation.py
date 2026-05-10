import mysql.connector
from user_donee.entity.fra import FRA


class Donation:
    @staticmethod
    def get_connection():
        return FRA.get_connection()

    @classmethod
    def get_donation_history(cls, user_id):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT d.donation_id, d.fra_id, d.donation_amt, d.donation_date,
                       f.fra_title, c.frc_name AS category_name
                FROM Donation d
                JOIN FRA f ON d.fra_id = f.fra_id
                JOIN FRC c ON f.fra_category = c.frc_id
                WHERE d.donation_user_id = %s
                ORDER BY d.donation_date DESC
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
    def searchDon(cls, user_id, keyword):
        print("Executing Donation.searchDon()")
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            search_text = f"%{keyword}%"
            query = """
                SELECT d.donation_id, d.fra_id, d.donation_amt, d.donation_date,
                       f.fra_title, c.frc_name AS category_name
                FROM Donation d
                JOIN FRA f ON d.fra_id = f.fra_id
                JOIN FRC c ON f.fra_category = c.frc_id
                WHERE d.donation_user_id = %s
                  AND (f.fra_title LIKE %s OR c.frc_name LIKE %s)
                ORDER BY d.donation_date DESC
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

    @classmethod
    def viewDon(cls, user_id, donation_id):
        print("Executing Donation.viewDon()")
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT d.donation_id, d.fra_id, d.donation_amt, d.donation_date,
                       f.fra_title, f.fra_des, f.fra_donation_goal,
                       c.frc_name AS category_name
                FROM Donation d
                JOIN FRA f ON d.fra_id = f.fra_id
                JOIN FRC c ON f.fra_category = c.frc_id
                WHERE d.donation_user_id = %s AND d.donation_id = %s
            """
            cursor.execute(query, (user_id, donation_id))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
