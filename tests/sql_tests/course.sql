USE education_management;

DROP TABLE IF EXISTS course_profile;

CREATE TABLE course_profile (
	course_id INT NOT NULL AUTO_INCREMENT,  -- for some reason adding NOT NULL removes an error
	course_name VARCHAR(50) NOT NULL UNIQUE,
	course_code VARCHAR(10) NOT NULL UNIQUE,
	course_desc TEXT,
	target_audience TINYINT DEFAULT 1 CHECK (target_audience IN (1, 2)),
	duration_in_weeks TINYINT,
	credit_hours FLOAT,
	profile_status TINYINT NOT NULL DEFAULT 0 CHECK (profile_status IN (0, 1)),
	PRIMARY KEY (course_id)
);

-- CREATE

INSERT INTO course_profile(course_name, course_code, course_desc,
target_audience, duration_in_weeks, credit_hours, profile_status)
VALUES ('Introduction to Computer Science', 'COMP 250',
'Searching/sorting algorithms, data structures', 2, 15, 3.0, 1);

INSERT INTO course_profile(course_name, course_code)
VALUES ('Theory of Computation', 'COMP 330');

INSERT INTO course_profile(course_name, course_code, course_desc)
VALUES ('Sampling Theory and Applications', 'MATH 525', 'Horvitz-Thompson estimator');

-- READ

SELECT * FROM course_profile; -- ALL courses

SELECT * FROM course_profile
WHERE profile_status = 0; -- list OF inactive courses

-- UPDATE

UPDATE course_profile
SET credit_hours = 4.0
WHERE course_code = 'MATH 525';

UPDATE course_profile
SET course_desc = 'Finite state machines, push-down automata, computability'
WHERE course_code = 'COMP 330';

SELECT * FROM course_profile;

-- DELETE

DELETE FROM course_profile
WHERE course_code = 'COMP 330';

SELECT * FROM course_profile;