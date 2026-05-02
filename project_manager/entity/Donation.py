import mysql.connector
from datetime import datetime, timedelta


class Donation:
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
    def _get_by_period(cls, start_dt, end_dt):
        conn = cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT d.donation_id, d.donation_amt, d.donation_date,
                       f.fra_title, c.frc_name AS category,
                       u.user_name AS donor_name
                FROM Donation d
                JOIN FRA   f ON d.fra_id          = f.fra_id
                JOIN FRC   c ON f.fra_category     = c.frc_id
                JOIN User  u ON d.donation_user_id = u.user_id
                WHERE d.donation_date >= %s AND d.donation_date <= %s
                ORDER BY d.donation_date DESC
                """,
                (start_dt, end_dt)
            )
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return []
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @classmethod
    def get_daily_summary(cls):
        today = datetime.now().date()
        rows  = cls._get_by_period(
            datetime.combine(today, datetime.min.time()),
            datetime.combine(today, datetime.max.time())
        )
        return {
            'period':           today.strftime('%d %B %Y'),
            'donations':        rows,
            'total_donations':  len(rows),
            'total_amount':     sum(r['donation_amt'] for r in rows),
        }

    @classmethod
    def get_weekly_summary(cls):
        today         = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week   = start_of_week + timedelta(days=6)
        rows = cls._get_by_period(
            datetime.combine(start_of_week, datetime.min.time()),
            datetime.combine(end_of_week,   datetime.max.time())
        )
        return {
            'period':           f"{start_of_week.strftime('%d %b %Y')} – {end_of_week.strftime('%d %b %Y')}",
            'donations':        rows,
            'total_donations':  len(rows),
            'total_amount':     sum(r['donation_amt'] for r in rows),
        }

    @classmethod
    def get_monthly_summary(cls):
        today           = datetime.now().date()
        start_of_month  = today.replace(day=1)
        if today.month == 12:
            end_of_month = today.replace(day=31)
        else:
            end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        rows = cls._get_by_period(
            datetime.combine(start_of_month, datetime.min.time()),
            datetime.combine(end_of_month,   datetime.max.time())
        )
        return {
            'period':           today.strftime('%B %Y'),
            'donations':        rows,
            'total_donations':  len(rows),
            'total_amount':     sum(r['donation_amt'] for r in rows),
        }
