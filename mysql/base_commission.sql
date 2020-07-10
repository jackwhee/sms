-- MySQL dump 10.13  Distrib 8.0.16, for Win64 (x86_64)
--
-- Host: localhost    Database: sms_02
-- ------------------------------------------------------
-- Server version	8.0.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `base_commission`
--

DROP TABLE IF EXISTS `base_commission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `base_commission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `month` varchar(2) NOT NULL,
  `application_fee` int(11) NOT NULL,
  `month_target` int(11) NOT NULL,
  `month_complete` int(11) NOT NULL,
  `month_unfinished` int(11) NOT NULL,
  `quarter_target` int(11) NOT NULL,
  `quarter_complete` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `base_commission`
--

LOCK TABLES `base_commission` WRITE;
/*!40000 ALTER TABLE `base_commission` DISABLE KEYS */;
INSERT INTO `base_commission` VALUES (1,'1',50,20,250,150,20,500),(2,'2',50,20,250,150,20,500),(3,'3',50,20,250,150,20,500),(4,'4',50,20,250,150,20,500),(5,'5',0,0,0,0,0,0),(6,'6',0,0,0,0,0,0),(7,'7',50,3,250,150,3,500),(8,'8',50,3,250,150,3,500),(9,'9',50,3,250,150,3,500),(10,'10',50,10,250,150,10,500),(11,'11',50,10,250,150,10,500),(12,'12',50,10,250,150,10,500);
/*!40000 ALTER TABLE `base_commission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-09-18 10:09:18
