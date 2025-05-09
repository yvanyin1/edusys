-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: education_management_test
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `class_schedule`
--

DROP TABLE IF EXISTS `class_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_schedule` (
  `schedule_id` int NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `semester_id` int NOT NULL,
  `class_capacity` int NOT NULL,
  `class_type` tinyint NOT NULL DEFAULT '1',
  `class_desc` text NOT NULL,
  PRIMARY KEY (`schedule_id`),
  KEY `course_id` (`course_id`),
  KEY `semester_id` (`semester_id`),
  CONSTRAINT `class_schedule_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course_profile` (`course_id`),
  CONSTRAINT `class_schedule_ibfk_2` FOREIGN KEY (`semester_id`) REFERENCES `semester` (`semester_id`),
  CONSTRAINT `class_schedule_chk_1` CHECK ((`class_type` between 1 and 5))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_schedule`
--

LOCK TABLES `class_schedule` WRITE;
/*!40000 ALTER TABLE `class_schedule` DISABLE KEYS */;
INSERT INTO `class_schedule` VALUES (1,1,2,100,2,'Computer science in a breeze'),(2,2,2,1,3,'DFA for one person'),(3,3,3,30,1,'Statistics in a medium-sized class');
/*!40000 ALTER TABLE `class_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classroom_location`
--

DROP TABLE IF EXISTS `classroom_location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classroom_location` (
  `location_id` int NOT NULL AUTO_INCREMENT,
  `room_number` varchar(10) NOT NULL,
  `building_name` varchar(100) NOT NULL,
  `capacity` int NOT NULL,
  PRIMARY KEY (`location_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classroom_location`
--

LOCK TABLES `classroom_location` WRITE;
/*!40000 ALTER TABLE `classroom_location` DISABLE KEYS */;
INSERT INTO `classroom_location` VALUES (1,'132','Leacock',600),(2,'112','Rutherford Physics',150),(3,'0132','Trottier',50);
/*!40000 ALTER TABLE `classroom_location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_profile`
--

DROP TABLE IF EXISTS `course_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course_profile` (
  `course_id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(50) NOT NULL,
  `course_code` varchar(10) NOT NULL,
  `course_desc` text,
  `target_audience` tinyint DEFAULT '1',
  `duration_in_weeks` tinyint DEFAULT NULL,
  `credit_hours` float DEFAULT NULL,
  `profile_status` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`course_id`),
  UNIQUE KEY `course_name` (`course_name`),
  UNIQUE KEY `course_code` (`course_code`),
  CONSTRAINT `course_profile_chk_1` CHECK ((`target_audience` between 1 and 3)),
  CONSTRAINT `course_profile_chk_2` CHECK ((`profile_status` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_profile`
--

LOCK TABLES `course_profile` WRITE;
/*!40000 ALTER TABLE `course_profile` DISABLE KEYS */;
INSERT INTO `course_profile` VALUES (1,'Introduction to Computer Science','COMP 250','Searching/sorting algorithms, data structures',2,15,3,1),(2,'Theory of Computation','COMP 330',NULL,2,12,3,1),(3,'Sampling Theory and Applications','MATH 525','Horvitz-Thompson estimator',1,10,3,1);
/*!40000 ALTER TABLE `course_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scheduled_class_session`
--

DROP TABLE IF EXISTS `scheduled_class_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scheduled_class_session` (
  `session_id` int NOT NULL AUTO_INCREMENT,
  `schedule_id` int NOT NULL,
  `location_id` int NOT NULL,
  `day_of_week` tinyint NOT NULL DEFAULT '1',
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `session_type` tinyint NOT NULL DEFAULT '1',
  `scheduled_date` date NOT NULL,
  `seq_no` tinyint NOT NULL,
  `session_change_type` tinyint DEFAULT NULL,
  `flag` tinyint NOT NULL DEFAULT '1',
  PRIMARY KEY (`session_id`),
  KEY `schedule_id` (`schedule_id`),
  KEY `location_id` (`location_id`),
  CONSTRAINT `scheduled_class_session_ibfk_1` FOREIGN KEY (`schedule_id`) REFERENCES `class_schedule` (`schedule_id`),
  CONSTRAINT `scheduled_class_session_ibfk_2` FOREIGN KEY (`location_id`) REFERENCES `classroom_location` (`location_id`),
  CONSTRAINT `scheduled_class_session_chk_1` CHECK ((`day_of_week` between 1 and 7)),
  CONSTRAINT `scheduled_class_session_chk_2` CHECK ((`session_type` between 1 and 4)),
  CONSTRAINT `scheduled_class_session_chk_3` CHECK (((`session_change_type` is null) or (`session_change_type` between 0 and 3))),
  CONSTRAINT `scheduled_class_session_chk_4` CHECK ((`flag` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduled_class_session`
--

LOCK TABLES `scheduled_class_session` WRITE;
/*!40000 ALTER TABLE `scheduled_class_session` DISABLE KEYS */;
INSERT INTO `scheduled_class_session` VALUES (1,1,1,2,'14:30:00','16:00:00',1,'2025-05-06',1,NULL,1),(2,1,1,4,'14:30:00','16:00:00',1,'2025-05-08',2,NULL,1),(3,1,1,2,'14:30:00','16:00:00',1,'2025-05-13',3,NULL,1),(4,1,1,4,'14:30:00','16:00:00',1,'2025-05-15',4,NULL,1),(5,1,1,2,'14:30:00','16:00:00',1,'2025-05-20',5,NULL,1),(6,1,1,4,'14:30:00','16:00:00',1,'2025-05-22',6,NULL,1),(7,1,1,2,'14:30:00','16:00:00',1,'2025-05-27',7,NULL,1),(8,1,1,4,'14:30:00','16:00:00',1,'2025-05-29',8,NULL,1),(9,1,1,2,'14:30:00','16:00:00',1,'2025-06-03',9,NULL,1),(10,1,1,4,'14:30:00','16:00:00',1,'2025-06-05',10,NULL,1),(11,1,1,2,'14:30:00','16:00:00',1,'2025-06-10',11,NULL,1),(12,1,1,4,'14:30:00','16:00:00',1,'2025-06-12',12,NULL,1),(13,1,1,2,'14:30:00','16:00:00',1,'2025-06-17',13,NULL,1),(14,1,1,4,'14:30:00','16:00:00',1,'2025-06-19',14,NULL,1),(15,1,1,2,'14:30:00','16:00:00',1,'2025-06-24',15,NULL,1),(16,1,1,4,'14:30:00','16:00:00',1,'2025-06-26',16,NULL,1),(17,1,1,2,'14:30:00','16:00:00',1,'2025-07-01',17,NULL,1),(18,1,1,4,'14:30:00','16:00:00',1,'2025-07-03',18,NULL,1),(19,1,1,2,'14:30:00','16:00:00',1,'2025-07-08',19,NULL,1),(20,1,1,4,'14:30:00','16:00:00',1,'2025-07-10',20,NULL,1),(21,1,1,2,'14:30:00','16:00:00',1,'2025-07-15',21,NULL,1),(22,1,1,4,'14:30:00','16:00:00',1,'2025-07-17',22,NULL,1),(23,1,1,2,'14:30:00','16:00:00',1,'2025-07-22',23,NULL,1),(24,1,1,4,'14:30:00','16:00:00',1,'2025-07-24',24,NULL,1),(25,1,1,2,'14:30:00','16:00:00',1,'2025-07-29',25,NULL,1),(26,1,1,4,'14:30:00','16:00:00',1,'2025-07-31',26,NULL,1),(27,1,1,2,'14:30:00','16:00:00',1,'2025-08-05',27,NULL,1),(28,1,1,4,'14:30:00','16:00:00',1,'2025-08-07',28,NULL,1),(29,1,1,2,'14:30:00','16:00:00',1,'2025-08-12',29,NULL,1),(30,1,1,4,'14:30:00','16:00:00',1,'2025-08-14',30,NULL,1),(31,1,1,2,'14:30:00','16:00:00',1,'2025-08-19',31,NULL,1),(32,1,1,4,'14:30:00','16:00:00',1,'2025-08-21',32,NULL,1),(33,2,3,1,'10:00:00','11:00:00',1,'2025-05-05',1,NULL,1),(34,2,3,3,'10:00:00','11:00:00',1,'2025-05-07',2,NULL,1),(35,2,3,5,'10:00:00','11:00:00',1,'2025-05-09',3,NULL,1),(36,2,3,1,'10:00:00','11:00:00',1,'2025-05-12',4,NULL,1),(37,2,3,3,'10:00:00','11:00:00',1,'2025-05-14',5,NULL,1),(38,2,3,5,'10:00:00','11:00:00',1,'2025-05-16',6,NULL,1),(39,2,3,1,'10:00:00','11:00:00',1,'2025-05-19',7,NULL,1),(40,2,3,3,'10:00:00','11:00:00',1,'2025-05-21',8,NULL,1),(41,2,3,5,'10:00:00','11:00:00',1,'2025-05-23',9,NULL,1),(42,2,3,1,'10:00:00','11:00:00',1,'2025-05-26',10,NULL,1),(43,2,3,3,'10:00:00','11:00:00',1,'2025-05-28',11,NULL,1),(44,2,3,5,'10:00:00','11:00:00',1,'2025-05-30',12,NULL,1),(45,2,3,1,'10:00:00','11:00:00',1,'2025-06-02',13,NULL,1),(46,2,3,3,'10:00:00','11:00:00',1,'2025-06-04',14,NULL,1),(47,2,3,5,'10:00:00','11:00:00',1,'2025-06-06',15,NULL,1),(48,2,3,1,'10:00:00','11:00:00',1,'2025-06-09',16,NULL,1),(49,2,3,3,'10:00:00','11:00:00',1,'2025-06-11',17,NULL,1),(50,2,3,5,'10:00:00','11:00:00',1,'2025-06-13',18,NULL,1),(51,2,3,1,'10:00:00','11:00:00',1,'2025-06-16',19,NULL,1),(52,2,3,3,'10:00:00','11:00:00',1,'2025-06-18',20,NULL,1),(53,2,3,5,'10:00:00','11:00:00',1,'2025-06-20',21,NULL,1),(54,2,3,1,'10:00:00','11:00:00',1,'2025-06-23',22,NULL,1),(55,2,3,3,'10:00:00','11:00:00',1,'2025-06-25',23,NULL,1),(56,2,3,5,'10:00:00','11:00:00',1,'2025-06-27',24,NULL,1),(57,2,3,1,'10:00:00','11:00:00',1,'2025-06-30',25,NULL,1),(58,2,3,3,'10:00:00','11:00:00',1,'2025-07-02',26,NULL,1),(59,2,3,5,'10:00:00','11:00:00',1,'2025-07-04',27,NULL,1),(60,2,3,1,'10:00:00','11:00:00',1,'2025-07-07',28,NULL,1),(61,2,3,3,'10:00:00','11:00:00',1,'2025-07-09',29,NULL,1),(62,2,3,5,'10:00:00','11:00:00',1,'2025-07-11',30,NULL,1),(63,2,3,1,'10:00:00','11:00:00',1,'2025-07-14',31,NULL,1),(64,2,3,3,'10:00:00','11:00:00',1,'2025-07-16',32,NULL,1),(65,2,3,5,'10:00:00','11:00:00',1,'2025-07-18',33,NULL,1),(66,2,3,1,'10:00:00','11:00:00',1,'2025-07-21',34,NULL,1),(67,2,3,3,'10:00:00','11:00:00',1,'2025-07-23',35,NULL,1),(68,2,3,5,'10:00:00','11:00:00',1,'2025-07-25',36,NULL,1),(69,2,3,1,'10:00:00','11:00:00',1,'2025-07-28',37,NULL,1),(70,2,3,3,'10:00:00','11:00:00',1,'2025-07-30',38,NULL,1),(71,2,3,5,'10:00:00','11:00:00',1,'2025-08-01',39,NULL,1),(72,2,3,1,'10:00:00','11:00:00',1,'2025-08-04',40,NULL,1),(73,2,3,3,'10:00:00','11:00:00',1,'2025-08-06',41,NULL,1),(74,2,3,5,'10:00:00','11:00:00',1,'2025-08-08',42,NULL,1),(75,2,3,1,'10:00:00','11:00:00',1,'2025-08-11',43,NULL,1),(76,2,3,3,'10:00:00','11:00:00',1,'2025-08-13',44,NULL,1),(77,2,3,5,'10:00:00','11:00:00',1,'2025-08-15',45,NULL,1),(78,2,3,1,'10:00:00','11:00:00',1,'2025-08-18',46,NULL,1),(79,2,3,3,'10:00:00','11:00:00',1,'2025-08-20',47,NULL,1),(80,2,3,5,'10:00:00','11:00:00',1,'2025-08-22',48,NULL,1),(81,3,2,3,'12:00:00','13:30:00',1,'2025-05-07',1,NULL,1),(82,3,2,5,'12:00:00','13:30:00',1,'2025-05-09',2,NULL,1),(83,3,2,3,'12:00:00','13:30:00',1,'2025-05-14',3,NULL,1),(84,3,2,5,'12:00:00','13:30:00',1,'2025-05-16',4,NULL,1),(85,3,2,3,'12:00:00','13:30:00',1,'2025-05-21',5,NULL,1),(86,3,2,5,'12:00:00','13:30:00',1,'2025-05-23',6,NULL,1),(87,3,2,3,'12:00:00','13:30:00',1,'2025-05-28',7,NULL,1),(88,3,2,5,'12:00:00','13:30:00',1,'2025-05-30',8,NULL,1),(89,3,2,3,'12:00:00','13:30:00',1,'2025-06-04',9,NULL,1),(90,3,2,5,'12:00:00','13:30:00',1,'2025-06-06',10,NULL,1),(91,3,2,3,'12:00:00','13:30:00',1,'2025-06-11',11,NULL,1),(92,3,2,5,'12:00:00','13:30:00',1,'2025-06-13',12,NULL,1),(93,3,2,3,'12:00:00','13:30:00',1,'2025-06-18',13,NULL,1),(94,3,2,5,'12:00:00','13:30:00',1,'2025-06-20',14,NULL,1),(95,3,2,3,'12:00:00','13:30:00',1,'2025-06-25',15,NULL,1),(96,3,2,5,'12:00:00','13:30:00',1,'2025-06-27',16,NULL,1),(97,3,2,3,'12:00:00','13:30:00',1,'2025-07-02',17,NULL,1),(98,3,2,5,'12:00:00','13:30:00',1,'2025-07-04',18,NULL,1),(99,3,2,3,'12:00:00','13:30:00',1,'2025-07-09',19,NULL,1),(100,3,2,5,'12:00:00','13:30:00',1,'2025-07-11',20,NULL,1),(101,3,2,3,'12:00:00','13:30:00',1,'2025-07-16',21,NULL,1),(102,3,2,5,'12:00:00','13:30:00',1,'2025-07-18',22,NULL,1),(103,3,2,3,'12:00:00','13:30:00',1,'2025-07-23',23,NULL,1),(104,3,2,5,'12:00:00','13:30:00',1,'2025-07-25',24,NULL,1),(105,3,2,3,'12:00:00','13:30:00',1,'2025-07-30',25,NULL,1),(106,3,2,5,'12:00:00','13:30:00',1,'2025-08-01',26,NULL,1),(107,3,2,3,'12:00:00','13:30:00',1,'2025-08-06',27,NULL,1),(108,3,2,5,'12:00:00','13:30:00',1,'2025-08-08',28,NULL,1),(109,3,2,3,'12:00:00','13:30:00',1,'2025-08-13',29,NULL,1),(110,3,2,5,'12:00:00','13:30:00',1,'2025-08-15',30,NULL,1),(111,3,2,3,'12:00:00','13:30:00',1,'2025-08-20',31,NULL,1),(112,3,2,5,'12:00:00','13:30:00',1,'2025-08-22',32,NULL,1);
/*!40000 ALTER TABLE `scheduled_class_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `semester`
--

DROP TABLE IF EXISTS `semester`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `semester` (
  `semester_id` int NOT NULL AUTO_INCREMENT,
  `season` tinyint NOT NULL DEFAULT '1',
  `academic_year` int NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `registration_deadline` datetime NOT NULL,
  `withdrawal_deadline` datetime NOT NULL,
  PRIMARY KEY (`semester_id`),
  CONSTRAINT `semester_chk_1` CHECK ((`season` between 1 and 3))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `semester`
--

LOCK TABLES `semester` WRITE;
/*!40000 ALTER TABLE `semester` DISABLE KEYS */;
INSERT INTO `semester` VALUES (1,3,2025,'2025-05-05','2025-08-22','2025-05-03 23:59:59','2025-06-15 23:59:59'),(2,1,2025,'2025-09-08','2025-12-19','2025-09-06 23:59:59','2025-10-15 23:59:59'),(3,2,2026,'2025-01-05','2025-04-24','2025-01-03 23:59:59','2025-02-15 23:59:59');
/*!40000 ALTER TABLE `semester` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_enrollment_details`
--

DROP TABLE IF EXISTS `student_enrollment_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_enrollment_details` (
  `enrollment_id` int NOT NULL AUTO_INCREMENT,
  `student_id` varchar(10) NOT NULL,
  `class_schedule_id` int NOT NULL,
  `enrollment_date` date NOT NULL,
  `enrollment_status` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`enrollment_id`),
  KEY `student_id` (`student_id`),
  KEY `class_schedule_id` (`class_schedule_id`),
  CONSTRAINT `student_enrollment_details_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student_profile` (`student_id`),
  CONSTRAINT `student_enrollment_details_ibfk_2` FOREIGN KEY (`class_schedule_id`) REFERENCES `class_schedule` (`schedule_id`),
  CONSTRAINT `student_enrollment_details_chk_1` CHECK ((`enrollment_status` between 0 and 3))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_enrollment_details`
--

LOCK TABLES `student_enrollment_details` WRITE;
/*!40000 ALTER TABLE `student_enrollment_details` DISABLE KEYS */;
INSERT INTO `student_enrollment_details` VALUES (1,'2025050001',1,'2025-05-03',1),(2,'2025050001',2,'2025-05-03',1),(3,'2025050001',3,'2025-05-03',1);
/*!40000 ALTER TABLE `student_enrollment_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_profile`
--

DROP TABLE IF EXISTS `student_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_profile` (
  `student_id` varchar(10) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `middle_name` varchar(30) DEFAULT NULL,
  `last_name` varchar(30) NOT NULL,
  `birth_date` date DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `email_address` varchar(120) NOT NULL,
  `home_address` varchar(255) DEFAULT NULL,
  `registration_date` date DEFAULT NULL,
  `enrollment_status` tinyint NOT NULL DEFAULT '0',
  `guardian_status` tinyint(1) NOT NULL DEFAULT '0',
  `profile_status` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `student_id` (`student_id`),
  UNIQUE KEY `email_address` (`email_address`),
  CONSTRAINT `student_profile_chk_1` CHECK ((`enrollment_status` between 0 and 2)),
  CONSTRAINT `student_profile_chk_2` CHECK ((`guardian_status` in (0,1))),
  CONSTRAINT `student_profile_chk_3` CHECK ((`profile_status` in (0,1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_profile`
--

LOCK TABLES `student_profile` WRITE;
/*!40000 ALTER TABLE `student_profile` DISABLE KEYS */;
INSERT INTO `student_profile` VALUES ('2025050001','Daniel','Ziyang','Luo','1998-12-10','5141234567','daniel.luo@mail.mcgill.ca','123 rue Street','2025-03-27',1,0,1),('2025050002','Brian','Harold','May','1947-07-19','4381234567','brianmay@gmail.com','1975 rue Queen','2024-10-31',0,0,0),('2025050003','Farrokh','','Bulsara','1946-09-05','4501234567','freddiemercury@gmail.com','1975 rue Bohemian','2024-01-31',1,1,1);
/*!40000 ALTER TABLE `student_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher_profile`
--

DROP TABLE IF EXISTS `teacher_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacher_profile` (
  `teacher_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(30) NOT NULL,
  `middle_name` varchar(30) DEFAULT NULL,
  `last_name` varchar(30) NOT NULL,
  `birth_date` date DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `email_address` varchar(120) NOT NULL,
  `home_address` varchar(255) DEFAULT NULL,
  `subject_expertise` varchar(100) NOT NULL,
  `employment_status` tinyint NOT NULL DEFAULT '0',
  `teacher_role` tinyint NOT NULL DEFAULT '1',
  `profile_status` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`teacher_id`),
  UNIQUE KEY `email_address` (`email_address`),
  CONSTRAINT `teacher_profile_chk_1` CHECK ((`employment_status` between 0 and 3)),
  CONSTRAINT `teacher_profile_chk_2` CHECK ((`teacher_role` in (1,2))),
  CONSTRAINT `teacher_profile_chk_3` CHECK ((`profile_status` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher_profile`
--

LOCK TABLES `teacher_profile` WRITE;
/*!40000 ALTER TABLE `teacher_profile` DISABLE KEYS */;
INSERT INTO `teacher_profile` VALUES (1,'Albert','','Einstein','1879-03-14','5143141879','emc2@gmail.com','123 Relativity Street','Physics, Science',1,1,1),(2,'Alan','Mathison','Turing','1912-06-23','5146231912','turing@gmail.com','468 Fox Street','Computer Science',3,1,0),(3,'Harald','','Cramer','1893-09-25','5149251893','haraldcramer@gmail.com','100 Gothenburg Street','Statistics',2,2,1);
/*!40000 ALTER TABLE `teacher_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'education_management_test'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-09 10:21:38
