CREATE DATABASE IF NOT EXISTS education_management_test;

USE education_management_test;

DROP TABLE IF EXISTS course_profile;

CREATE TABLE course_profile (
	course_id INT NOT NULL AUTO_INCREMENT,  -- for some reason adding NOT NULL removes an error
	course_name VARCHAR(50) NOT NULL UNIQUE,
	course_code VARCHAR(10) NOT NULL UNIQUE,
	course_desc TEXT,
	target_audience TINYINT DEFAULT 1 CHECK (target_audience BETWEEN 1 AND 3),
	duration_in_weeks TINYINT,
	credit_hours FLOAT,
	profile_status TINYINT NOT NULL DEFAULT 0 CHECK (profile_status IN (0, 1)),
	PRIMARY KEY (course_id)
);

DROP TABLE IF EXISTS student_profile;

CREATE TABLE student_profile (
	student_id VARCHAR(10) NOT NULL UNIQUE,
	first_name VARCHAR(30) NOT NULL,
	middle_name VARCHAR(30),
	last_name VARCHAR(30) NOT NULL,
	birth_date DATE,
	phone_number VARCHAR(15),
	email_address VARCHAR(120) NOT NULL UNIQUE,
	home_address VARCHAR(255),
	registration_date DATE,
	enrollment_status TINYINT NOT NULL DEFAULT 0 CHECK (enrollment_status BETWEEN 0 AND 2),
	guardian_status TINYINT(1) NOT NULL DEFAULT 0 CHECK (guardian_status IN (0, 1)),
	profile_status TINYINT NOT NULL DEFAULT 0 CHECK (profile_status IN (0, 1)),
	PRIMARY KEY (student_id)
);
