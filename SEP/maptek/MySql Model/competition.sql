SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for competition
-- ----------------------------
DROP TABLE IF EXISTS `competition`;
CREATE TABLE `competition` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) DEFAULT NULL,
  `description` text,
  `rank` int(11) DEFAULT NULL,
  `duetime` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of competition
-- ----------------------------
BEGIN;
INSERT INTO `competition` VALUES (2, 'Lyft 3D Object Detection for Autonomous Vehicles', 'Self-driving technology presents a rare opportunity to improve the quality of life in many of our communities. Avoidable collisions, single-occupant commuters, and vehicle emissions are choking cities, while infrastructure strains under rapid urban growth. Autonomous vehicles are expected to redefine transportation and unlock a myriad of societal, environmental, and economic benefits. You can apply your data analysis skills in this competition to advance the state of self-driving technology.\n\nLyft, whose mission is to improve people’s lives with the world’s best transportation, is investing in the future of self-driving vehicles. Level 5, their self-driving division, is working on a fleet of autonomous vehicles, and currently has a team of 450+ across Palo Alto, London, and Munich working to build a leading self-driving system (they’re hiring!). Their goal is to democratize access to self-driving technology for hundreds of millions of Lyft passengers.\n\nFrom a technical standpoint, however, the bar to unlock technical research and development on higher-level autonomy functions like perception, prediction, and planning is extremely high. This implies technical R&D on self-driving cars has traditionally been inaccessible to the broader research community.\n\nThis dataset aims to democratize access to such data, and foster innovation in higher-level autonomy functions for everyone, everywhere. By conducting a competition, we hope to encourage the research community to focus on hard problems in this space—namely, 3D object detection over semantic maps.\n\nIn this competition, you will build and optimize algorithms based on a large-scale dataset. This dataset features the raw sensor camera inputs as perceived by a fleet of multiple, high-end, autonomous vehicles in a restricted geographic area.\n\nIf successful, you’ll make a significant contribution towards stimulating further development in autonomous vehicles and empowering communities around the world.', 2, '11 oct');
INSERT INTO `competition` VALUES (7, 'fsdfdsfdsgdsg', 'sdsdadadasdasdadsad', 6, '11 oct');
INSERT INTO `competition` VALUES (8, 'ssasaadaa', 'sfsfsdfsdfsdfdsfsdf', 7, '11 oct');
INSERT INTO `competition` VALUES (9, 'fvfxvxcv', 'dsdfdsfdsfdsfsdfsf', 8, '11 oct');
INSERT INTO `competition` VALUES (10, 'vhvhvh', 'gjhjgjhgjhg', 4, '11 oct');
INSERT INTO `competition` VALUES (11, 'hgfh', 'fhgh', 6, '11 oct');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
