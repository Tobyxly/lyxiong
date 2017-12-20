
DROP TABLE IF EXISTS `email_info`;
CREATE TABLE `email_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `thread_id` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `msg_id` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL UNIQUE ,
  `receiver` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sender` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `content` text COLLATE utf8mb4_unicode_ci,
  `timestamps` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=324 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

