-- DROP DATABASE fundraising_db;
CREATE DATABASE IF NOT EXISTS fundraising_db;
USE fundraising_db;

/*
-- User
CREATE TABLE User (
    user_id            INT AUTO_INCREMENT PRIMARY KEY,
    user_name          VARCHAR(100) NOT NULL,
    user_email         VARCHAR(100) UNIQUE NOT NULL,
    user_password_hash VARCHAR(255) NOT NULL,
    user_status        ENUM('active', 'suspended') NOT NULL DEFAULT 'active',
    user_created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);
*/

-- UserProf
CREATE TABLE UserProf (
    profile_id     INT AUTO_INCREMENT PRIMARY KEY,
    profile_role   VARCHAR(100) UNIQUE NOT NULL,
    profile_status TINYINT(1) NOT NULL DEFAULT 1
);

-- UserAcct (Added UNIQUE to user_id to enforce 1-to-1)
CREATE TABLE UserAcct (
    account_id       INT AUTO_INCREMENT PRIMARY KEY,
    account_email    VARCHAR(100) UNIQUE NOT NULL,
    account_password VARCHAR(255) NOT NULL,
    account_name     VARCHAR(100),
    account_phone    VARCHAR(20), -- Kept as VARCHAR for safety, change to INT if strictly required
    account_address  VARCHAR(255),
    account_role     VARCHAR(100) NOT NULL,
    account_status   TINYINT(1) NOT NULL DEFAULT 1,
    FOREIGN KEY (account_role_id) REFERENCES UserProfdonation(profile_id)
);


-- FRC (Renamed to match ERD)
CREATE TABLE FRC (
    frc_id     INT AUTO_INCREMENT PRIMARY KEY,
    frc_name   VARCHAR(100) NOT NULL,
    frc_des    VARCHAR(255),
    frc_status TINYINT(1) DEFAULT 1
);

-- FRA (Renamed to match ERD, standardized PK to fra_id)
CREATE TABLE FRA (
    fra_id            INT AUTO_INCREMENT PRIMARY KEY, 
    fra_title         VARCHAR(100) NOT NULL,
    fra_des           TEXT,
    fra_donation_goal INT NOT NULL,
    fra_donation_amt  INT DEFAULT 0,
    fra_create_date   DATETIME DEFAULT CURRENT_TIMESTAMP,
    fra_start_date    DATETIME,
    fra_end_date      DATETIME,
    fra_views         INT DEFAULT 0,
    fra_num_of_fav    INT DEFAULT 0,
    fra_category      INT NOT NULL,
    fra_owner_id      INT NOT NULL,
    fra_status        ENUM('ongoing', 'completed', 'cancelled') NOT NULL DEFAULT 'ongoing',
    FOREIGN KEY (fra_category) REFERENCES FRC(frc_id),
    FOREIGN KEY (fra_owner_id) REFERENCES UserAcct(account_id)
);

-- Donation (Corrected FK to point to FRA)
CREATE TABLE Donation (
    donation_id      INT AUTO_INCREMENT PRIMARY KEY,
    fra_id           INT NOT NULL,
    donation_user_id INT NOT NULL,
    donation_amt     INT NOT NULL,
    donation_date    DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fra_id) REFERENCES FRA(fra_id),
    FOREIGN KEY (donation_user_id) REFERENCES UserAcct(account_id)
);

-- FavouriteFRA
CREATE TABLE FavouriteFRA (
    fav_id       INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT NOT NULL,
    fra_id       INT NOT NULL,
    fav_saved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_fav (user_id, fra_id),
    FOREIGN KEY (user_id) REFERENCES UserAcct(account_id),
    FOREIGN KEY (fra_id) REFERENCES FRA(fra_id)
);