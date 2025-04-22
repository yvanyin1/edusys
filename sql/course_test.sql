USE education_management;

-- Assuming that course_profile already exists

SELECT * FROM course_profile;

-- CREATE

INSERT INTO course_profile(course_name, course_code, course_desc,
target_audience, duration_in_weeks, credit_hours, profile_status)
VALUES ('Introduction to Software Systems', 'COMP 206',
'Programming in C, Unix, Bash, makefile, version control systems', 2, 15, 3.0, 1);

-- READ

SELECT * FROM course_profile; -- ALL courses

SELECT * FROM course_profile
WHERE profile_status = 0; -- list OF inactive courses

-- UPDATE

UPDATE course_profile
SET course_desc = 'Programming in C, Unix, Bash, makefile, Git, version control systems'
WHERE course_code = 'COMP 206';

SELECT * FROM course_profile;

-- DELETE

DELETE FROM course_profile
WHERE course_code = 'COMP 206';

SELECT * FROM course_profile;