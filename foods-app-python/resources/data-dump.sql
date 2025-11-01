-- MySQL dump 10.13  Distrib 8.3.0, for macos14.2 (arm64)
--
-- Host: localhost    Database: final_schema
-- ------------------------------------------------------
-- Server version	8.0.36

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
-- Table structure for table `GroceryList`
--

DROP TABLE IF EXISTS `GroceryList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `GroceryList` (
  `GroceryListID` int NOT NULL AUTO_INCREMENT,
  `RecipeIngredientID` int DEFAULT NULL,
  `store` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`GroceryListID`),
  KEY `RecipeIngredientID` (`RecipeIngredientID`),
  CONSTRAINT `grocerylist_ibfk_1` FOREIGN KEY (`RecipeIngredientID`) REFERENCES `RecipeIngredient` (`RecipeIngredientID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `GroceryList`
--

LOCK TABLES `GroceryList` WRITE;
/*!40000 ALTER TABLE `GroceryList` DISABLE KEYS */;
/*!40000 ALTER TABLE `GroceryList` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Ingredient`
--

DROP TABLE IF EXISTS `Ingredient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Ingredient` (
  `IngredientID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `cal` int DEFAULT NULL,
  `protein` int DEFAULT NULL,
  `fat` int DEFAULT NULL,
  `carb` int DEFAULT NULL,
  PRIMARY KEY (`IngredientID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ingredient`
--

LOCK TABLES `Ingredient` WRITE;
/*!40000 ALTER TABLE `Ingredient` DISABLE KEYS */;
INSERT INTO `Ingredient` VALUES (1,'Chicken','Meat',128,26,3,0),(2,'lettuce','Vegatable',14,1,0,3),(3,'tomato','Vegatable',16,1,0,4),(4,'Bun','Bread',256,9,4,48),(5,'Ground Beef','Meat',154,24,6,0),(6,'Cheddar Cheese','Cheese',115,7,9,0),(7,'Caesar dressing','dressing',77,0,9,1),(8,'salt','seasoning',0,0,0,0);
/*!40000 ALTER TABLE `Ingredient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Inventory`
--

DROP TABLE IF EXISTS `Inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Inventory` (
  `InventoryID` int NOT NULL,
  `IngredientID` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`InventoryID`),
  KEY `Inventory_Ingredient_IngredientID_fk` (`IngredientID`),
  CONSTRAINT `inventory_ibfk_1` FOREIGN KEY (`IngredientID`) REFERENCES `Ingredient` (`IngredientID`),
  CONSTRAINT `inventory_ibfk_2` FOREIGN KEY (`IngredientID`) REFERENCES `Ingredient` (`IngredientID`),
  CONSTRAINT `inventory_ibfk_3` FOREIGN KEY (`IngredientID`) REFERENCES `Ingredient` (`IngredientID`),
  CONSTRAINT `Inventory_Ingredient_IngredientID_fk` FOREIGN KEY (`IngredientID`) REFERENCES `Ingredient` (`IngredientID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Inventory`
--

LOCK TABLES `Inventory` WRITE;
/*!40000 ALTER TABLE `Inventory` DISABLE KEYS */;
INSERT INTO `Inventory` VALUES (1,1,10,'fridge'),(2,2,0,'fridge'),(3,3,4,'pantry'),(4,4,1,'fridge'),(5,5,1,'freezer'),(6,6,2,'fridge'),(7,7,1,'fridge');
/*!40000 ALTER TABLE `Inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MealPlan`
--

DROP TABLE IF EXISTS `MealPlan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MealPlan` (
  `MealPlanID` int NOT NULL AUTO_INCREMENT,
  `MealDate` date DEFAULT NULL,
  `RecipeID` int DEFAULT NULL,
  PRIMARY KEY (`MealPlanID`),
  KEY `RecipeID` (`RecipeID`),
  CONSTRAINT `mealplan_ibfk_1` FOREIGN KEY (`RecipeID`) REFERENCES `Recipe` (`RecipeID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MealPlan`
--

LOCK TABLES `MealPlan` WRITE;
/*!40000 ALTER TABLE `MealPlan` DISABLE KEYS */;
INSERT INTO `MealPlan` VALUES (1,'2024-02-17',3);
/*!40000 ALTER TABLE `MealPlan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `mealplanview`
--

DROP TABLE IF EXISTS `mealplanview`;
/*!50001 DROP VIEW IF EXISTS `mealplanview`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `mealplanview` AS SELECT 
 1 AS `MealPlanID`,
 1 AS `MealDate`,
 1 AS `RecipeName`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `Recipe`
--

DROP TABLE IF EXISTS `Recipe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Recipe` (
  `RecipeID` int NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `instructions` varchar(1000) DEFAULT NULL,
  `cookTimeMin` int DEFAULT NULL,
  `servings` int DEFAULT NULL,
  `category` enum('Breakfast','Lunch','Dinner','Snack') DEFAULT NULL,
  PRIMARY KEY (`RecipeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Recipe`
--

LOCK TABLES `Recipe` WRITE;
/*!40000 ALTER TABLE `Recipe` DISABLE KEYS */;
INSERT INTO `Recipe` VALUES (1,'Chicken Caesar Burger','Season and cook the chicken breasts until fully cooked.\nToast the burger buns.\nAssemble the burgers by placing lettuce leaves, sliced tomatoes, and cooked chicken breasts on the bottom half of each bun.\nDrizzle Caesar dressing over the chicken.\nSprinkle shredded cheddar cheese on top.\nPlace the top half of the bun over the filling.',20,4,'Dinner'),(2,'Beef and Cheddar Stuffed Lettuce Wraps','1. Cook ground beef in a skillet over medium heat until browned. Season with salt, pepper, and other desired seasonings. 2. Rinse and dry lettuce leaves, then lay them out flat. 3. Place a spoonful of cooked ground beef onto each lettuce leaf. 4. Top the beef with diced tomatoes and shredded cheddar cheese. 5. Roll up the lettuce leaves to form wraps. 6. Serve immediately, or chill for a cold appetizer.',15,4,'Snack'),(3,'Tex-Mex Chicken and Cheddar Salad','1. In a large bowl, combine chopped lettuce, diced tomatoes, diced chicken, and shredded cheddar cheese. 2. Drizzle Tex-Mex dressing over the salad and toss to coat evenly. 3. Serve the salad as is or as a filling for sandwiches by spooning it into burger buns. 4. Optionally, sprinkle extra shredded cheddar cheese on top before serving.',20,4,'Dinner');
/*!40000 ALTER TABLE `Recipe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RecipeIngredient`
--

DROP TABLE IF EXISTS `RecipeIngredient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RecipeIngredient` (
  `RecipeIngredientID` int NOT NULL,
  `IngredientID` int DEFAULT NULL,
  `RecipeID` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `unitMeasure` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`RecipeIngredientID`),
  UNIQUE KEY `RecipeID` (`RecipeID`,`IngredientID`),
  KEY `RecipeIngredient_Ingredient_IngredientID_fk` (`IngredientID`),
  CONSTRAINT `recipeingredient_ibfk_2` FOREIGN KEY (`RecipeID`) REFERENCES `Recipe` (`RecipeID`),
  CONSTRAINT `RecipeIngredient_Ingredient_IngredientID_fk` FOREIGN KEY (`IngredientID`) REFERENCES `Ingredient` (`IngredientID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RecipeIngredient`
--

LOCK TABLES `RecipeIngredient` WRITE;
/*!40000 ALTER TABLE `RecipeIngredient` DISABLE KEYS */;
INSERT INTO `RecipeIngredient` VALUES (1,1,1,1,'lbs'),(2,2,1,8,'leaves'),(3,4,1,2,'medium sized'),(4,3,1,4,NULL),(5,7,1,1,'half cup'),(6,6,1,1,'cup'),(7,5,2,1,'lbs'),(8,2,2,8,'leaves'),(9,4,2,1,NULL),(10,6,2,1,'half cup'),(11,1,3,2,'cups'),(12,2,3,6,'cups'),(13,4,3,2,'medium sized'),(14,6,3,1,'cup'),(15,7,3,1,'cup');
/*!40000 ALTER TABLE `RecipeIngredient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `mealplanview`
--

/*!50001 DROP VIEW IF EXISTS `mealplanview`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `mealplanview` AS select `MP`.`MealPlanID` AS `MealPlanID`,`MP`.`MealDate` AS `MealDate`,`R`.`name` AS `RecipeName` from (`mealplan` `MP` join `recipe` `R` on((`MP`.`RecipeID` = `R`.`RecipeID`))) order by `MP`.`MealDate` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-18  0:10:55
