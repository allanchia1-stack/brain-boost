import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

config = {
    'user':     'root',
    'password': '',
    'host':     'localhost',
    'port':     3307,
    'database': 'fundraising_db'
}

fake = Faker()

def random_datetime(start_days_ago=365, end_days_ago=0):
    """Return a random datetime between start_days_ago and end_days_ago from now."""
    start = datetime.now() - timedelta(days=start_days_ago)
    end   = datetime.now() - timedelta(days=end_days_ago)
    return start + (end - start) * random.random()

def populate_data():
    try:
        conn   = mysql.connector.connect(**config)
        cursor = conn.cursor()
        print("Connected to database...")

        # FRC (FundRaisingCategory)
        categories = [
            ('Education',       'Support for Education initiatives'),
            ('Medical',         'Support for Medical initiatives'),
            ('Environment',     'Support for Environment initiatives'),
            ('Disaster Relief', 'Support for Disaster Relief initiatives'),
            ('Community',       'Support for Community initiatives'),
            ('Animals',         'Support for Animal welfare initiatives'),
            ('Arts & Culture',  'Support for Arts and Culture initiatives'),
            ('Sports',          'Support for Sports initiatives'),
        ]
        for name, des in categories:
            cursor.execute(
                "INSERT INTO FRC (frc_name, frc_des, frc_status) "
                "VALUES (%s, %s, %s)",
                (name, des, 1)
            )
        conn.commit()

        cursor.execute("SELECT frc_id FROM FRC")
        category_ids = [row[0] for row in cursor.fetchall()]
        print(f"  [1/5] Inserted {len(category_ids)} categories.")

        # Users (User + UserAcct + UserProf) 100 tuples of data
        role_list = (
            ['Admin']      * 2  +
            ['Manager']    * 2  +
            ['FundRaiser'] * 16 +
            ['Donee']      * 80
        )
        random.shuffle(role_list)

        all_user_ids   = []
        fundraiser_ids = []
        donee_ids      = []

        for role in role_list:
            # Generate the core identity ONCE per iteration
            current_name = fake.name()
            current_email = fake.unique.email()
            
            # User Table
            cursor.execute(
                "INSERT INTO User "
                "(user_name, user_email, user_password_hash, user_status) "
                "VALUES (%s, %s, %s, %s)",
                (
                    current_name,
                    current_email,
                    "hashed_pass_placeholder",
                    random.choices(['active', 'suspended'], weights=[90, 10])[0]
                )
            )
            uid = cursor.lastrowid
            all_user_ids.append(uid)

            # UserAcct Table
            cursor.execute(
                "INSERT INTO UserAcct "
                "(user_id, account_password, account_email, account_status) "
                "VALUES (%s, %s, %s, %s)",
                (
                    uid,
                    "hashed_pass_placeholder",
                    current_email,
                    1
                )
            )

            # UserProf Table
            cursor.execute(
                "INSERT INTO UserProf "
                "(user_id, profile_name, phone, address, profile_role, profile_status) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    uid,
                    current_name,
                    fake.numerify('9#######'),
                    fake.address().replace('\n', ', '),
                    role,
                    1
                )
            )

            if role == 'FundRaiser':
                fundraiser_ids.append(uid)
            elif role == 'Donee':
                donee_ids.append(uid)

        conn.commit()
        print(f"  [2/5] Inserted 100 users with unified identities.")

        # FRA & Donations (Combined Logic)
        activity_ids = []
        total_donations_created = 0
        
        for _ in range(100):
            start_date = random_datetime(start_days_ago=400, end_days_ago=30)
            end_date   = start_date + timedelta(days=random.randint(30, 180))
            status     = random.choices(['ongoing', 'completed', 'cancelled'], weights=[60, 30, 10])[0]
            goal       = random.randint(1000, 50000)
            
            # Insert the FRA with 0 raised initially
            cursor.execute(
                "INSERT INTO FRA "
                "(fra_title, fra_des, fra_donation_goal, fra_donation_amt, "
                " fra_start_date, fra_end_date, fra_views, fra_num_of_fav, "
                " fra_category, fra_owner_id, fra_status) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    fake.catch_phrase(),
                    fake.text(max_nb_chars=200),
                    goal,
                    0, 
                    start_date,
                    end_date,
                    random.randint(0, 5000),
                    random.randint(0, 500),
                    random.choice(category_ids),
                    random.choice(fundraiser_ids),
                    status,
                )
            )
            current_fra_id = cursor.lastrowid
            activity_ids.append(current_fra_id)

            # Generate random donations specifically for THIS activity
            total_raised_for_this_fra = 0
            if status != 'cancelled':
                num_donations = random.randint(1, 4) 
                for _ in range(num_donations):
                    donation_amt = random.randint(10, 500)
                    total_raised_for_this_fra += donation_amt
                    total_donations_created += 1
                    
                    # Ensure donation date falls within the activity timeframe
                    donation_date = start_date + (end_date - start_date) * random.random()
                    
                    cursor.execute(
                        "INSERT INTO Donation "
                        "(fra_id, donation_user_id, donation_amt, donation_date) "
                        "VALUES (%s, %s, %s, %s)",
                        (
                            current_fra_id,
                            random.choice(donee_ids),
                            donation_amt,
                            donation_date
                        )
                    )
            
            # Update the FRA table with the exact sum of its actual donations
            cursor.execute(
                "UPDATE FRA SET fra_donation_amt = %s WHERE fra_id = %s",
                (total_raised_for_this_fra, current_fra_id)
            )

        conn.commit()
        print(f"  [3/5 & 4/5] Inserted 100 activities and {total_donations_created} perfectly matched donations.")

        # FavouriteFRA
        fav_pairs = set()
        attempts  = 0
        while len(fav_pairs) < 100 and attempts < 1000:
            attempts += 1
            pair = (random.choice(donee_ids), random.choice(activity_ids))
            if pair not in fav_pairs:
                fav_pairs.add(pair)
                cursor.execute(
                    "INSERT INTO FavouriteFRA (user_id, fra_id, fav_saved_at) "
                    "VALUES (%s, %s, %s)",
                    (pair[0], pair[1], random_datetime())
                )
        conn.commit()
        print(f"  [5/5] Inserted {len(fav_pairs)} favourite FRA records.")

        print("\nDatabase populated successfully! All data integrity checks passed.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if 'conn' in locals() and conn.is_connected():
            conn.rollback()
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Connection closed.")

if __name__ == "__main__":
    populate_data()